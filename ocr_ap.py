import pytesseract
from PIL import Image
import cv2
import os,argparse
import re
import ftfy
import sys
import json
import io

def adhaar_read_data(text):
    res=text.split()
    name = None
    dob = None
    adh = None
    sex = None
    nameline = []
    dobline = []
    text0 = []
    text1 = []
    text2 = []
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
            adh=aadhar_number
        else:
            adh="none"
        
    except:
        pass
    
    aadhar_data = {}
    aadhar_data['ID Type'] = "Adhaar"
    aadhar_data['Name'] = name
    aadhar_data['Date of Birth'] = dob
    aadhar_data['Adhaar Number'] = adh
    aadhar_data['Sex'] = sex
    return aadhar_data


def pan_read_data(text):
    name = None
    fname = None
    dob = None
    pan = None
    nameline = []
    dobline = []
    panline = []
    text0 = []
    text1 = []
    text2 = []
    lines = text.split('\n')
    for lin in lines:
        s = lin.strip()
        s = lin.replace('\n','')
        s = s.rstrip()
        s = s.lstrip()
        text1.append(s)
    
    text1 = list(filter(None, text1))
    lineno = 0
    
    for wordline in text1:
        xx = wordline.split('\n')
        if ([w for w in xx if re.search('(INCOMETAXDEPARWENT|INCOME|TAX|GOW|GOVT|GOVERNMENT|OVERNMENT|VERNMENT|DEPARTMENT|EPARTMENT|PARTMENT|ARTMENT|INDIA|NDIA)$', w)]):
            text1 = list(text1)
            lineno = text1.index(wordline)
            break
    text0 = text1[lineno+1:]
    
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
        
        # Cleaning Father's name
        fname = text0[1]
        fname = fname.rstrip()
        fname = fname.lstrip()
        fname = fname.replace("8", "S")
        fname = fname.replace("0", "O")
        fname = fname.replace("6", "G")
        fname = fname.replace("1", "I")
        fname = fname.replace("\"", "A")
        fname = re.sub('[^a-zA-Z] +', ' ', fname)
        
        # Cleaning DOB
        dob = text0[2][:10]
        dob = dob.rstrip()
        dob = dob.lstrip()
        dob = dob.replace('l', '/')
        dob = dob.replace('L', '/')
        dob = dob.replace('I', '/')
        dob = dob.replace('i', '/')
        dob = dob.replace('|', '/')
        dob = dob.replace('\"', '/1')
        dob = dob.replace(" ", "")
        
        # Cleaning PAN Card details
        text0 = findword(text1, '(Pormanam|Number|umber|Account|ccount|count|Permanent|ermanent|manent|wumm)$')
        panline = text0[0]
        pan = panline.rstrip()
        pan = pan.lstrip()
        pan = pan.replace(" ", "")
        pan = pan.replace("\"", "")
        pan = pan.replace(";", "")
        pan = pan.replace("%", "L")
    
    except:
        pass
    
    pan_data = {}
    pan_data['ID Type'] = "PAN"
    pan_data['Name'] = name
    pan_data['Father Name'] = fname
    pan_data['Date of Birth'] = dob
    pan_data['PAN'] = pan
    
    pan_json = []
    return pan_data


# Using regex to find the neceesary information
def findword(textlist, wordstring):
    lineno = -1
    for wordline in textlist:
        xx = wordline.split( )
        if ([w for w in xx if re.search(wordstring, w)]):
            lineno = textlist.index(wordline)
            textlist = textlist[lineno+1:]
            return textlist
    return textlist

def extract_data(images_dir):
    
    # Defining path to tesseract.exe and the image
    pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
    
    data_list = []
    
    # Iterating the images inside the folder
    for imageName in os.listdir(images_dir):
        inputPath = os.path.join(images_dir, imageName)
        img = Image.open(inputPath)
        
        # Extract text from image
        text = pytesseract.image_to_string(img, lang ="eng")
        text = ftfy.fix_text(text)
        text = ftfy.fix_encoding(text)
        
        # Read the Aadhar and PAN number
        
        #for reading Aadhar Card Details
        if "male" in text.lower():
            data = adhaar_read_data(text)
            data_list.append(data)
            
        #for reading PAN Card Details
        elif "income" in text.lower() or "tax" in text.lower() or "department" in text.lower():
            data = pan_read_data(text)
            data_list.append(data)
    
    #print(data_list)
    data_json = json.dumps(data_list)
    return "{" + "\"OCR\"" + ":" + data_json + "}"
    

#input folder
#images_dir = r"C:\Users\VSK\Downloads\OCR\Images"   
#extract_data(images_dir)

from flask import Flask, jsonify, request #import objects from the Flask model
import json
app = Flask(__name__) #define app using Flask    

@app.route('/data', methods=['POST'])
def ocrData():
    ocr = { "images_dir": request.json['images_dir']}
    ocr_data = extract_data(ocr["images_dir"]) 
    return (ocr_data)

if __name__ == '__main__':
	app.run(debug=True, port=8080) #run app on port 8080 in debug mode