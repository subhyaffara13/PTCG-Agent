
def _str(self, *, tensor_contents=None):
    with torch.no_grad(), torch.utils._python_dispatch._disable_current_modes():
        guard = torch._C._DisableFuncTorch()  # noqa: F841
        return _str_intern(self, tensor_contents=tensor_contents)

