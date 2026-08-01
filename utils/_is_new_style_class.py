
def _is_new_style_class(cls):
    if hasattr(cls, "__class__"):
        return "__dict__" in dir(cls) or hasattr(cls, "__slots__")

