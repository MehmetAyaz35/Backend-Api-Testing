# Api-Testing

This Python Flask application provides a simple yet powerful framework for managing product data using RESTful APIs. It is designed with Pydantic schemas to ensure data integrity and includes comprehensive testing scripts to validate all functionalities. Ideal for developers and small teams looking to implement or learn about product management systems, this project serves as an excellent base for expanding into more complex web applications or as a teaching tool for those new to Flask and API development..

## Files
- **app.py**: Contains the main Flask application.
- **schemas.py**: Defines model schemas using Pydantic.
- **test_products.py**: Includes test scenarios for products.
- **.gitignore**: Lists files to be ignored by Git.
- **requirements.txt**: Lists external dependencies used in the project (Flask, Pydantic, pytest).

## Installation
To set up and run the project locally, follow these steps:

### Install the requirements
```bash
pip install -r requirements.txt
```

Start the application with debugging enabled
```bash
python -m flask run --debug
```

## Testing
To run the unit tests using pytest:
```bash
pytest test_products.py
```

## Contributing
If you would like to contribute to the project, please ensure to run your tests and verify everything passes before submitting a pull request. Feel free to fork the repository and send a pull request with your suggested changes.

