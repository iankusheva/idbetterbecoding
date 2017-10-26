import os
import subprocess


def setup():
    print("basic setup")


def teardown():
    path_to_db = '/home/irina/Documents/pythonic_stuff/idbetterbecoding/dp_app/test_db.db'
    if os.path.exists(path_to_db):
        os.remove(path_to_db)


def test_database():
    print("testing db")
    cmd = "python3.5 /home/irina/Documents/pythonic_stuff/idbetterbecoding/run_cli.py add_book --json_file=result.json --dbname=test_db.db"
    code = subprocess.call(cmd, shell=True)