class User:
    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password

# This is a simple in-memory storage for demo purposes
# In a real application, you would use a database
users = []