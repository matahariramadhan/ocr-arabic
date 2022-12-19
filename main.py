import sys
import os
import tempfile
from PIL import Image
import pytesseract as pt
from pdf2image import convert_from_path
from zipfile import ZipFile


def get_user_input(message: str, error_message='Please provide the asked input') -> str:
    '''
    Get user input and prevent user to leave it blank
    '''
    user_input = ""

    while user_input == "":
        user_input = input(message)

        # prevent user to leave the input blank
        if user_input == "":
            print(error_message, end=", ")
            exit = input(
                'wanna exit?(y/N): ')
            if exit == "y" or exit == "Y":
                sys.exit('Exiting the program')

    return user_input


def main():
    print('Welcome to Arabic OCR by Matahari Ramadhan!')
    print('You can convert your arabic pdf file to txt easily\n')

    pdf_path = get_user_input(
        "Enter full path of file you want to convert: ", "Please enter full path of file you want to convert")
    result_path = get_user_input(
        "Enter the path to save the result: ", "Please enter the path to save the result")

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
            imageName = imageName.split('-')[-1:][0]
            imageName = imageName[:-4]

            fullTempPath = os.path.join(tempDir, imageName+".txt")

            # saving the  text for every image in a separate .txt file
            with open(fullTempPath, "w", encoding="utf-16") as file:
                file.write(text)

        # zip all text result in temp directory
        zipObj = ZipFile(result_path + "Result.zip", 'w')
        for file in os.listdir(tempDir):
            file_extension = "q"+file[:]
            if file_extension[-4:] == '.txt':
                zipObj.write(os.path.join(tempDir, file), file)

        zipObj.close()

    print('Done! Your text is ready now')


if __name__ == '__main__':
    main()
