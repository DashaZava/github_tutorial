import os
import shutil
import zipfile

# Словник з дозволеними розширеннями та відповідними папками
valid_extensions = {
    'images': ['JPEG', 'PNG', 'JPG', 'SVG'],
    'video': ['AVI', 'MP4', 'MOV', 'MKV'],
    'documents': ['DOC', 'DOCX', 'TXT', 'PDF', 'XLSX', 'PPTX'],
    'audio': ['MP3', 'OGG', 'WAV', 'AMR'],
    'archives': ['ZIP', 'GZ', 'TAR']
}

# Функція для нормалізації імені файлу
def normalize(name):
    normalized_name = []
    for char in name:
        if char.isalpha() or char.isdigit() or char == ' ':
            normalized_name.append(char)
        else:
            normalized_name.append('_')
    return ''.join(normalized_name)

# Функція для обробки файлів різних типів
def process_file(file_path, destination_folder):
    _, ext = os.path.splitext(file_path)
    ext = ext[1:].upper()  # Видаляємо точку з розширення і переводимо в верхній регістр

    dest_folder = None
    for folder, extensions in valid_extensions.items():
        if ext in extensions:
            dest_folder = os.path.join(destination_folder, folder)
            break

    if dest_folder is None:
        dest_folder = os.path.join(destination_folder, 'unknown')

    # Створюємо папку призначення, якщо її немає
    os.makedirs(dest_folder, exist_ok=True)

    # Ім'я файлу після нормалізації
    normalized_file_name = normalize(os.path.splitext(os.path.basename(file_path))[0])
    new_file_path = os.path.join(dest_folder, f"{normalized_file_name}{ext}")

    # Переміщення файлу
    shutil.move(file_path, new_file_path)

# Функція для обробки папки
def process_folder(folder_path):
    for root, _, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            process_file(file_path, folder_path)

        # Видалення порожніх папок
        if not os.listdir(root):
            os.rmdir(root)

# Основна функція
def main(source_folder):
    # Створюємо папку для архівів, якщо її немає
    archives_folder = os.path.join(source_folder, "archives")
    os.makedirs(archives_folder, exist_ok=True)

    # Отримуємо список всіх файлів і папок у вказаній директорії
    items = os.listdir(source_folder)

    # Обробляємо кожен елемент (файл або папку)
    for item in items:
        item_path = os.path.join(source_folder, item)
        if os.path.isfile(item_path):
            process_file(item_path, source_folder)
        elif os.path.isdir(item_path) and item not in valid_extensions.keys() and item != "archives":
            process_folder(item_path)

if __name__ == "__main__":
    import sys

    # Перевіряємо кількість аргументів командного рядка
    if len(sys.argv) != 2:
        print("Usage: python sort.py /path/to/folder")
        sys.exit(1)

    source_folder = sys.argv[1]

    # Перевіряємо, чи існує вказана папка
    if not os.path.exists(source_folder):
        print("Source folder does not exist.")
        sys.exit(1)

    main(source_folder)
