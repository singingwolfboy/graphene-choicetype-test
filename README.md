# Graphene ChoiceType test

Setup:

```
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
export FLASK_APP=app.py
flask db create
flask db seed
flask run
```

To manually test, visit http://127.0.0.1:5000/graphql and try to query the
`color` field of a widget. It's not there.

To run automated tests:

```
pytest
```
