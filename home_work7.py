clean_folder/
├── clean_folder/
│   ├── clean.py
│   └── __init__.py
└── setup.py



# clean_folder/clean_folder/clean.py
from setuptools import setup
import os
import shutil

# Функція для нормалізації імені файлу


def normalize(name):
    # Реалізуйте транслітерацію та заміну символів
    pass

# Функція для обробки файлів різних типів


def process_file(file_path, destination_folder):
    # Реалізуйте визначення типу файлу за його розширенням та переміщення в відповідну папку
    # Використайте функцію normalize для зміни імені файлу
    pass

# Функція для обробки папки


def process_folder(folder_path):
    for root, _, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            process_file(file_path, folder_path)

# Основна функція


def main(source_folder):
    # Створюємо папку для архівів, якщо її немає
    archives_folder = os.path.join(source_folder, "archives")
    os.makedirs(archives_folder, exist_ok=True)

    # Отримуємо список усіх файлів та папок в зазначеній директорії
    items = os.listdir(source_folder)

    # Обробляємо кожен елемент (файл або папку)
    for item in items:
        item_path = os.path.join(source_folder, item)
        if os.path.isfile(item_path):
            process_file(item_path, source_folder)
        elif os.path.isdir(item_path) and item not in ["archives", "video", "audio", "documents", "images"]:
            process_folder(item_path)


if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        print("Usage: python clean.py /path/to/folder")
        sys.exit(1)

    source_folder = sys.argv[1]

    if not os.path.exists(source_folder):
        print("Source folder does not exist.")
        sys.exit(1)

    main(source_folder)


# clean_folder/setup.py

setup(
    name="clean_folder",
    version="0.1",
    packages=["clean_folder"],
    entry_points={
        "console_scripts": [
            "clean-folder = clean_folder.clean:main"
        ]
    },
)
