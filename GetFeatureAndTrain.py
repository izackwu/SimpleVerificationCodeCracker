#coding=utf-8

import glob
import os
import CollectAndPreprocess
import configparser
from PIL import Image
from svmutil import *

def getFeature(imagePath):
    '''
        Return a list of the feature of a image.
        The feature includes the number of white pixels of every row and column.
    '''
    featureList=[]
    binImage=Image.open(imagePath).point(lambda x :x>140)
    for y in range(binImage.height):
        temp=0
        for x in range(binImage.width):
            temp+=binImage.getpixel((x,y))
        featureList.append(temp)
    for x in range(binImage.width):
        temp=0
        for y in range(binImage.height):
            temp+=binImage.getpixel((x,y))
        featureList.append(temp)
    return featureList


if __name__ == '__main__':
    config=configparser.ConfigParser()
    config.read("config.ini")
    classifiedFolder=config.get("classify", "folder")
    featureFilePath=config.get("getfeature", "filename")
    modelFilePath=config.get("train", "filename")
    if os.path.exists(featureFilePath):
        print("Feature file already exists,are you sure to continue?(y/n)")
        if input()[0].upper()=="Y":
            print("Okay. Note that the old data in feature file won't be erased and new data will be appended.")
        else:
            print("A wise choice.Goodbye!")
            exit()
    folders="ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    print("Start to get feature from classified vcodes.")
    for eachFolder in folders:
        if not os.path.exists(classifiedFolder + "/" +eachFolder + "/"):    #In case some characters never occur in the vcodes.
            continue
        allImagePaths=glob.iglob(classifiedFolder + "/" + eachFolder + "/*.jpg")
        bufferString="" #Reduce the times of writing data into file.
        for eachImagePath in allImagePaths:
            featureList=getFeature(eachImagePath)
            bufferString+=str(ord(eachFolder)) +  " "   #ord() converts characters to ASCII codes
            for (index,value) in enumerate(featureList):
                bufferString+= str(index+1) + ":" + str(value) + " "
            bufferString+="\n"
        #print(bufferString)
        with open(featureFilePath,"a") as featureFile:
            featureFile.write(bufferString)
    print("Successfully got the feature file {0}!".format(featureFilePath))
    print("Start to train model from feature.")
    y,x=svm_read_problem(featureFilePath)
    model=svm_train(y,x,"-q")
    svm_save_model(modelFilePath,model)
    print("Successfully got the model file {0}!".format(modelFilePath))
    print("Finally, it seems that everything has been ready.Now,run Cracker.py to have a try!")
