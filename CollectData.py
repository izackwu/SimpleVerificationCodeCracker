#coding=utf-8

import requests

vcodeSource="http://****.com/inc/checkcode.asp"
num=int(input("Please enter how many vcodes are to be downloaded:"))
for i in range(0,num):
    req=requests.get(vcodeSource)
    filename="RawVcode/"+str(i)+".jpg"
    with open(filename,"wb") as file:
        file.write(req.content)
print("Done!\n")



