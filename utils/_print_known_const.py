
def _print_known_const(self, expr):
    known = self.known_constants[expr.__class__.__name__]
    return self._module_format(known)

