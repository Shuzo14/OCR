import pytesseract
from PIL import Image
import os
import ftfy
import json
from flask import Flask, request 
import re
import time
import base64

def vehicleRC_read_data(image):
    
    # Defining path to tesseract.exe and the image
    pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
    
    img = Image.open(image)

    DL = []

    # Extract text from image
    text = pytesseract.image_to_string(img, lang ="eng")
    text = ftfy.fix_text(text)
    text = ftfy.fix_encoding(text)

    # Splitting the lines to sort the text paragraph wise
    lines = text.split('\n')
    for lin in lines:
        s = lin.strip()
        s = s.rstrip()
        s = s.lstrip()
        DL.append(s)
    
    for x in lines:
        _ = x.split()
        if ([w for w in _ if re.search("(Driving Licence|DL No|DL|Licence No|REGN)$", w)]):    
            dl_number = x
            #print(dl_number)
            
        if ([w for w in _ if re.search("(Date of Birth|DOB|D.O.B.)$", w)]):    
            dl_dob = x.split(':')[1].strip()
            #print(dob)
        
    data = json.dumps(DL)
    dl_data = {
    'DL data' : data,
    'DL Number' : dl_number,
    'DOB' : dl_dob
    }
    
    return dl_data

app = Flask(__name__) #define app using Flask    

@app.route('/dl', methods=['POST'])
def aadhar():
    bs = { "image": request.json['image']}
    img_file = (bs["image"])
    res = bytes(img_file, 'utf-8')
    value = base64.decodebytes(res)
    timestr = time.strftime("%Y%m%d-%H%M%S")
    f = open('/tmp/'+timestr+".png",'wb')
    f.write(value)
    f.close()
    with open('/tmp/'+timestr+".png",'rb') as f:
        dl_data = vehicleRC_read_data(f) 
    os.remove('/tmp/'+timestr+".png")
    return(dl_data)

if __name__ == '__main__':
	app.run(debug=True)