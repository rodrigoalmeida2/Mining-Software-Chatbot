import os
import shutil
import chardet


def convert_to_txt(file_path, txt_path):
    try:
        with open(file_path, 'rb') as f:
            result = chardet.detect(f.read())

        # If the confidence is less than 0.5, it's probably not text
        if result['confidence'] < 0.5:
            print(f"Deleting unreadable file: {file_path}")
            os.remove(file_path)
            return

        # Copy the contents of the original file to the txt file
        shutil.copyfile(file_path, txt_path)
        os.remove(file_path)

    except Exception as e:
        print(f"Error processing file {file_path}: {e}")
        return


def find_and_convert_in_dir(dir_path):
    for root, _, files in os.walk(dir_path):
        for file in files:
            if file.endswith(".txt"):
                continue

            file_path = os.path.join(root, file)
            base = os.path.splitext(file_path)[0]
            txt_path = base + '.txt'
            if not os.path.exists(txt_path):
                convert_to_txt(file_path, txt_path)
