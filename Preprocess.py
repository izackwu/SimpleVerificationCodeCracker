#coding=utf-8

from PIL import Image


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
            print(transformer[binImage.getpixel((x,y))],end=' ')
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

def cutAndSaveImage(binImage,num):
    '''
        a
    '''
    #imageOutputPath="CuttedVcode/" + str(num) + ".jpg"
    #binImage.save(imageOutputPath)
    binImage=binImage.point(lambda x:x*255)
    #binImagePrinter(binImage)
    for i in range(0,4):
        subImage=binImage.crop((10*i+1,0,10*i+9,10))
        #imageOutputPath="CuttedVcodeBMP/" + str(num) + "-" + str(i) + ".bmp"
        imageOutputPath="CuttedVcode/" + str(num) + "-" + str(i) + ".jpg"
        #binImagePrinter(subImage)
        subImage.save(imageOutputPath)


if __name__=="__main__":
    begin,end = 0,0
    while True:
        try:
            begin=int(input("Please enter the number of the first image:"))
            end=int(input("Please enter the number of the last image:"))
        except KeyboardInterrupt:
            print("\nGoodbye!\n")
            exit()
        except Exception:
            print("Invalid input,please try again.(Enter Ctrl+C to exit)")
        else:
            break
    for i in range(begin,end + 1):
        imagePath="RawVcode/" + str(i) + ".jpg"
        imageRaw=Image.open(imagePath)
        #imageRaw.save("CuttedVcode/raw" + str(i) + ".jpg")
        imageGrey=imageRaw.convert("L")
        #imageGrey.save("CuttedVcode/grey" + str(i) + ".jpg")
        imageBin=imageGrey.point(lambda x : x >140)
        binImagePrinter(imageBin)     #Print the binarized image for debugging.
        ridNoise(imageBin)
        binImagePrinter(imageBin)
        cutAndSaveImage(imageBin,i)









