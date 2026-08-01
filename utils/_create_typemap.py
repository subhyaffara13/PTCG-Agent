
def _create_typemap():
    import types
    d = dict(list(__builtin__.__dict__.items()) + \
             list(types.__dict__.items())).items()
    for key, value in d:
        if getattr(value, '__module__', None) == 'builtins' \
                and type(value) is type:
            yield key, value
    return

