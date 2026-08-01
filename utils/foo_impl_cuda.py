
def foo_impl_cuda(x, z):
    x.add_(5)
    z.add_(5)
    return x.clone(), z.clone(), x + z

