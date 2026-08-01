
def map_proxy_torch_dispatch_mode(mode, f, xs, args):
    return trace_map(mode, map_impl, f, xs, args)

