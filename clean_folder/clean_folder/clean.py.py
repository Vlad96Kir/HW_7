import os
import shutil
import sys
from pyunpack import Archive
import patoolib

CATEGORIES = {
    'images': ['JPEG', 'PNG', 'JPG', 'SVG'],
    'videos': ['AVI', 'MP4', 'MOV', 'MKV'],
    'documents': ['DOC', 'DOCX', 'TXT', 'PDF', 'XLSX', 'PPTX'],
    'audio': ['MP3', 'OGG', 'WAV', 'AMR'],
    'archives': ['ZIP', 'GZ', 'TAR', 'RAR']
}

unknown_extensions = []
known_extensions = []


def create_category_folders(folder_path):
    for category in CATEGORIES.keys():
        category_folder = os.path.join(folder_path, category)
        if not os.path.exists(category_folder):
            os.makedirs(category_folder)


def process_folder(folder_path):
    global known_extensions
    global unknown_extensions

    for root, _, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            _, extension = os.path.splitext(file_path)
            extension = extension.upper()[1:] if extension else ''

            known_category = None
            for category, extensions in CATEGORIES.items():
                if extension in extensions:
                    known_category = category
                    break

            if known_category:
                known_extensions.append(extension)
                new_file_name = file if '.' in file else file + extension
                new_file_path = os.path.join(folder_path, known_category, new_file_name)
                os.makedirs(os.path.dirname(new_file_path), exist_ok=True)
                shutil.move(file_path, new_file_path)
            else:
                unknown_extensions.append(extension)
                shutil.move(file_path, os.path.join(folder_path, file))

    # Remove empty directories
    for root, dirs, _ in os.walk(folder_path, topdown=False):
        for dir in dirs:
            dir_path = os.path.join(root, dir)
            if not os.listdir(dir_path):
                shutil.rmtree(dir_path)


def extract_archives(folder_path):
    for root, _, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            _, extension = os.path.splitext(file_path)
            extension = extension.upper()[1:] if extension else ''
            if extension in ['ZIP', 'RAR']:
                destination_folder = os.path.join(root, os.path.splitext(file)[0])
                os.makedirs(destination_folder, exist_ok=True)
                try:
                    if extension == 'ZIP':
                        Archive(file_path).extractall(destination_folder)
                    elif extension == 'RAR':
                        patoolib.extract_archive(file_path, outdir=destination_folder)
                    if os.path.isfile(file_path):
                        os.remove(file_path)
                    elif os.path.isdir(file_path):
                        shutil.rmtree(file_path)

                except Exception as e:
                    print(f"Error extracting archive '{file}': {str(e)}")


def main():
    try:
        target_folder = sys.argv[1]
    except IndexError:
        print("No path to folder")
        sys.exit(-1)

    create_category_folders(target_folder)
    process_folder(target_folder)
    extract_archives(target_folder)

    print('--- Files in Each Category ---')
    for category in CATEGORIES.keys():
        category_path = os.path.join(target_folder, category)
        if os.path.exists(category_path):
            files = os.listdir(category_path)
            print(f'{category}: {", ".join(files)}')

    print('--- Known Extensions ---')
    print(', '.join(set(known_extensions)))

    print('--- Unknown Extensions ---')
    print(', '.join(set(unknown_extensions)))


if __name__ == '__main__':
    main()
