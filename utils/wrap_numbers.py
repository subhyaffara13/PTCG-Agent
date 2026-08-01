
def wrap_numbers(input_dict, name):
    """Given an `input_dict` and a function `name`, adjust the numbers
    which "wrap" (restart from zero) across different calls by adding
    "old value" to "new value" and return an updated dict.
    """
    with _wn.lock:
        return _wn.run(input_dict, name)

