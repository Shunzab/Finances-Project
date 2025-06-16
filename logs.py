from datetime import datetime 
import pandas as pd

class log: # A class to handle logging operations.
    @staticmethod
    def log_in():
        # Log ins to finances.
        with open('login.txt', 'a') as login:
            login.write(f"{datetime.now()}\n")

        print(f"Logged in at {datetime.now()}")
        print(f"Last login at : {pd.read_csv('login.txt').tail(1).to_string(index=False)}") # Although it fetches it from a text file, I had to use "pd.read_csv()" 

    @staticmethod
    def log_out():
        # Log outs from finances.
        with open('logout.txt', 'a') as logout:
            logout.write(f"{datetime.now()}\n")

        print(f"Logged out at {datetime.now()}")


