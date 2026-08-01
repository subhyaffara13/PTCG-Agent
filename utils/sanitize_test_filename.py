
def sanitize_test_filename(filename):
    strip_py = re.sub(r'.py$', '', filename)
    return re.sub('/', r'.', strip_py)

