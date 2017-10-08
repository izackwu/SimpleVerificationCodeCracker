#coding=utf-8

import requests
import configparser
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
    config=configparser.ConfigParser()
    config.read("config.ini")
    url=config.get("download", "url")
    folder=config.get("download", "folder")
    num=config.getint("download", "num")
    maxAttemptTimes=config.getint("download", "maxAttemptTimes")
    for i in range(0,abs(num)):
        attemptTimes=0
        while attemptTimes<maxAttemptTimes:
            attemptTimes=attemptTimes+1
            try:
                req=requests.get(url)
            except:
                print("Failed to download vcode.(Attemp {0} of {1})".format(attemptTimes,maxAttemptTimes))
            else:
                filename=folder + "/" +"{0:04d}".format(i) + ".jpg"
                with open(filename,"wb") as file:
                    file.write(req.content)
                break
    print("Downloaded {0} vcodes successfully!".format(num))






if __name__ == "__main__":
    if checkBeforeRunning()==False:
        print("Please modify config.ini correctly before running this program.")
        exit()
    downloader()





