import os

# 定义加密参数
_KEY = 'IGS2023'.encode('utf-8')  # 将密钥转换为bytes
_ENCRYSIG = b'PNG'  # 以bytes形式指定加密签名

def decryption(fileData, key, encryS):
    """解密操作，实际上与加密操作相同，因为XOR是可逆的"""
    # 首先移除加密签名
    if fileData.startswith(encryS):
        fileData = fileData[len(encryS):]
    else:
        print("The file does not start with the expected encryption signature.")
        return fileData  # 返回未修改的数据

    # 应用与加密相同的XOR逻辑进行解密
    klen = len(key)
    decryptedData = bytearray(fileData)
    for i, byte in enumerate(decryptedData):
        decryptedData[i] = byte ^ key[i % klen]
    return decryptedData

def process_decryption(filePath, key, encrySig):
    """处理单个图片的解密"""
    with open(filePath, 'rb') as file:
        fileData = file.read()
        decryptedData = decryption(fileData, key, encrySig)
    with open(filePath, 'wb') as file:
        file.write(decryptedData)
    print(f"{os.path.basename(filePath)} has been decrypted.")

if __name__ == "__main__":
    encrypted_img_path = os.path.join(os.getcwd(), 'test_decrtpy.png')
    if os.path.exists(encrypted_img_path):
        process_decryption(encrypted_img_path, _KEY, _ENCRYSIG)
    else:
        print("Encrypted test.png does not exist in the script directory.")
