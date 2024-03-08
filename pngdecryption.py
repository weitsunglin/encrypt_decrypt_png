import os

# 定义加密参数
_KEY = 'IGS2023'.encode('utf-8')  # 将密钥转换为bytes
_ENCRYSIG = b'PNG'  # 以bytes形式指定加密签名

def decryption(fileData, key, encryS):
    """解密操作，实际上与加密操作相同，因为XOR是可逆的"""
    if fileData.startswith(encryS):
        fileData = fileData[len(encryS):]  # 移除加密签名
    else:
        print("The file does not start with the expected encryption signature.")
        return None  # 如果文件不包含预期的签名，则返回None
    klen = len(key)
    decryptedData = bytearray(fileData)
    for i, byte in enumerate(decryptedData):
        decryptedData[i] = byte ^ key[i % klen]
    return decryptedData

def process_decryption(inputFilePath, outputFilePath, key, encrySig):
    """处理单个图片的解密，并保存为新文件"""
    if os.path.exists(inputFilePath):
        with open(inputFilePath, 'rb') as file:
            fileData = file.read()
            decryptedData = decryption(fileData, key, encrySig)
            if decryptedData is not None:
                with open(outputFilePath, 'wb') as outFile:
                    outFile.write(decryptedData)
                print(f"{os.path.basename(inputFilePath)} has been decrypted and saved as {os.path.basename(outputFilePath)}")
            else:
                print("Decryption failed. The file might not be encrypted with the expected signature.")
    else:
        print(f"{os.path.basename(inputFilePath)} does not exist.")

if __name__ == "__main__":
    encrypted_img_path = os.path.join(os.getcwd(), 'test_encrypt.png')  # 假设加密的文件名为test.png
    decrypted_img_path = os.path.join(os.getcwd(), 'test_decrypt.png')  # 解密后要保存的新文件名
    process_decryption(encrypted_img_path, decrypted_img_path, _KEY, _ENCRYSIG)
