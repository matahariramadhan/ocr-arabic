from PIL import Image
import pytesseract as pt
import os
      
def main():
    # path for the folder for getting the raw images
    path = input("Enter path folder to convert:")
  
    # path for the folder for getting the output
    tempPath = input("Enter path folder to save:")

    option = "-l ara"
  
    # iterating the images inside the folder
    for imageName in os.listdir(path):

        inputPath = os.path.join(path, imageName)
        img = Image.open(inputPath)
  
        # applying ocr using pytesseract for python
        text = pt.image_to_string(img, config=option)
  
        # for removing the .jpg from the imagePath
        # imagePath = imagePath[0:-4]
  
        imageName = imageName[-7:]

        fullTempPath = os.path.join(tempPath, imageName+".txt")
        print(text)
  
        # saving the  text for every image in a separate .txt file
        file1 = open(fullTempPath, "w", encoding="utf-16")
        file1.write(text)
        file1.close() 
  
if __name__ == '__main__':
    main()