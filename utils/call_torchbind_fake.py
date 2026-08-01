
def call_torchbind_fake(mode, *args, **kwargs):
    with mode:
        out = call_torchbind_impl(*args, **kwargs)
        return pytree.tree_map_only(
            torch.Tensor,
            lambda x: mode.from_tensor(x, static_shapes=True)
            if not isinstance(x, torch._subclasses.fake_tensor.FakeTensor)
            else x,
            out,
        )

