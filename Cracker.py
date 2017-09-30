#coding=utf-8

import Preprocess
import GetFeature
import svmutil
from PIL import Image


if __name__ == '__main__':
    num=int(input("Please input how many vcodes to crack:"))
    model=svmutil.svm_load_model("First.model")
    for i in range(num):
        imagePath="TestVcode/" + str(i) + ".jpg"
        imageRaw=Image.open(imagePath)
        imageGrey=imageRaw.convert("L")
        imageBin=imageGrey.point(lambda x : x >140)
        Preprocess.ridNoise(imageBin)
        imagePaths=Preprocess.cutAndSaveImage(imageBin,i,"Temp")
        bufferString=""
        print("The content of Vcode %d is:" % i)
        for eachPath in imagePaths:
            featureList=GetFeature.getFeature(eachPath)
            #print(featureList)
            featureDict={}
            for (index,value) in enumerate(featureList):
                featureDict[index+1]=value
            xt=[]
            xt.append(featureDict)
            yt=[0]
            p_label,p_acc,p_val=svmutil.svm_predict(yt, xt, model,"-q")
            cnt = 0
            for item in p_label:
                print('%s' % chr(int(item)),end="")
        print("\n")

