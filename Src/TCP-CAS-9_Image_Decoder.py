import binascii, os, argparse, cv2, numpy, math, sys, socket
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
s.settimeout(1)
imgfr = ""
host = ip
try:
	remote_ip = socket.gethostbyname( host )
except socket.gaierror:
	print('Hostname could not be resolved. Exiting')
	sys.exit()
s.connect((remote_ip , port))
print("----------------------------------------------")
print("                                              ")
print("       XW-3 (CAS-9) Image Frames Reader       ")
print("                by Egor UB1QBJ                ")
print("                                              ")
print("----------------------------------------------")
print('Connected to ' + str(remote_ip) + ":" + str(port))
print("")
print("To stop receiving and saving photos, press the key combination (CTRL + C) in this window!")
if __name__ == "__main__":
    try:
        while True:
            try:
                reply = s.recv(555)
                imgfr = reply.hex()[:36]
                if(len(reply.hex()) == 550):
                    with open('image.data', 'ab') as ff:
                        ff.write(binascii.unhexlify(reply.hex()))
                    print("New image frame! line: " + str(n) + " | Frame Sync: 0x" + str(imgfr.upper()), end='\r')
                    n += 1
                if(len(reply.hex()) != 550):
                    print("Telemetry frame! Sync: " + imgfr + " Skip...                                     ", end='\r')
            except socket.timeout:
                continue
    except KeyboardInterrupt:
        with open('image.data', "rb") as image:
            f = image.read()
        size = os.path.getsize('image.data')
        l = int(size)/int(275)
        if(float(l).is_integer() == True):
            bbyteArray = bytearray(f)
            grayImage = numpy.array(bbyteArray).reshape(int(l), int(275))
            print("Saving 256 px...")
            cv2.imwrite(outfile, grayImage)
            print("Saved!")
            sys.exit()
        else:
            fl = math.floor(l)
            normalsize = int(275)*int(fl)
            cut = int(size-normalsize)
            bbyteArray = bytearray(f)[:-cut]
            grayImage = numpy.array(bbyteArray).reshape(int(l), int(275))
            print("Saving 256 px...")
            cv2.imwrite(outfile, grayImage)
            sys.exit()