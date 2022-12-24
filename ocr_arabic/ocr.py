import os
import tempfile
import pytesseract as pt
from zipfile import ZipFile
from pdf2image import convert_from_path
from PIL import Image
from tqdm import tqdm


class OCR:
    '''OCR that can convert pdf or image to text'''

    def __init__(self, file_path: str) -> None:
        self.file_path = file_path
        pass

    def convert_file_to_zip(self, output_folder: str) -> None:
        '''Convert pdf to text and archive the result to Result.zip then store it in output folder'''
        # initialize temorary directory
        with tempfile.TemporaryDirectory() as tempDir:
            # convert pdf to image
            print('Initializing...')
            convert_from_path(self.file_path, output_folder=tempDir)

            # iterating the images inside the folder
            for imageName in tqdm(os.listdir(tempDir)):
                img = Image.open(os.path.join(tempDir, imageName))

                # convert img to string (arabic) with pytesseract
                text = pt.image_to_string(img, config="-l ara")

                # take 7 last character as imageName exluding .ppm extension
                imageName = imageName.split('-')[-1:][0]
                imageName = imageName[:-4]

                fullTempPath = os.path.join(tempDir, imageName+".txt")

                # saving the  text for every image in a separate .txt file
                with open(fullTempPath, "w", encoding="utf-16") as file:
                    file.write(text)

            # zip all text result in temp directory
            zipObj = ZipFile(output_folder + "Result.zip", 'w')
            for file in os.listdir(tempDir):
                file_extension = "q"+file[:]
                if file_extension[-4:] == '.txt':
                    zipObj.write(os.path.join(tempDir, file), file)

            zipObj.close()
