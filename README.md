# VACATION MANAGER
Program for managing employees vacation time made in Python using **tkinter** for user graphical interface and **reportlab** for creating
reports in **.pdf** file format.

The main goal of this program is to help maintain the management of employees vacation days in small business. It has easy to use and
clear interface, so the user can easily check, add or modify data. You can also generate reports about chosen person in **.pdf** file 
format if needed. Program is summing and displaying the vacation and sick days in chosen year for all added persons in the database, 
and it's calculating how many vacation days they're left.

**How to build (Windows):**
- you will need following Python extensions: **reportlab**, **Pillow**, **PyInstaller**
- **appdata.bat** script is creating special directroiry in *AppData/Local* for program's config file
- **installer.ps1** script is used to create **.exe** file for Windows from project files
- **arial.ttf**, **arial_bold.ttf**, **logo_ikona.ico**, **logo2.png** files should be placed in the same directory as the **.exe** file
