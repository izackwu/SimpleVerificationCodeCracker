#coding=utf-8

import CollectAndPreprocess
import GetFeatureAndTrain
import svmutil
import configparser
import requests
import os
from io import BytesIO
from PIL import Image

def cracker(imageRaw,tempFolder,modelFilePath,mode="default"):
    '''
        imageRaw is the object returned by PIL.Image.open()
        tempFolder is the temporary folder to store some temp files
        modelFilePath is the path of trained model
        if mode="quiet",then this function produces no output
        This function returns the result of cracking
    '''
    imageGrey=imageRaw.convert("L")
    imageBin=imageGrey.point(lambda x : x >140)
    CollectAndPreprocess.ridNoise(imageBin)
    imagePaths=CollectAndPreprocess.cutAndSaveImage(imageBin,i,tempFolder)
    result=""
    for eachPath in imagePaths:
        featureList=GetFeatureAndTrain.getFeature(eachPath)
        os.remove(eachPath)
        #print(featureList)
        featureDict={}
        for (index,value) in enumerate(featureList):
            featureDict[index+1]=value
        xt=[]
        xt.append(featureDict)
        yt=[0]
        model=svmutil.svm_load_model(modelFilePath)
        p_label,p_acc,p_val=svmutil.svm_predict(yt, xt, model,"-q")
        for item in p_label:
          result+=chr(int(item))
    if mode=="default":
        print(result)
    return result


if __name__ == '__main__':
    config=configparser.ConfigParser()
    config.read("config.ini")
    tempFolder=config.get("crack","tempfolder")
    if not os.path.exists(tempFolder + "/"):
        os.mkdir(tempFolder)
    modelFilePath=config.get("train","filename")
    num=config.getint("crack", "num")
    url=""
    try:
        url=config.get("crack", "url")
    except:
        url=config.get("download", "url")
        print("Can't get url..Using default url of downloading.")
    for i in range(0,num):
        try:
            req=requests.get(url)
            temp=BytesIO()
            temp.write(req.content)
            result=cracker(Image.open(temp),tempFolder,modelFilePath)
            with open(tempFolder+"/"+result + ".jpg","wb") as file:
                file.write(req.content)
        except:
            print("Something wrong...")




