#coding=utf-8

import requests

vcodeSource="http://{0}.com/inc/checkcode.asp"
domain=input("\nPlease input the domain of vcode source:")
folder=input("\nPlease input the folder to save vcodes:")
num=int(input("\nPlease input how many vcodes are to be downloaded:"))
for i in range(0,num):
    req=requests.get(vcodeSource.format(domain))
    filename=folder + "/" +str(i) + ".jpg"
    with open(filename,"wb") as file:
        file.write(req.content)
print("Done!\n")



