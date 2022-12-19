import sys
import os
import tempfile
from PIL import Image
import pytesseract as pt
from pdf2image import convert_from_path
from zipfile import ZipFile


def main():
    pdf_path = ""
    result_path = ""

    # Asking path to pdf that want to be converted
    while pdf_path == "":
        pdf_path = input("Enter full path to pdf: ")
        if pdf_path == "":
            exit = input(
                'Please enter the full path of pdf!, wanna exit?(y/N): ')
            if exit == "y" or exit == "Y":
                print('Exiting!')
                sys.exit()

    # Asking path to save the result
    while result_path == "":
        result_path = input("Enter the path to save the result: ")
        if result_path == "":
            exit = input(
                'Please enter the full path to save the result!, wanna exit?(y/N): ')
            if exit == "y" or exit == "Y":
                print('Exiting!')
                sys.exit()

    # initialize temorary directory
    with tempfile.TemporaryDirectory() as tempDir:
        # convert pdf to image
        convert_from_path(pdf_path, output_folder=tempDir)

        # iterating the images inside the folder
        for imageName in os.listdir(tempDir):
            img = Image.open(os.path.join(tempDir, imageName))

            # convert img to string (arabic) with pytesseract
            text = pt.image_to_string(img, config="-l ara")

            # take 7 last character as imageName exluding .ppm extension
            imageName = imageName[-7:-4]

            fullTempPath = os.path.join(tempDir, imageName+".txt")

            # saving the  text for every image in a separate .txt file
            with open(fullTempPath, "w", encoding="utf-16") as file:
                file.write(text)

        # zip all text result in temp directory
        zipObj = ZipFile(result_path + "Result.zip", 'w')
        for file in os.listdir(tempDir):
            file_extension = "q"+file[:]
            if file_extension[-4:] == '.txt':
                zipObj.write(os.path.join(tempDir, file))

        zipObj.close()

    print('Done! Your text is ready now')


if __name__ == '__main__':
    main()
