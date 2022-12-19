import sys
from ocr import OCR


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

    ocr = OCR()
    ocr.convert_file_to_zip(file_path=pdf_path, output_folder=result_path)

    print('Done! Your text is ready now')


if __name__ == '__main__':
    main()
