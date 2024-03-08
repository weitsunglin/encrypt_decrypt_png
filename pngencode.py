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
    """处理单个图片"""
    with open(filePath, 'rb') as file:
        fileData = file.read()
        encryptedData = encryption(fileData, key, encrySig)
    with open(filePath, 'wb') as file:
        file.write(encryptedData)
    print(f"{os.path.basename(filePath)} has been encrypted.")

if __name__ == "__main__":
    test_img_path = os.path.join(os.getcwd(), 'test.png')
    if os.path.exists(test_img_path):
        process_image(test_img_path, _KEY, _ENCRYSIG)
    else:
        print("test.png does not exist in the script directory.")
