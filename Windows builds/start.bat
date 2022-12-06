echo @off
del image.data
TCP-CAS-9_Image_Decoder.exe -p 8100 -ip 127.0.0.1 -o out.png
del image.data