
def intlike(n):
    try:
        as_int(n, strict=False)
        return True
    except ValueError:
        return False

