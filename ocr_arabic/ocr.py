import os
import pathlib
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

    def __convert_img_to_txt(self, img_path: str, output_path: str):
        img = Image.open(img_path)

        # convert img to string (arabic) with pytesseract
        text = pt.image_to_string(img, config="-l ara")

        # take 7 last character as imageName exluding .ppm extension
        imageName = img_path.split('-')[-1:][0]
        imageName = imageName[:-4]

        fullTempPath = os.path.join(output_path, imageName+".txt")

        # saving the  text for every image in a separate .txt file
        with open(fullTempPath, "w", encoding='UTF-8') as file:
            file.write(text)

    def convert_to_zip(self, output_folder: str) -> None:
        '''Convert pdf to text and archive the result to Result.zip then store it in output folder'''
        # initialize temorary directory
        with tempfile.TemporaryDirectory() as tempDir:
            # convert pdf to image
            print('Processing...')
            convert_from_path(self.file_path, output_folder=tempDir)

            # iterating the images inside the folder
            for imageName in tqdm(os.listdir(tempDir)):
                self.__convert_img_to_txt(os.path.join(
                    tempDir, imageName), output_path=tempDir)

            # zip all text result in temp directory
            zipObj = ZipFile(output_folder + "Result.zip", 'w')
            for file in os.listdir(tempDir):
                file_extension = "q"+file[:]
                if file_extension[-4:] == '.txt':
                    zipObj.write(os.path.join(tempDir, file), file)

            zipObj.close()

    def convert_to_txt(self, output_folder: str) -> None:
        '''Convert pdf to text and store it in output folder as Result.txt'''
        # initialize temorary directory
        with tempfile.TemporaryDirectory() as tempDir:
            # convert pdf to image
            print('Processing...')
            convert_from_path(self.file_path, output_folder=tempDir)

            # iterating the images inside the folder
            for imageName in tqdm(os.listdir(tempDir)):
                self.__convert_img_to_txt(os.path.join(
                    tempDir, imageName), output_path=tempDir)

            files = []
            for f in os.listdir(tempDir):
                files.append(f)
            files.sort()

            combined_txt = pathlib.Path(output_folder).resolve() / 'Result.txt'
            with combined_txt.open('w', encoding='utf-8') as txt:
                for file in files:
                    file_extension = "q"+file[:]
                    if file_extension[-4:] == '.txt':
                        with pathlib.Path(tempDir+'/'+file).open('r') as f:
                            txt.write(f.read())
