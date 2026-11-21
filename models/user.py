class User:
    """A person who can log in: an admin or a coordinator."""

    def __init__(self, user_id, username, full_name, role):
        self.user_id = user_id
        self.username = username
        self.full_name = full_name
        self.role = role

    def is_admin(self):
        return self.role == "admin"
