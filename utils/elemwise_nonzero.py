import re

def elemwise_nonzero(self: ComplexTensor) -> torch.Tensor:
    re, im = split_complex_tensor(self)
    return (re != 0) | (im != 0)

