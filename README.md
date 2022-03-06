# invoice-api

## Folder structure

- `app.py` - Entrypoint of the application, where all the wiring happens.
- `lib/` - Source folder for the application's modules.
- `database/` - Folder containing database scripts.
* `tests/` - Unit and integration tests for the API.

## Setting up a dev/test environment

### Create a Python virtual environment using Python 3
You'll want a Python virtual environment for running unit tests and running `flask` if you want to deploy the app locally.
* Run `python3 -m venv venv` or `python -m venv venv` if Python 3 is your default Python version.
* Run `source venv/bin/activate`, or if using Windows PowerShell `venv\Scripts\Activate.ps1`
* Run `pip install -r requirements-dev.txt`

## Testing

All tests are defined within the `tests` folder in this project. They can be run with:

```bash
python -m pytest tests
```

## Local deployment

### Start the docker container

```commandline
docker-compose up -d
```

### Deploy Flask locally

The Flask CLI can host a local deployment of your Python application. Use the following command to run your application locally.

```commandline
flask run
```

After running this command, the app will be running at URL http://127.0.0.1:5000/.

## Endpoints

| Method | Path                                    | Function                          |
|--------|-----------------------------------------|-----------------------------------|
| GET    | `/invoices`                             | Get all invoices                  |
| POST   | `/invoices/{invoiceId}`                 | Create a new invoice              |
| GET    | `/invoices/{invoiceId}`                 | Get a specific invoice            |
| GET    | `/invoices/{invoiceId}/items`           | Get all items for a given invoice |
| POST   | `/invoices/{invoiceId}/items`           | Add a new item to a given invoice |
| GET    | `/invoices/{invoiceId}/items/{itemId}`  | Get a specific invoice item       |

You can also import `postman_collection.json` to your Postman with these same endpoints.