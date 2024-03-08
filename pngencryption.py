import os

# 定义加密参数
_KEY = 'IGS2023'.encode('utf-8')  # 将密钥转换为bytes
_ENCRYSIG = b'PNG'  # 以bytes形式指定加密签名

def encryption(fileData, key, encryS):
    """加密操作"""
    klen = len(key)
    encryptedData = bytearray(fileData)
    for i, byte in enumerate(encryptedData):
        encryptedData[i] = byte ^ key[i % klen]
    return encryS + encryptedData

def process_image(filePath, key, encrySig):
    """处理单个图片，并输出为新的加密文件"""
    with open(filePath, 'rb') as file:
        fileData = file.read()
        encryptedData = encryption(fileData, key, encrySig)
    
    # 构建加密文件的路径，更改文件名
    encryptedFilePath = os.path.splitext(filePath)[0] + '_encrtpy.png'
    
    with open(encryptedFilePath, 'wb') as file:
        file.write(encryptedData)
    print(f"{os.path.basename(encryptedFilePath)} has been encrypted.")

if __name__ == "__main__":
    test_img_path = os.path.join(os.getcwd(), 'test_decrtpy.png')
    if os.path.exists(test_img_path):
        process_image(test_img_path, _KEY, _ENCRYSIG)
    else:
        # 注意这里的文件名也做相应的调整
        print("test_decrtpy.png does not exist in the script directory.")
