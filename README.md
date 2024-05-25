Files
app.py: Contains the main Flask application.
schemas.py: Defines model schemas using Pydantic.
test_products.py: Includes test scenarios for products.
.gitignore: Lists files to be ignored by Git.
requirements.txt: Lists external dependencies used in the project (Flask, Pydantic, pytest).
Installation
To set up and run the project locally, follow these steps:

Install the requirements:
pip install -r requirements.txt

Start the application with debugging enabled:
python -m flask run --debug

Testing
To run the unit tests using pytest:
pytest test_products.py

Contributing
If you would like to contribute to the project, please ensure to run your tests and verify everything passes before submitting a pull request.
