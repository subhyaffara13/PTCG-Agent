
def is_string_or_list_of_strings(val):
    return (isinstance(val, str) or
            (isinstance(val, list) and val and
             builtins.all(isinstance(s, str) for s in val)))

