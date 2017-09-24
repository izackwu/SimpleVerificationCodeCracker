#coding=utf-8

from PIL import Image


def binImagePrinter(binImage):
    '''
        binImage must be a binarized image.
        In the output,1 = black ,0 = white.
    '''
    for y in range(binImage.height):
        for x in range(binImage.width):
            print(binImage.getpixel((x,y)),end=' ')
        print("\n")
    print("\n\n\n\n\n")

def ridNoise(binImage):
    '''
        binImage must be a binarized image.
        This function will rid the noise points,which have no other black point
        around them.
        (Of course this is not a perfect way,but it's enough.)
    '''
    def isNoise(xx,yy):
        surrounding=0
        temp=0
        for i in range(-1,2):
            for j in range(-1,2):
                try:
                    temp=binImage.getpixel((xx + i,yy + j))
                except:
                    temp=0
                surrounding+=temp
        if surrounding <= 1:
            return True
        else:
            return False

    for y in range(binImage.height):
        for x in range(binImage.width):
            if(isNoise(x,y)==True):
                binImage.putpixel((x,y),0)


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
        imageGrey=imageRaw.convert("L")
        imageBin=imageGrey.point(lambda x : x < 140)
        binImagePrinter(imageBin)     #Print the binarized image for debugging.
        ridNoise(imageBin)
        binImagePrinter(imageBin)









