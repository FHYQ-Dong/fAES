from Crypto.Cipher import AES
from sys import argv

def pad(text:bytes) -> bytes :
    return text + b'\x00' * ((16 - len(text) %16) % 16)

def fencrypt(FileName:str, pwd:bytes, toFileName=False) -> str :
    pwd = pad(pwd)
    with open (FileName, "rb") as f:
        data = f.read()
    cipher = AES.new(pwd, AES.MODE_EAX)
    ciphertext, tag = cipher.encrypt_and_digest(data)
    if not toFileName:
        toFileName = FileName+".bin"
    with open (toFileName, "wb") as f:
        [ f.write(x) for x in (cipher.nonce, tag, ciphertext) ]
    return toFileName

def fdecrypt(FileName:str, pwd:bytes, toFileName=False) -> str :
    with open (FileName, "rb") as f:
        nonce, tag, ciphertext = [ f.read(x) for x in (16, 16, -1) ]
    pwd = pad(pwd)
    cipher = AES.new(pwd, AES.MODE_EAX, nonce)
    data = cipher.decrypt_and_verify(ciphertext, tag)
    if not toFileName:
        toFileName = FileName[:FileName.find(".bin")]
    with open (toFileName, "wb") as f:
        f.write(data)
    return toFileName

def fencrypt_lowram(FileName:str, pwd:bytes, toFileName=False) ->str :
    pwd = pad(pwd)
    if not toFileName:
        toFileName = FileName+".bin"

    with open (FileName, "rb") as fin:
        with open (toFileName, "wb") as fout:
            data = fin.read(16*1024*1024)
            while data:
                cipher = AES.new(pwd, AES.MODE_EAX)
                ciphertext, tag = cipher.encrypt_and_digest(data)
                [ fout.write(x) for x in (cipher.nonce, tag, ciphertext) ]
                data = fin.read(16*1024*1024)
    
    return toFileName

def fdecrypt_lowram(FileName:str, pwd:bytes, toFileName=False) -> str :
    if not toFileName:
        toFileName = FileName[:FileName.find(".bin")]
    pwd = pad(pwd)

    with open (FileName, "rb") as fin:
        with open (toFileName, "wb") as fout:
            nonce, tag, ciphertext = [ fin.read(x) for x in (16, 16, 16*1024*1024) ]
            while ciphertext:
                cipher = AES.new(pwd, AES.MODE_EAX, nonce)
                data = cipher.decrypt_and_verify(ciphertext, tag)
                fout.write(data)
                nonce, tag, ciphertext = [ fin.read(x) for x in (16, 16, 16*1024*1024) ]
        
    return toFileName

def main() -> None:
    try:
        mode = argv[1]
        FileName = argv[2]
        pwd = pad(argv[3].encode("utf-8"))

        try:
            low_ram = eval(argv[4])
        except NameError:
            print("Unable to understand.")
            return
        try:
            toFileName = argv[5]
        except IndexError:
            toFileName = False

        if low_ram:
            if mode in ["encrypt", "en"]:
                print(fencrypt_lowram(FileName, pwd, toFileName))
            elif mode in ["decrypt", "de"]:
                try:
                    print(fdecrypt_lowram(FileName, pwd, toFileName))
                except ValueError:
                    print("Wrong pwd.")
                    return
            else:
                print("Unable to understand.")
                return
        else:
            if mode in ["encrypt", "en"]:
                print(fencrypt(FileName, pwd, toFileName))
            elif mode in ["decrypt", "de"]:
                try:
                    print(fdecrypt(FileName, pwd, toFileName))
                except ValueError:
                    print("Wrong pwd.")
                    return
            else:
                print("Unable to understand.")
                return
    except:
        print("Wrong arguments")
        print("args[1]:mode (encrypt/decrypt)")
        print("args[2]:FileName\nargs[3]:pwd")
        print("args[4]:low_ram (True/False)")
        print("args[5]:toFileName (optional)")
        

if __name__ == "__main__":
    main()