import os
START_SEQUENSE = "\033[90m "
END_SEQUENSE = "\033[0m"

def log(text):
    if os.getenv("DEBUG") =="True":
        print(f"  {START_SEQUENSE}{text}{END_SEQUENSE}")