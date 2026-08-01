
def is_valid_python(text):
    try:
        ast.parse(text)
        return True
    except SyntaxError:
        return False

