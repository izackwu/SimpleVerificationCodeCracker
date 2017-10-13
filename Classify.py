#coding=utf-8

from PIL import Image
import configparser
import os
import CollectAndPreprocess
import glob
import shutil

if __name__ == '__main__':
    config=configparser.ConfigParser()
    config.read("config.ini")
    unclassifiedFolder=config.get("preprocess","folder")
    classifiedFolder=config.get("classify","folder")
    allUnclassifiedImages=glob.iglob(unclassifiedFolder + "\*.jpg")
    if os.path.exists(classifiedFolder)==False:
        os.mkdir(classifiedFolder)
    successNum=0
    try:
        for imagePath in allUnclassifiedImages:
            unclassifiedImage=Image.open(imagePath)
            tempImage=unclassifiedImage.point(lambda x : x>140 )
            CollectAndPreprocess.binImagePrinter(tempImage,mode = "special")
            while True:
                try:
                    character=input("\nPlease input the character in this image:")
                    targetPath=classifiedFolder + "/" + character[0].upper() + "/"
                    if os.path.exists(targetPath)==False:
                        os.mkdir(targetPath)
                    shutil.move(imagePath, targetPath)
                except Exception:
                    print("\nThere's something wrong,please try again.(Enter Ctrl + C to exit)")
                else:
                    successNum+=1
                    break
    except: #If enter Ctrl+C to quit.
        print("\nOkay,let's have a break now.")
        print("You have classified {0} characters this time.".format(successNum))
    else:   #If finish all the classification.
        print("\nWell done! You have classified all the characters!")
        print("Now,Please run GetFeatureAndTrain.py")







