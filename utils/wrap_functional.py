
def wrap_functional(fn, **kwargs):
    class FunctionalModule(nn.Module):
        def forward(self, *args):
            return fn(*args, **kwargs)
    return FunctionalModule

