import pytesseract
from PIL import Image
import os
import matplotlib.pyplot as plt
import ftfy
import json
from flask import Flask, request 
import re
import time
import base64

def vehicleRC_read_data(folder_dir):
    
    # Defining path to tesseract.exe and the image
    path_to_tesseract = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
    pytesseract.pytesseract.tesseract_cmd = path_to_tesseract
    
    DL = []
    
    for images in folder_dir:
        if (images.endswith(".png") or images.endswith(".jpg") or images.endswith(".jpeg")):
            inputPath = os.path.join(folder_dir, images)
            img = Image.open(inputPath)

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

@app.route('/data', methods=['POST'])
def ocrData():
    dl = { "image": request.json['image']}
    dl_data = vehicleRC_read_data(dl["image"]) 
    return (dl_data)

if __name__ == '__main__':
	app.run(debug=True, port=8080)