from cscb705_main import *

email = ""

with open("email.txt", "r", encoding="utf8") as file:
    # Read the contents of the file and store it in a variable
    email = file.read()

check_email(email)
