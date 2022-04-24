# ShopOnline

An E-commerce site for shopping hardware online.
Site is live at [this link](https://shoponline-ca.herokuapp.com/)

## How to run the project?

### 1. Get the project

**Follow any one of the two methods listed below**

1. Download the **.zip** of master branch, and extract it into a folder in your desktop, or,
2. Clone the master branch repo in your desktop.

### 2. Installations

1. Install **Python 3** onto your computer (python_version>=**3.6**)
2. Install **dependencies** by running

`python -m pip install -r requirements.txt`.

### 3. Running the project

Run the following command in the terminal with project folder as the working directory

`python manage.py runserver`

## Active Bugs

Refer to [BUGS.md](/BUGS.md) for better view on Active Bugs

## Advanced Operations

### Note: *Stay away if you don't know what is happening!*

### Changed any field in Database?

python manage.py makemigrations
python manage.py migrate

### Reset Database

python manage.py flush

### Recreate database

python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
