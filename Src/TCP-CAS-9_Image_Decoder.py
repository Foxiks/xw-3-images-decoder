import binascii, os, argparse, cv2, sys, socket, math
import numpy as np
from datetime import datetime
parser = argparse.ArgumentParser()
parser.add_argument("-p", "--port", help="port")
parser.add_argument("-ip", "--ip", help="ip")
parser.add_argument("-o", "--out", help="out image name")
outfile = parser.parse_args().out
ip = parser.parse_args().ip
port1 = parser.parse_args().port
port = int(port1)
n = 1
try:
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except socket.error:
	print('Failed to create socket')
	sys.exit()
s.settimeout(0.5) #<-- (1(sec)/4800(symbol_rate))*2200(packet_symbols) + buff()
imgfr = ""
host = ip
mode = 0
status = "nrx"
try:
	remote_ip = socket.gethostbyname( host )
except socket.gaierror:
	print('Hostname could not be resolved. Exiting')
	sys.exit()
s.connect((remote_ip , port))
print("------------------------------------------------------")
print("                                                      ")
print("       XW-3 (CAS-9) Image Frames Reader/Decoder       ")
print("                    by Egor UB1QBJ                    ")
print("                                                      ")
print("------------------------------------------------------")
print('Connected to ' + str(remote_ip) + ":" + str(port))
print("")
print("To stop receiving and saving photos, press the key combination (CTRL + C) in this window!")
print("")
if __name__ == "__main__":
    try:
        while True:
            try:
                reply = s.recv(1024)
                imgfr = reply.hex()[:36]
                catalogfr = reply.hex()[:50]
                if(len(reply.hex()) == 550):
                    status = "rx"
                    mode = 256
                    with open('image.data', 'ab') as ff:
                        ff.write(binascii.unhexlify(reply.hex()[36:-2]))
                    now = datetime.now()
                    current_time = now.strftime("%H:%M:%S")
                    print("[" + str(current_time) + "]" + " New image frame! line: " + str(n) + " | Frame Sync: 0x" + str(imgfr.upper()), end='\r')
                    n += 1
                    if(n >= 265):
                        mode = 512
                if(len(reply.hex()) != 550 and len(reply.hex()) != 212):
                    status = "nrx"
                    now = datetime.now()
                    current_time = now.strftime("%H:%M:%S")
                    print("[" + str(current_time) + "]" + " Telemetry frame! Sync: " + imgfr + " Skip..." + " "*20, end='\r')
                    if(n > 1):
                        print("[" + str(current_time) + "]" + " Done! Lines received: " + str(n) + " Please restart the decoder to save the photo!" + " "*20, end='\r')
                if(len(reply.hex()) == 212):
                    if(catalogfr == "c00086a240404040608682a67240406103f002000100010057"):
                        print("Catalog Frame!" + " "*100)
                        c1y = str(int(reply.hex()[50:52], 16))
                        if(len(c1y) == 1):
                            c1y = "0" + str(int(reply.hex()[50:52], 16))
                        c1m = str(int(reply.hex()[52:54], 16))
                        if(len(c1m) == 1):
                            c1m = "0" + str(int(reply.hex()[52:54], 16))
                        c1d = str(int(reply.hex()[54:56], 16))
                        if(len(c1d) == 1):
                            c1d = "0" + str(int(reply.hex()[54:56], 16))
                        c1h = str(int(reply.hex()[56:58], 16))
                        if(len(c1h) == 1):
                            c1h = "0" + str(int(reply.hex()[56:58], 16))
                        c1min = str(int(reply.hex()[58:60], 16))
                        if(len(c1min) == 1):
                            c1min = "0" + str(int(reply.hex()[58:60], 16))
                        c1s = str(int(reply.hex()[60:62], 16))
                        if(len(c1s) == 1):
                            c1s = "0" + str(int(reply.hex()[60:62], 16))
                        print("*01# -> " + "20"+str(c1y)+"."+str(c1m)+"."+str(c1d) + " - " + str(c1h)+":"+str(c1min)+":"+str(c1s))
                        c2y = str(int(reply.hex()[66:68], 16))
                        c2m = str(int(reply.hex()[68:70], 16))
                        c2d = str(int(reply.hex()[70:72], 16))
                        c2h = str(int(reply.hex()[72:74], 16))
                        c2min = str(int(reply.hex()[74:76], 16))
                        c2s = str(int(reply.hex()[76:78], 16))
                        if(len(c2y) == 1):
                            c2y = "0" + str(c2y)
                        if(len(c2m) == 1):
                            c2m = "0" + str(c2m)
                        if(len(c2d) == 1):
                            c2d = "0" + str(c2d)
                        if(len(c2h) == 1):
                            c2h = "0" + str(c2h)
                        if(len(c2min) == 1):
                            c2min = "0" + str(c2min)
                        if(len(c2s) == 1):
                            c2s = "0" + str(c2s)
                        print("*02# -> " + "20"+str(c2y)+"."+str(c2m)+"."+str(c2d) + " - " + str(c2h)+":"+str(c2min)+":"+str(c2s))
                        c3y = str(int(reply.hex()[82:84], 16))
                        c3m = str(int(reply.hex()[84:86], 16))
                        c3d = str(int(reply.hex()[86:88], 16))
                        c3h = str(int(reply.hex()[88:90], 16))
                        c3min = str(int(reply.hex()[90:92], 16))
                        c3s = str(int(reply.hex()[92:94], 16))
                        if(len(c3y) == 1):
                            c3y = "0" + str(c3y)
                        if(len(c3m) == 1):
                            c3m = "0" + str(c3m)
                        if(len(c3d) == 1):
                            c3d = "0" + str(c3d)
                        if(len(c3h) == 1):
                            c3h = "0" + str(c3h)
                        if(len(c3min) == 1):
                            c3min = "0" + str(c3min)
                        if(len(c3s) == 1):
                            c3s = "0" + str(c3s)
                        print("*03# -> " + "20"+str(c3y)+"."+str(c3m)+"."+str(c3d) + " - " + str(c3h)+":"+str(c3min)+":"+str(c3s))
                        c4y = str(int(reply.hex()[98:100], 16))
                        c4m = str(int(reply.hex()[100:102], 16))
                        c4d = str(int(reply.hex()[102:104], 16))
                        c4h = str(int(reply.hex()[104:106], 16))
                        c4min = str(int(reply.hex()[106:108], 16))
                        c4s = str(int(reply.hex()[108:110], 16))
                        if(len(c4y) == 1):
                            c4y = "0" + str(c4y)
                        if(len(c4m) == 1):
                            c4m = "0" + str(c4m)
                        if(len(c4d) == 1):
                            c4d = "0" + str(c4d)
                        if(len(c4h) == 1):
                            c4h = "0" + str(c4h)
                        if(len(c4min) == 1):
                            c4min = "0" + str(c4min)
                        if(len(c4s) == 1):
                            c4s = "0" + str(c4s)
                        print("*04# -> " + "20"+str(c4y)+"."+str(c4m)+"."+str(c4d) + " - " + str(c4h)+":"+str(c4min)+":"+str(c4s))
                        c5y = str(int(reply.hex()[114:116], 16))
                        c5m = str(int(reply.hex()[116:118], 16))
                        c5d = str(int(reply.hex()[118:120], 16))
                        c5h = str(int(reply.hex()[120:122], 16))
                        c5min = str(int(reply.hex()[122:124], 16))
                        c5s = str(int(reply.hex()[124:126], 16))
                        if(len(c5y) == 1):
                            c5y = "0" + str(c5y)
                        if(len(c5m) == 1):
                            c5m = "0" + str(c5m)
                        if(len(c5d) == 1):
                            c5d = "0" + str(c5d)
                        if(len(c5h) == 1):
                            c5h = "0" + str(c5h)
                        if(len(c5min) == 1):
                            c5min = "0" + str(c5min)
                        if(len(c5s) == 1):
                            c5s = "0" + str(c5s)
                        print("*05# -> " + "20"+str(c5y)+"."+str(c5m)+"."+str(c5d) + " - " + str(c5h)+":"+str(c5min)+":"+str(c5s))
                        c6y = str(int(reply.hex()[130:132], 16))
                        c6m = str(int(reply.hex()[132:134], 16))
                        c6d = str(int(reply.hex()[134:136], 16))
                        c6h = str(int(reply.hex()[136:138], 16))
                        c6min = str(int(reply.hex()[138:140], 16))
                        c6s = str(int(reply.hex()[140:142], 16))
                        if(len(c6y) == 1):
                            c6y = "0" + str(c6y)
                        if(len(c6m) == 1):
                            c6m = "0" + str(c6m)
                        if(len(c6d) == 1):
                            c6d = "0" + str(c6d)
                        if(len(c6h) == 1):
                            c6h = "0" + str(c6h)
                        if(len(c6min) == 1):
                            c6min = "0" + str(c6min)
                        if(len(c6s) == 1):
                            c6s = "0" + str(c6s)
                        print("*06# -> " + "20"+str(c6y)+"."+str(c6m)+"."+str(c6d) + " - " + str(c6h)+":"+str(c6min)+":"+str(c6s))
                        c7y = str(int(reply.hex()[146:148], 16))
                        c7m = str(int(reply.hex()[148:150], 16))
                        c7d = str(int(reply.hex()[150:152], 16))
                        c7h = str(int(reply.hex()[152:154], 16))
                        c7min = str(int(reply.hex()[154:156], 16))
                        c7s = str(int(reply.hex()[156:158], 16))
                        if(len(c7y) == 1):
                            c7y = "0" + str(c7y)
                        if(len(c7m) == 1):
                            c7m = "0" + str(c7m)
                        if(len(c7d) == 1):
                            c7d = "0" + str(c7d)
                        if(len(c7h) == 1):
                            c7h = "0" + str(c7h)
                        if(len(c7min) == 1):
                            c7min = "0" + str(c7min)
                        if(len(c7s) == 1):
                            c7s = "0" + str(c7s)
                        print("*07# -> " + "20"+str(c7y)+"."+str(c7m)+"."+str(c7d) + " - " + str(c7h)+":"+str(c7min)+":"+str(c7s))
                        c8y = str(int(reply.hex()[162:164], 16))
                        c8m = str(int(reply.hex()[164:166], 16))
                        c8d = str(int(reply.hex()[166:168], 16))
                        c8h = str(int(reply.hex()[168:170], 16))
                        c8min = str(int(reply.hex()[170:172], 16))
                        c8s = str(int(reply.hex()[172:174], 16))
                        if(len(c8y) == 1):
                            c8y = "0" + str(c8y)
                        if(len(c8m) == 1):
                            c8m = "0" + str(c8m)
                        if(len(c8d) == 1):
                            c8d = "0" + str(c8d)
                        if(len(c8h) == 1):
                            c8h = "0" + str(c8h)
                        if(len(c8min) == 1):
                            c8min = "0" + str(c8min)
                        if(len(c8s) == 1):
                            c8s = "0" + str(c8s)
                        print("*08# -> " + "20"+str(c8y)+"."+str(c8m)+"."+str(c8d) + " - " + str(c8h)+":"+str(c8min)+":"+str(c8s))
                        c9y = str(int(reply.hex()[178:180], 16))
                        c9m = str(int(reply.hex()[180:182], 16))
                        c9d = str(int(reply.hex()[182:184], 16))
                        c9h = str(int(reply.hex()[184:186], 16))
                        c9min = str(int(reply.hex()[186:188], 16))
                        c9s = str(int(reply.hex()[188:190], 16))
                        if(len(c9y) == 1):
                            c9y = "0" + str(c9y)
                        if(len(c9m) == 1):
                            c9m = "0" + str(c9m)
                        if(len(c9d) == 1):
                            c9d = "0" + str(c9d)
                        if(len(c9h) == 1):
                            c9h = "0" + str(c9h)
                        if(len(c9min) == 1):
                            c9min = "0" + str(c9min)
                        if(len(c9s) == 1):
                            c9s = "0" + str(c9s)
                        print("*09# -> " + "20"+str(c9y)+"."+str(c9m)+"."+str(c9d) + " - " + str(c9h)+":"+str(c9min)+":"+str(c9s))
                        c10y = str(int(reply.hex()[194:196], 16))
                        c10m = str(int(reply.hex()[196:198], 16))
                        c10d = str(int(reply.hex()[198:200], 16))
                        c10h = str(int(reply.hex()[200:202], 16))
                        c10min = str(int(reply.hex()[202:204], 16))
                        c10s = str(int(reply.hex()[204:206], 16))
                        if(len(c10y) == 1):
                            c10y = "0" + str(c10y)
                        if(len(c10m) == 1):
                            c10m = "0" + str(c10m)
                        if(len(c10d) == 1):
                            c10d = "0" + str(c10d)
                        if(len(c10h) == 1):
                            c10h = "0" + str(c10h)
                        if(len(c10min) == 1):
                            c10min = "0" + str(c10min)
                        if(len(c10s) == 1):
                            c10s = "0" + str(c10s)
                        print("*10# -> " + "20"+str(c10y)+"."+str(c10m)+"."+str(c10d) + " - " + str(c10h)+":"+str(c10min)+":"+str(c10s))
            except socket.timeout:
                if(status == "rx"):
                    now = datetime.now()
                    current_time = now.strftime("%H:%M:%S")
                    if(n <= 1026):
                        with open('image.data', 'ab') as ff:
                            ff.write(binascii.unhexlify("00"*256))
                        print("[" + str(current_time) + "]" + " Bad image frame!" + " "*70, end='\r')
                        n += 1
                continue
    except KeyboardInterrupt:
        with open('image.data', "rb") as image1:
            f = image1.read()
        size = os.path.getsize('image.data')
        l = int(size)/int(256)
        if(float(l).is_integer() == True):
            if(mode == 256):
                bbyteArray = bytearray(f)
                grayImage = np.array(bbyteArray).reshape(int(l), int(256))
                print("Saving 256 px..." + " "*100)
                cv2.imwrite(outfile, grayImage)
                print("Saving 256 px normalized..." + " "*100)
                alpha = 1.5 # Contrast control (1.0-3.0)
                beta = 1.7 # Brightness control (0-100)
                manual_result = cv2.convertScaleAbs(grayImage, alpha=alpha, beta=beta)
                cv2.imwrite(str('normalized_')+outfile, manual_result)
                print("Saved!" + " "*100)
                os.remove('image.data')
                sys.exit()
            if(mode == 512):
                l1 = int(size)/int(256*2)
                if(float(l1).is_integer() == True):
                    bbyteArray = bytearray(f)
                    grayImage2 = np.array(bbyteArray).reshape(int(l1), int(256*2))
                    print("Saving 512 px..." + " "*100)
                    cv2.imwrite(outfile, grayImage2)
                    print("Saving 512 px normalized..." + " "*100)
                    alpha = 1.5 # Contrast control (1.0-3.0)
                    beta = 1.7 # Brightness control (0-100)
                    manual_result2 = cv2.convertScaleAbs(grayImage2, alpha=alpha, beta=beta)
                    cv2.imwrite(str('normalized_')+outfile, manual_result2)
                    print("Saved!" + " "*100)
                    os.remove('image.data')
                    sys.exit()
                else:
                    fl = math.floor(l1)
                    normalsize = int(512)*int(fl)
                    cut = int(size-normalsize)
                    print("Converting...")
                    #print(cut)
                    bbyteArray = bytearray(f)[:-cut]
                    grayImage2 = np.array(bbyteArray).reshape(int(l1), int(256*2))
                    print("Saving 512 px..." + " "*100)
                    cv2.imwrite(outfile, grayImage2)
                    print("Saving 512 px normalized..." + " "*100)
                    alpha = 1.5 # Contrast control (1.0-3.0)
                    beta = 1.7 # Brightness control (0-100)
                    manual_result2 = cv2.convertScaleAbs(grayImage2, alpha=alpha, beta=beta)
                    cv2.imwrite(str('normalized_')+outfile, manual_result2)
                    print("Saved!" + " "*100)
                    os.remove('image.data')
                    sys.exit()