
def collection_function_recursion():
    d = {}
    def g():
        return d
    d['g'] = g
    return g

