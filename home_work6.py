import os
import shutil
import zipfile

# Функция для нормализации имени файла


def normalize(name):
    # Транслитерация кириллических символов и замена неподходящих символов на "_"
    normalized_name = []
    for char in name:
        if char.isalpha() or char.isdigit() or char == ' ':
            normalized_name.append(char)
        else:
            normalized_name.append('_')
    return ''.join(normalized_name)

# Функция для обработки файлов разных типов


def process_file(file_path, destination_folder):
    _, ext = os.path.splitext(file_path)
    # Убираем точку из расширения и переводим в верхний регистр
    ext = ext[1:].upper()

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
        # Распаковка архива
        with zipfile.ZipFile(file_path, 'r') as zip_ref:
            zip_ref.extractall(dest_folder)
        return  # Не перемещаем распакованные файлы
    else:
        dest_folder = os.path.join(destination_folder, 'unknown')

    # Создаем папку назначения, если ее нет
    os.makedirs(dest_folder, exist_ok=True)

    # Имя файла после нормализации
    normalized_file_name = normalize(
        os.path.splitext(os.path.basename(file_path))[0])
    new_file_path = os.path.join(dest_folder, f"{normalized_file_name}{ext}")

    # Перемещение файла
    shutil.move(file_path, new_file_path)

# Функция для обработки папки


def process_folder(folder_path):
    for root, _, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            process_file(file_path, folder_path)
        # Удаление пустых папок
        if not os.listdir(root):
            os.rmdir(root)

# Основная функция


def main(source_folder):
    # Создаем папку для архивов, если ее нет
    archives_folder = os.path.join(source_folder, "archives")
    os.makedirs(archives_folder, exist_ok=True)

    # Получаем список всех файлов и папок в указанной директории
    items = os.listdir(source_folder)

    # Обрабатываем каждый элемент (файл или папку)
    for item in items:
        item_path = os.path.join(source_folder, item)
        if os.path.isfile(item_path):
            process_file(item_path, source_folder)
        elif os.path.isdir(item_path) and item not in ["archives", "video", "audio", "documents", "images"]:
            process_folder(item_path)


# Если скрипт запущен как отдельный файл
if __name__ == "__main__":
    import sys

    # Проверяем количество аргументов командной строки
    if len(sys.argv) != 2:
        print("Usage: python sort.py /path/to/folder")
        sys.exit(1)

    source_folder = sys.argv[1]

    # Проверяем, существует ли указанная папка
    if not os.path.exists(source_folder):
        print("Source folder does not exist.")
        sys.exit(1)

    main(source_folder)
