#coding=utf-8

from PIL import Image
import os
import Preprocess
import glob
import shutil

if __name__ == '__main__':
    filePath="CuttedVcode/"
    allUnclassifiedImages=glob.iglob(filePath + "*.jpg")
    for imagePath in allUnclassifiedImages:
        #print(imagePath)
        unclassifiedImage=Image.open(imagePath)
        tempImage=unclassifiedImage.point(lambda x : x>140 )
        Preprocess.binImagePrinter(tempImage,mode = "special")
        #Preprocess.binImagePrinter(unclassifiedImage)
        while True:
            try:
                content=input("\nPlease input the content of this image:")
                shutil.move(imagePath, "ClassifiedVcode/" + content[0] + "/")
            except Exception:
                print("\nThere's something wrong,please try again.(Enter Ctrl + C to exit)")
            else:
                break





