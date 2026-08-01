
def custom_dialect():
    dialect_name = "weird"
    dialect_kwargs = {
        "doublequote": False,
        "escapechar": "~",
        "delimiter": ":",
        "skipinitialspace": False,
        "quotechar": "`",
        "quoting": 3,
    }
    return dialect_name, dialect_kwargs

