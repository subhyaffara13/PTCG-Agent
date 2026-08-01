
def export_tracepoint_fake_tensor_mode(mode, *args, **kwargs):
    with mode:
        return args

