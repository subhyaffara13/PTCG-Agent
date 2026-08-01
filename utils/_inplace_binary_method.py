
def _inplace_binary_method(ufunc, name):
    """Implement an in-place binary method with a ufunc, e.g., __iadd__."""
    def func(self, other):
        return ufunc(self, other, out=(self,))
    func.__name__ = f'__i{name}__'
    return func

