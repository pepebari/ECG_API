# ECG_API
API to store ECG data and extract some insights

## How to run 

Create a virtual environement and install the required packages

`python3 -m venv .venv`
`source .venv/bin/activate`

`pip install -r requirements.txt`

Start the server using uvicorn

`uvicorn app.main:app`

## Load some data

There are some real ECG data extracted from [here](https://www.nature.com/articles/s41597-020-0386-x#Sec9) that can be uploaded using the following script

`cd app/test`

`python3 populateDatabase.py`
