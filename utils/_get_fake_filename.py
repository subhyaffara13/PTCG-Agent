
def _get_fake_filename(cls, method_name):
    return os.path.join(FAKE_FILENAME_PREFIX, cls.__name__, method_name)

