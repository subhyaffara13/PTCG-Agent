
def __ua_function__(method, args, kwargs):
    fn = _implements.get(method)
    return (fn(*args, **kwargs) if fn is not None
            else NotImplemented)

