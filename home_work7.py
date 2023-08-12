clean_folder/
│
├── clean_folder/
│   ├── clean.py
│   └── __init__.py
│
└── setup.py

from setuptools import setup

setup(
    name='clean_folder',
    version='1.0',
    packages=['clean_folder'],
    entry_points={
        'console_scripts': [
            'clean-folder = clean_folder.clean:main'
        ]
    },
    install_requires=[
        # Ось можна перерахувати будь-які залежності, якщо є
    ],
)

 # Після створення цих файлів ми можете встановити свій пакет за допомогою команди:
pip install -e .
