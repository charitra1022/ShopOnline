# ShopOnline
An E-commerce site for shopping hardware online.
Site is live at [this link](https://shoponline-ca.herokuapp.com/)

# How to run the project?
## 1. Get the project
*Follow any one of the two methods listed below*
1. Download the **.zip**, and extract it into a folder in your desktop, or,
2. Clone the repo in your desktop.

## 2. Installations
1. Install **Python 3** onto your computer (python_version>=**3.6**)
2. Install **dependencies** by running `python -m pip install -r requirements.txt`.

## 3. Running the project
Run the following command in the terminal with project folder as the working directory after selecting **master** branch
`python manage.py runserver`

## Active Bugs
1. Username is Case Sensitive.
2. Slow speed of product list auto scroller
3. No word wrap for product description. [Reference](https://shoponline-ca.herokuapp.com/product-detail/12)
4. Green text on card hover. [Reference](https://shoponline-ca.herokuapp.com/ram/)


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