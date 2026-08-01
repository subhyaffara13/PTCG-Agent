
def _no_dispatch_record_stream(tensor: torch.Tensor, stream: torch.Stream) -> None:
    # FIXME record_stream doesn't work with non-cuda/mtia/xpu tensors
    if tensor.device.type not in [
        "cuda",
        "mtia",
        "xpu",
        torch._C._get_privateuse1_backend_name(),
    ]:
        return

    if torch.distributed._functional_collectives.is_torchdynamo_compiling():
        return
        # from @ezyang:
        # The no_dispatch was added in https://github.com/pytorch/pytorch/pull/88014 cc @fegin
        # Looking over the PR, it looks like this is because we don't actually support Stream arguments
        # in torch dispatch, so it just chokes.
        # If Dynamo is able to answer "are there any torch dispatch modes" active (it should answer False),
        # a better version of this would just be to check if there are any modes before disabling dispatch.
        # TODO(voz): Extend a dynamo util to answer the above, unify the codepaths here.
        tensor.record_stream(stream)
    else:
        with no_dispatch():
            tensor.record_stream(stream)

