
def standardise_name(name):
    "Standardises a property or value name."
    try:
        return numeric_to_rational("".join(name))
    except (ValueError, ZeroDivisionError):
        return "".join(ch for ch in name if ch not in "_- ").upper()

