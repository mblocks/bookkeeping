# bookkeeping

## Run

```bash

pipenv shell
pipenv install
uvicorn app.main:app --reload

```
## Generate Requirement

```sh
pipenv lock -r > requirements.txt
```
