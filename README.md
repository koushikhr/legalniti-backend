# Legalniti Backend Django

This is an initial Django boilerplate for backend.

## Getting started with this boilerplate:
##### (Open your IDE (VS-Code [OR] PyCharm) follow these steps)

1. Create a project root directory in your local machine
```bash
mkdir <project_name> 
```
2. Clone the project in this <project_name> directory (you can use ssh also)
```bash
cd <project_name>
git clone https://github.com/legalnitiai6690/backend.git && cd backend/
```
3. Create a Virtual python environment.
```bash
python3 -m venv venv
```
4. Activate Virtual Environment in terminal.
```bash
source venv/bin/activate
```
5. Create your virtual environment, activate that environment and install all the requirements
```bash
pip install -r requirements.txt
```
6. Remember `<project_name>/backend` is the directory name from where you will run the server.

## Folder Structure
```
<project_name>
|
|---assets (folder created once static files are collected)
|
|---django_project
|   |---apps
|   |   |---core (custom app)
|   |   |---...<other apps>...
|   |   |---urls.py
|   |
|   |---config
|   |   |---settings
|   |   |   |---base.py
|   |   |   |---env.py (ignored by git)
|   |   |   |---development.py
|   |   |
|   |   |---asgi.py
|   |   |---urls.py
|   |   |---wsgi.py
|   |   |
|   |   |static_files (all static files we use in development)
|   |   |---base (project as a whole specific static files)
|   |   |   |---css
|   |   |   |---img
|   |   |   |---js
|   |   |---core (my custom app specific)
|   |   |   |---css
|   |   |   |---img
|   |   |   |---js
|   |   |
|   |---templates
|   |   |---core (custom app specific)
|   |   |---<other app specific templates>
|   |   |---base.html (included basics of jquery and bootstrap)
|   |
|   |---.gitignore
|   |---manage.py
|   |---requirements.txt
|
|---media (folder created once items were uploaded)
|---db.sqlite3
```
