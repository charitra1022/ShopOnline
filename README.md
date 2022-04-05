# ShopOnline
An E-commerce site

# How to run the project?
## 1. Get the project
*Follow any one of the two methods listed below*
1. Download the **.zip**, and extract it into a folder in your desktop, or,
2. Clone the repo in your desktop.

## 2. Installations
1. Install **Python 3** onto your computer (python_version>=**3.6**)
2. Install **django** by running `pip install django`.

## 3. Running the project
Run the following command in the terminal with project folder as the working directory
`python manage.py runserver`



# Advanced Operations!!
## Note: *Stay away if you don't know what is happening!*

### Changed any field in Database?
python manage.py makemigrations
python manage.py migrate

### Reset Database
python manage.py flush

### Recreate database
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser