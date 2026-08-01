
def make_func(param_string, raise_if_called=True):
    if not param_string.startswith('('):
        param_string = '(%s)' % param_string
    if raise_if_called:
        body = 'raise ValueError("function should not be called")'
    else:
        body = 'return True'
    d = {}
    exec(f'def func{param_string}:\n    {body}', globals(), d)
    return d['func']

