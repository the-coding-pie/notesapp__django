Hope you are using python3.4+ and venv.

Also make sure you are using bash terminal, and you are standing now directly inside this root folder - notesapp__django

Now let's do the following:

<!-- MySQL Database Setup -->

## 1. Make a Virtual Environment using venv

`python3 -m venv venv`

## 2. Activate venv

`source venv/bin/activate`

## 3. Setting up MySQL Database

`sudo apt update`

`sudo apt install mysql-server`

`sudo apt install python3-dev libmysqlclient-dev default-libmysqlclient-dev`

## 4. Configuring MySQL

  `sudo mysql_secure_installation`

# 5. Create a Database

  `sudo mysql`

  `CREATE DATABASE your_db_name;`

## 6. Creating User & Granting Privileges

  `CREATE USER 'sammy'@'%' IDENTIFIED WITH mysql_native_password BY 'password';`

  `GRANT ALL ON your_db_name.* TO 'sammy'@'%';`

  `FLUSH PRIVILEGES;`

  `exit`



<!-- Project Setup -->

## 7. Install requirements.txt

  `pip install -r requirements.txt`

## 8. Editing secrets.json file
- Now open "secrets.json" file and provide necessary "correct" informations.

## 9. Run Migrations
- These migrations will create corresponding "Tables" on your DB.
    
  `python manage.py makemigrations`

  `python manage.py makemigrations notes`

  `python manage.py migrate`
  
  `python manage.py collectstatic`

## 10. Running Django Development Server

  `python manage.py runserver --your_ip_address:8000`
    
    - Then visit your http://your_ip_address:8000