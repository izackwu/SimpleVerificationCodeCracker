#coding=utf-8

import requests
import configparser
import os
import sys
import glob
from PIL import Image


def checkBeforeRunning():
    modified=False
    try:
        config=configparser.ConfigParser()
        config.read("config.ini")
        modified=config.getboolean("flag","modified")
    except:
        print("config.ini has been invalidly modified or deleted!")
    return modified


def downloader():
    print("Start to download vcodes now.")
    config=configparser.ConfigParser()
    config.read("config.ini")
    url=config.get("download", "url")
    folder=config.get("download", "folder")
    num=config.getint("download", "num")
    maxAttemptTimes=config.getint("download", "maxAttemptTimes")
    successNum=0
    if os.path.exists(folder)== False:
        os.makedirs(folder)
    for i in range(0,abs(num)):
        attemptTimes=0
        while attemptTimes<maxAttemptTimes:
            attemptTimes=attemptTimes+1
            try:
                req=requests.get(url)
            except:
                print("Failed to download vcode.(Attemp {0} of {1})".format(attemptTimes,maxAttemptTimes))
            else:
                filename=folder + "/" +"{0:04d}".format(successNum) + ".jpg"
                with open(filename,"wb") as file:
                    file.write(req.content)
                successNum+=1
                print("\rDownloaded {0} of {1} vcodes successfully!".format(successNum,num),end="")
                break
    config.set("download", "successnum",str(successNum))
    config.write(open("config.ini","w"))


def binImagePrinter(binImage,mode = "default"):
    '''
        binImage must be a binarized image.
        In the output,0 = black ,1 = white.
    '''
    transformer=["0","1"]
    if mode == "special":
        transformer = ["*"," "]
    for y in range(binImage.height):
        for x in range(binImage.width):
            print(transformer[binImage.getpixel((x,y))],end='  ')
        print("\n")
    print("\n\n\n")


def ridNoise(binImage):
    '''
        binImage must be a binarized image.
        This function will rid the noise points,which have no other black point
        around them.
        (Of course this is not a perfect way,but it's enough.)
    '''
    def isNoise(xx,yy):
        '''
            If the point(xx,yy) has no other black point around it,
            then we assume it as noise.
        '''
        surrounding=0
        temp=0
        for i in range(-1,2):
            for j in range(-1,2):
                try:
                    temp=binImage.getpixel((xx + i,yy + j))
                except:
                    temp=1
                surrounding+=temp
        if surrounding >= 8:
            return True
        else:
            return False

    for y in range(binImage.height):
        for x in range(binImage.width):
            if(isNoise(x,y)==True):
                binImage.putpixel((x,y),1)


def cutAndSaveImage(binImage,num,imageOutputFolder):
    '''
        waiting to be written...
    '''
    binImage=binImage.point(lambda x:x*255)
    imagePaths=[]
    config=configparser.ConfigParser()
    config.read("config.ini")
    characterNum=config.getint("preprocess", "characternum")
    firstCharacter=[int(x) for x in config.get("preprocess", "firstcharacter").split(",")]
    step=config.getint("preprocess", "step")
    for i in range(0,characterNum):
        x1=step*i+firstCharacter[0]
        y1=firstCharacter[1]
        x2=step*i+firstCharacter[2]
        y2=firstCharacter[3]
        subImage=binImage.crop((x1,y1,x2,y2))
        path=imageOutputFolder+ "/{0:04d}-{1}.jpg".format(num,i)
        subImage.save(path)
        imagePaths.append(path)
    return imagePaths


def preprocessor():
    print("Start to preprocess vcodes now.")
    config=configparser.ConfigParser()
    config.read("config.ini")
    successNum=config.getint("download", "successnum")
    folderOfRawVcode=config.get("download", "folder")
    folderOfCuttedVcode=config.get("preprocess","folder")
    if os.path.exists(folderOfCuttedVcode)== False:
        os.makedirs(folderOfCuttedVcode)
    for i in range(0,successNum):
        imagePath=folderOfRawVcode + "/{0:04d}".format(i) + ".jpg"
        imageRaw=Image.open(imagePath)
        #imageRaw.save("CuttedVcode/raw" + str(i) + ".jpg")
        imageGrey=imageRaw.convert("L")
        #imageGrey.save("CuttedVcode/grey" + str(i) + ".jpg")
        imageBin=imageGrey.point(lambda x : x >140)
        #binImagePrinter(imageBin)     #Print the binarized image for debugging.
        ridNoise(imageBin)
        binImagePrinter(imageBin)
        cutAndSaveImage(imageBin,i,imageOutputFolder=folderOfCuttedVcode)


if __name__ == "__main__":
    if checkBeforeRunning()==False:
        print("Please modify config.ini correctly before running this program.")
        exit()
    downloader()
    preprocessor()
    print("Vcodes have been collected and preprocessed successfully.")
    print("Please run classify.py to classify images artificially.")





