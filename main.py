import sys
import os
import tempfile
from PIL import Image
import pytesseract as pt
from pdf2image import convert_from_path


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

            fullTempPath = os.path.join(result_path, imageName+".txt")

            # saving the  text for every image in a separate .txt file
            file = open(fullTempPath, "w", encoding="utf-16")
            file.write(text)
            file.close()

    print('Done! Your text is ready now')


if __name__ == '__main__':
    main()
