
def udf_with_torch_ops(device=-1, use_record_function=False):
    device_ctx = contextlib.nullcontext() if device == -1 else torch.cuda.device(device)
    record_function_ctx = (
        torch.autograd.profiler.record_function("##forward##")
        if use_record_function
        else contextlib.nullcontext()
    )
    with device_ctx, record_function_ctx:
        t1, t2 = torch.ones(1), torch.ones(1)
        t = torch.add(t1, t2)
        t = torch.mul(t, t)
        t = t.relu()
        t = t.sigmoid()

