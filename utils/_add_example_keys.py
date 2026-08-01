
def _add_example_keys(func):
    def inner():
        solver=func()
        examples=[]
        for example in solver['examples']:
            temp={
                'eq': solver['examples'][example]['eq'],
                'sol': solver['examples'][example]['sol'],
                'XFAIL': solver['examples'][example].get('XFAIL', []),
                'func': solver['examples'][example].get('func',solver['func']),
                'example_name': example,
                'slow': solver['examples'][example].get('slow', False),
                'simplify_flag':solver['examples'][example].get('simplify_flag',True),
                'checkodesol_XFAIL': solver['examples'][example].get('checkodesol_XFAIL', False),
                'dsolve_too_slow':solver['examples'][example].get('dsolve_too_slow',False),
                'checkodesol_too_slow':solver['examples'][example].get('checkodesol_too_slow',False),
                'hint': solver['hint']
            }
            examples.append(temp)
        return examples
    return inner()

