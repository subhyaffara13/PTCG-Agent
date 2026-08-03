import re

def conj_physical_impl(self: ComplexTensor) -> ComplexTensor:
    re, im = split_complex_tensor(self)
    return ComplexTensor(re, -im)


def conj_physical_impl(self: ComplexTensor) -> ComplexTensor:
    return aten._conj_physical(self)

