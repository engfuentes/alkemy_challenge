## Steps to set up the environment of the project

### Step 1 - Create and set up a virtual environment with venv
1.1 Go to the project's directoy. Right click and open the terminal.
1.2 Write the following code into the terminal:

    python -m venv my_venv

This created a virtual environment named my_venv.  

1.3 To activate the environment type into the terminal:

    my_venv/Scripts/activate.bat

1.4 To install the required libraries type:

    python -m pip install -r requirements.txt

### Step 2 - Setup the PostgreSQL database
2.1 Donwnload and install PostgreSQL from https://www.postgresql.org/download/
2.2 Create a `.env` empty file. Type into the terminal

    type NUL > .env

2.3 Open `.env` file and copy the following code, replacing *database_name* with the name that you desire for the db and *database_password* with the password that you chose when you installed PostgreSQL. Save the `.env` file.

    DATABASE_NAME=database_name
    DATABASE_PASSWORD=database_password

### Step 3 - Run the `main.py` file to get the data into the SQL database
3.1 Open the terminal and type:

    python main.py