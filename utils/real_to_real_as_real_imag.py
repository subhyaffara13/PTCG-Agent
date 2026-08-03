import re

def real_to_real_as_real_imag(self, deep=True, **hints):
    if self.args[0].is_extended_real:
        if deep:
            hints['complex'] = False
            return (self.expand(deep, **hints), S.Zero)
        else:
            return (self, S.Zero)
    if deep:
        x, y = self.args[0].expand(deep, **hints).as_real_imag()
    else:
        x, y = self.args[0].as_real_imag()
    re = (self.func(x + I*y) + self.func(x - I*y))/2
    im = (self.func(x + I*y) - self.func(x - I*y))/(2*I)
    return (re, im)

