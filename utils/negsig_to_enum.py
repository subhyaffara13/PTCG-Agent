
def negsig_to_enum(num):
    """Convert a negative signal value to an enum."""
    try:
        return Negsignal(num)
    except ValueError:
        return num

