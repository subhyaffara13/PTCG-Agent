
def deepcopy_to_fake_tensor(
    obj: Any, fake_mode: torch._subclasses.fake_tensor.FakeTensorMode
) -> Any:
    with torch._subclasses.fake_tensor.FakeCopyMode(fake_mode):
        return wrap_fake_exception(lambda: copy.deepcopy(obj))

