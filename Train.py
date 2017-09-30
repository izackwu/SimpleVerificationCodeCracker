#coding=utf-8

import os
#os.chdir("C:\Program Files\libsvm-3.22\python")
from svmutil import *


if __name__ == '__main__':
    featureFilePath="C:\Python Code\SimpleVerificationCodeCracker\Feature.data"
    y,x=svm_read_problem(featureFilePath)
    model=svm_train(y,x)
    svm_save_model("C:\Python Code\SimpleVerificationCodeCracker\First.model",model)

