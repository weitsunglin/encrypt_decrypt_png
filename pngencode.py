# -*- coding:UTF-8 -*-
#該脚本用於加密png&jpg圖片 使用python2.7版本執行
import os
import time
CUR_DIR = os.getcwd();
print("cur_dir:",CUR_DIR)
#CUR_DIR = 'C:\\Users\\shawn\\Desktop'
_KEY = 'IGS2023' #指定加密密鑰,英文
_ENCRYSIG = 'PNG'#不可超過_PNGSIG長度
_PNGSIG = '\x89PNG\r\n\x1a\n'
_PNGIEND = '\x00\x00\x00\x00IEND\xaeB`\x82'
_ENCRYSOI = 'JP'#不可超過_JPGSOI長度
_JPGSOI = '\xff\xd8'
_JPGEOI = '\xff\xd9'
#獲取filesig是否是png
def isPNGSig(bytes_8):
    return bytes_8 == _PNGSIG

def isPNG(absPath):#判斷是否是PNG圖片
    """
    :param absPath: 文件的绝对路径
    :return: {Bool}
    """
    isFile = os.path.isfile(absPath)
    hasPNGSig = False
    fileExt = os.path.splitext(absPath)[1]
    isPngExt = (fileExt == ".png" or fileExt == ".PNG")
    if isFile and isPngExt:
        with open(absPath,"rb") as file:
            hasPNGSig = isPNGSig(file.read(8)[:8])
    return isFile and isPngExt and hasPNGSig

#獲取filesig是否是jpg
def isJPGSOI(bytes_2):
    return bytes_2 == _JPGSOI

def isJPG(absPath):#判斷是否是JPG圖片
    """
    :param absPath: 文件的绝对路径
    :return: {Bool}
    """
    isFile = os.path.isfile(absPath)
    hasJPGSOI = False
    fileExt = os.path.splitext(absPath)[1]
    isJpgExt = (fileExt == ".jpg" or fileExt == ".JPG")
    if isFile and isJpgExt:
        with open(absPath,"rb") as file:
            hasJPGSOI = isJPGSOI(file.read(2)[:2])
    return isFile and isJpgExt and hasJPGSOI

def preProcessPng(pngData):#預備理png圖片數據
    """
    剪掉png的signature(8bytes),IEND(12Bytes)
    :param pngData:
    :return:
    """
    assert type(pngData) == bytes
    lostHeadData = pngData[8:]
    iendData = lostHeadData[-12:]
    if iendData == _PNGIEND:#防止Png已經進行過外部壓縮,丢掉了IEND
        return lostHeadData[:-12]
    else:
        return lostHeadData
    
def preProcessJpg(jpgData):#预備處理jpg圖片數據
    """
    剪掉jpg的SOI(2bytes),EOI(2Bytes)
    :param jpgData:
    :return:
    """
    assert type(jpgData) == bytes
    lostHeadData = jpgData[2:]
    iendData = lostHeadData[-2:]
    if iendData == _JPGEOI:#防止Jpg已經進行過外部壓縮,丢掉了EOI=>其實我不知道會不會發生XD
        return lostHeadData[:-2]
    else:
        return lostHeadData

def encryption(fileData,key,encryS):#加密操作 ascii占一个字節
    """
    加密png數據
    :param fileData:{bytes}預備處理後的圖片數據
    :param key:{str}密鑰
    :return:{bytes}加密後的數據
    """
    assert type(key) is str
    k = key.encode("utf8")
    klen= len(k)
    kindex = 0
    fileData = bytearray(fileData)
    for i,v in enumerate(fileData):
        if kindex >= klen:
            kindex = 0
        fileData[i] = ord(chr(v)) ^ ord(k[kindex])#加密
        kindex = kindex + 1
    return encryS + fileData

#處理图片
def processPNG(filePath):
    global filenum
    fileData = None
    print(_ENCRYSIG)
    with open(filePath,'rb') as file:
        fileData = encryption(preProcessPng(file.read()),_KEY,_ENCRYSIG)
    os.remove(filePath)
    with open(filePath,'wb') as file: #覆蓋新文件
        file.write(fileData)
    filenum = filenum + 1

#處理图片
def processJPG(filePath):
    global filenum
    fileData = None
    with open(filePath,'rb') as file:
        fileData = encryption(preProcessJpg(file.read()),_KEY,_ENCRYSOI)
    os.remove(filePath)
    with open(filePath,'wb') as file: #覆蓋新文件
        file.write(fileData)
    filenum = filenum + 1



def traverseDir(absDir):#遍歷當前目錄以及遞迴的子目錄，找到所有的圖片
    """
    :param absDir: 要遍歷的路徑
    :return: None
    """
    assert (os.path.isdir(absDir) and os.path.isabs(absDir))
    dirName = absDir
    for fileName in os.listdir(absDir):
        absFileName = os.path.join(dirName,fileName)
        if os.path.isdir(absFileName):#遞迴查找文件夾
            traverseDir(absFileName)
        elif isPNG(absFileName):
            processPNG(absFileName)
            print("PNG PROCESS %s"%absFileName)
        elif isJPG(absFileName):
            processJPG(absFileName)
            print("JPG PROCESS %s"%absFileName)
        else:
            pass


#------------------- 主函式-------------------------#
#start_clock = time.clock()
filenum = 0
#traverseDir(os.path.join(CUR_DIR,"png2"))
traverseDir(CUR_DIR)
#end_clock = time.clock()
#time = (end_clock - start_clock)*1000
print("encrypt %d Png Pictures"%filenum)
#print("use time %fms"%time)
