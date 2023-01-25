from users import *
import secrets

user1 = User(
    input("Please enter your first name. "),
    input("Please enter your last name. "),
    "",
    secrets.randbelow(10000000),
    input("Please enter your email address. "),
)

user1 = User(
    user1.first_name,
    user1.last_name,
    user1.first_name + "." + user1.last_name,
    user1.id,
    user1.email_address,
)

print(user1.first_name, user1.last_name, user1.username, user1.id, user1.email_address)
