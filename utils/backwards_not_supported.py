
def backwards_not_supported(prim):
    def redispatch_prim(args, kwargs):
        with torch._C._AutoDispatchBelowAutograd():
            return prim(*args, **kwargs)

    class BackwardsNotSupported(torch.autograd.Function):
        @staticmethod
        # pyrefly: ignore [bad-override]
        def forward(ctx, args_spec, *flat_args):
            args, kwargs = tree_unflatten(flat_args, args_spec)  # type: ignore[arg-type]
            return redispatch_prim(args, kwargs)

        @staticmethod
        def backward(ctx, *args):
            raise RuntimeError("backwards not supported on prim")

    @wraps(prim)
    def _autograd_impl(*args, **kwargs):
        flat_args, args_spec = tree_flatten((args, kwargs))
        if torch.is_grad_enabled() and any(
            a.requires_grad for a in flat_args if isinstance(a, torch.Tensor)
        ):
            # TODO: There is a subtle bug here: prims like copy_to
            # return their input argument after mutating it; and custom
            # autograd function will incorrectly turn the result into
            # a view which will fail test_python_ref_executor tests.
            # At the moment, we sidestep this by observing that the
            # unit tests don't ever try to run the executor with
            # autograd, so we don't exercise the buggy case, but if
            # you ever want to feed autograd through this, be aware
            # of it!  We need a way of properly implementing autograd
            # for mutating operations in Python to do this.
            return BackwardsNotSupported.apply(args_spec, *flat_args)
        else:
            return redispatch_prim(args, kwargs)

    return _autograd_impl

