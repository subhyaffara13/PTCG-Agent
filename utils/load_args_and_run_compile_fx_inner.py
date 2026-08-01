
def load_args_and_run_compile_fx_inner(path: str) -> Any:
    from torch._inductor.compile_fx import compile_fx_inner

    with open(path, "rb") as f:
        args, kwargs = pickle.load(f)

    def handle_tensor(x: Any) -> Any:
        if isinstance(x, TensorMetadataHolder):
            return torch._dynamo.testing.rand_strided(
                x.tensor_metadata.shape,
                x.tensor_metadata.stride,
                x.tensor_metadata.dtype,
                x.device,
            )
        else:
            return x

    fake_mode = torch._subclasses.FakeTensorMode(allow_non_fake_inputs=True)
    with fake_mode, config.patch("save_args", False):
        args, kwargs = tree_map(handle_tensor, (args, kwargs))
        return compile_fx_inner(*args, **kwargs)

