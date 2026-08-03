import os

def get_username() -> str:
    """Returns the username of the current user."""
    if platform.system() == "Windows":
        return os.getlogin()
    else:
        return pwd.getpwuid(os.getuid()).pw_name

