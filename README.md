#Bunq Budget
Bunq budget is a - self hosted - web app to keep track of your finances!

This app uses the uses the official [Bunq Python SDK](https://github.com/bunq/sdk_python) to get the data. [Stisla](https://getstisla.com/) is being used as a front-end. 

> **_NOTE:_** This app will **ONLY** use GET requests, this app wil never talk to a endpoint of the Bunq API using PATCH, POST, PUT or DELETE.

##Installing
> **_NOTE:_** This app is still in early stage and in heavy development. Therefor there is only a guide to install a development environment.
```console
# Clone using SSH
git clone git@github.com:haijeploeg/bunq-budget.git
# OR clone using HTTPS
https://github.com/haijeploeg/bunq-budget.git

# Change directories and create a virtualenv
cd bunq-budget
python3 -m venv env
source env/bin/activate

# Install the requirements
pip install -r requirements.txt

# Run migrations
python3 manage.py migrate

# Start the development server
python3 manage.py runserver
```

## Things that work
- [x] Register
- [x] Login
- [x] Settings page
- [x] Overview page of accounts
- [x] Choose which accounts to use in the app

Only dutch is still supported, english is coming soon...