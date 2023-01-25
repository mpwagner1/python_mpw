import secrets


class User:
    def __init__(self, first_name, last_name, username, email_address, id):
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.id = id
        self.email_address = email_address

    def get_firstname(self):
        return self.first_name

    def get_lastname(self):
        return self.last_name

    def get_username(self):
        return self.username

    def get_id(self):
        return self.id

    def get_email_address(self):
        return self.email_address
