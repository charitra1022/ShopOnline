# ShopOnline

An E-commerce site designed in **Django** for shopping hardware online.
Site is live at [this link](https://shoponline-ca.herokuapp.com/)

This is a college project and not any actual e-commerce website!


<br/><hr/><br/>


## Table of Contents
1. [How to run Project](#how-to-run-the-project)
2. [Running Tests](#running-tests)
3. [Active Bugs](#active-bugs)
4. [Advanced Database Operation](#advanced-database-operations)


<br/><hr/><br/>



## How to run the project?

### 1. Get the project

    **Follow any one of the two methods listed below**
    

  * Download the **.zip** of **master** branch, and extract it into a folder in your desktop, *__or__*,

  * Clone the **master** branch in your desktop.


<br/>

### 2. Installations

1. Install **Python 3** onto your computer (_python_version_>=**3.6**)
2. Install **dependencies** by running :-

    ```
    python -m pip install -r requirements.txt
    ```

<br/>


### 3. Running the project

Run the following command in the terminal with __project__ folder as the working directory.

  ```
  python manage.py runserver
  ```

<br/><hr/><br/>

## Environment Variables required
1. `ALLOWED_HOSTS` : Space separated domain names in **settings.py**.<br> Ex: `localhost 127.0.0.1 .onrender.com`
2. `SECRET_KEY` : Django app secret key in **settings.py**.
3. `DEBUG` : App debug mode in **settings.py**. set `true` for debug mode (optional).
4. `PAYPAL-CLIENTID` : for paypal integration.
5. `ADMIN_EMAIL` : admin email for sending mails to customer
6. `DATABASE_URL` : db url for externally connected databases (optional).

<br/><hr/><br/>



## Running Tests

To run tests, run the following command into the terminal:

```
  coverage run manage.py test app -v 2
  coverage html
```

To see the output, go to `htmlcov` folder and run the `index.html` file. 

Click any links in that page to see the test efficiency.

<br/><hr/><br/>

## Active Bugs

Refer to [BUGS.md](/BUGS.md) for better view on Active Bugs


<br/><hr/><br/>


## Advanced Database Operations

_**Note: Stay away if you don't know what is happening!**_

### Current admin details
route: `/admin`
username: `admin`
password: `admin`

### Changed any field in Database?

```
  python manage.py makemigrations
  python manage.py migrate
```

### Reset Database

```
  python manage.py flush
```

### Recreate database

```
  python manage.py makemigrations
  python manage.py migrate
  python manage.py createsuperuser
```

<br/><hr/><br/>