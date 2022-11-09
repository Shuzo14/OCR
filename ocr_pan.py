import pytesseract
from PIL import Image
import os
import re

def findword(textlist, wordstring):
    lineno = -1
    for wordline in textlist:
        xx = wordline.split( )
        if ([w for w in xx if re.search(wordstring, w)]):
            lineno = textlist.index(wordline)
            textlist = textlist[lineno+1:]
            return textlist
    return textlist

def pan_read_data(folder_dir):
    
    # Defining path to tesseract.exe and the image
    pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
    
    for images in os.listdir(folder_dir):
        inputPath = os.path.join(folder_dir, images)
        img = Image.open(inputPath)
        
        # Extract text from image
        text = pytesseract.image_to_string(img, lang ="eng")
    
        
        name, fname, dob, pan = None, None, None, None
        panline, text0, text1 = [], [], []
        
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
            text0 = findword(text0, '(Pormanam|Number|umber|Account|ccount|count|Permanent|ermanent|manent|wumm)$')
            panline = text0[0]
            pan = panline.rstrip()
            pan = pan.lstrip()
            pan = pan.replace(" ", "")
            pan = pan.replace("\"", "")
            pan = pan.replace(";", "")
            pan = pan.replace("%", "L")

        except:
            pass
        
        data = {
            'pan_data' : lines,
            'pan_name' : name,
            'pan_fname' : fname,
            'pan_dob' : dob,
            'pan_number': pan
        }

        return data
    
# read the images with text
folder_dir = r"C:\Users\VSK\Downloads\OCR\Images\PAN"
pan = pan_read_data(folder_dir)
print(pan)