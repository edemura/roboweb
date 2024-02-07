from PyPDF2 import PdfReader
from PIL import Image
from pyzbar.pyzbar import decode
import os


def parse_tasks(file):

    reader = PdfReader(file)
    page = reader.pages[0]
    strings=page.extract_text().split('\n')
    print(strings)



    count=0
    listfiles=[]
    tasks=[]


    for image_file_object in page.images:
        filename=str(count) + image_file_object.name
        listfiles.append(filename)
        with open(filename, "wb") as fp:
            fp.write(image_file_object.data)
            count += 1

    print(listfiles)

    for file in listfiles:   
        img_code=Image.open(file)
        decoded=decode(img_code)
        data=decoded[0].data

        task={'analysis':strings.pop(0) , 'fio':strings.pop(0) , 'code': data}
        tasks.append(task)
        print(data)
        os.remove(file)
        
    print(tasks)


    return tasks

  
    