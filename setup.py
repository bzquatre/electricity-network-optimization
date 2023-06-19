import PyInstaller.__main__
import os
database= '--add-binary=database.db;.' if os.name=='nt' else '--add-binary=database.db:.'
icon='--add-data=Icon.ico;.' if os.name=='nt' else'--add-data=Icon.ico:.' 
style='--add-data=style.qss;.' if os.name=='nt' else'--add-data=style.qss:.' 
PyInstaller.__main__.run(
    [
        'main.py',
        '--name=Electricity Network Optimization',
        '--windowed',
        '--onedir',
        '--icon=Icon.ico',
        database,
        icon,
        style
    ]
)