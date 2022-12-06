# XW-3 (CAS-9) Satellite Images decoder
This is an XW-3 (CAS-9) Satellite Images decoder that works in conjunction with HS_soundmodem 

![1](https://github.com/Foxiks/xw-3-images-decoder/blob/main/img/1.png)

## Using
Before use, specify the port for KISS Server in your soudmodem settings. Settings->Devices->KISS Server port

![2](https://github.com/Foxiks/xw-3-images-decoder/blob/main/img/2.png)

After that run start.bat for Windows or:
```sh
TCP-CAS-9_Image_Decoder.exe -p (--port) 8100 -ip 127.0.0.1 -o out.png
```
or
```sh
python TCP-CAS-9_Image_Decoder.py -p (--port) 8100 -ip 127.0.0.1 -o out.png
```
Note! After decoding, you can get a photo by pressing the CTRL + C key combination in the command line window. If you close it normally, the photo will not be saved!
Mode for sondmodem: FSK G3RUH 4800bd.
