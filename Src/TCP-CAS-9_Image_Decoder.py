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
                if(len(reply.hex()) != 550):
                    status = "nrx"
                    now = datetime.now()
                    current_time = now.strftime("%H:%M:%S")
                    print("[" + str(current_time) + "]" + " Telemetry frame! Sync: " + imgfr + " Skip..." + " "*20, end='\r')
                    if(n > 1):
                        print("[" + str(current_time) + "]" + " Done! Lines received: " + str(n) + " Please restart the decoder to save the photo!" + " "*20, end='\r')
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
                    normalsize = int(l1)*int(fl)
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