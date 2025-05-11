to use firstly 
enter virtual venv using .\asn_venv\Scripts\activate
then use python -r requirements.txt install
then do not forget to install postgresql on your computer and use
CREATE DATABASE asn_shop;
CREATE USER admin WITH PASSWORD 'admin';
GRANT ALL PRIVILEGES ON DATABASE asn_shop TO admin;
if not working search in windows tab "pg admin" tap on databases and change owner of asn_shop to admin
everything must be fine after that
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
than you can go to http://127.0.0.1:8000/admin/ and see database 

