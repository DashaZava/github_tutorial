import os
import shutil
import zipfile

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

    if ext in ['JPEG', 'PNG', 'JPG', 'SVG']:
        dest_folder = os.path.join(destination_folder, 'images')
    elif ext in ['AVI', 'MP4', 'MOV', 'MKV']:
        dest_folder = os.path.join(destination_folder, 'video')
    elif ext in ['DOC', 'DOCX', 'TXT', 'PDF', 'XLSX', 'PPTX']:
        dest_folder = os.path.join(destination_folder, 'documents')
    elif ext in ['MP3', 'OGG', 'WAV', 'AMR']:
        dest_folder = os.path.join(destination_folder, 'audio')
    elif ext in ['ZIP', 'GZ', 'TAR']:
        dest_folder = os.path.join(destination_folder, 'archives', os.path.splitext(
            os.path.basename(file_path))[0])
        # Розпаковка архіву
        with zipfile.ZipFile(file_path, 'r') as zip_ref:
            zip_ref.extractall(dest_folder)
        return  # Не переміщуємо розпаковані файли
    else:
        dest_folder = os.path.join(destination_folder, 'unknown')

    # Створюємо папку призначення, якщо її немає
    os.makedirs(dest_folder, exist_ok=True)

    # Ім'я файлу після нормалізації
    normalized_file_name = normalize(
        os.path.splitext(os.path.basename(file_path))[0])
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
        elif os.path.isdir(item_path) and item not in ["archives", "video", "audio", "documents", "images"]:
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
