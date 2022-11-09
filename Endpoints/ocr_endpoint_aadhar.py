import pytesseract
from PIL import Image
import re
from flask import Flask, request 
import base64 
import os
import time


def aadhar_read_data(image):
    
    # Defining path to tesseract.exe and the image
    pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
        
    img = Image.open(image)
    
    # Extract text from image
    text = pytesseract.image_to_string(img, lang ="eng")

    res = text.split()
    name, dob, adh, sex = None, None, None, None
    text0, text1 = [], []
    lines = text.split('\n')
    for lin in lines:
        s = lin.strip()
        s = lin.replace('\n','')
        s = s.rstrip()
        s = s.lstrip()
        text1.append(s)

    if 'female' in text.lower():
        sex = "FEMALE"
    else:
        sex = "MALE"

    text1 = list(filter(None, text1))
    text0 = text1[:]

    try:
        # Cleaning first names
        name = text0[0]
        name = name.rstrip()
        name = name.lstrip()
        name = name.replace("8", "B")
        name = name.replace("0", "D")
        name = name.replace("6", "G")
        name = name.replace("1", "I")
        name = re.sub('[^a-zA-Z] +', ' ', name)

        # Cleaning DOB
        dob = text0[1][-10:]
        dob = dob.rstrip()
        dob = dob.lstrip()
        dob = dob.replace('l', '/')
        dob = dob.replace('L', '/')
        dob = dob.replace('I', '/')
        dob = dob.replace('i', '/')
        dob = dob.replace('|', '/')
        dob = dob.replace('\"', '/1')
        dob = dob.replace(":","")
        dob = dob.replace(" ", "")
    
        # Cleaning Aadhaar number details
        aadhar_number=''
        for word in res:
            if len(word) == 4 and word.isdigit():
                aadhar_number=aadhar_number  + word + ' '
        if len(aadhar_number)>=12:
            adh = aadhar_number

    except:
        pass
    
    data = {
        'ad_data' : lines,
        'ad_number': adh,
        'ad_name': name,
        'ad_dob': dob,
        'ad_sex': sex
    }

    return data

# read the images with text
# folder_dir = r"C:\Users\VSK\Downloads\OCR\Images\Aadhar"
# ad = aadhar_read_data(folder_dir)
# print(ad)

app = Flask(__name__) #define app using Flask    

@app.route('/aadhar', methods=['POST'])
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
        aadhar_data = aadhar_read_data(f) 
    os.remove('/tmp/'+timestr+".png")
    return(aadhar_data)

if __name__ == '__main__':
	app.run(debug=True)
