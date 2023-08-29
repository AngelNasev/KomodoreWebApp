# Komodore Auto Parts KG

### Prerequisites

- Python 3.8
- pip 23.2.1 (or later)

## How To Run
1. Install `virtualenv`:
```
$ pip install virtualenv
```

2. Create a virtual environment:
```
$ virtualenv venv  
```
or
```
$ python -m virtualenv venv
```

3. Activate the virtual environment:
```
$ venv\Scripts\activate
```

4. Then install the dependencies:
```
$ (venv) pip install -r requirements.txt
```

5. Apply Migrations:
```
$ (venv) python manage.py migrate
```

6. Finally start the web server:
```
$ (venv) python manage.py runserver
```

The app should now be running at http://127.0.0.1:8000/.
