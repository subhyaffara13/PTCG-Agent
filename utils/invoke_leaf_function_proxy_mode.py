
def invoke_leaf_function_proxy_mode(proxy_mode, *all_args, **kwargs):
    out = invoke_leaf_function(*all_args, **kwargs)
    proxies = pytree.tree_map(proxy_mode.tracer.unwrap_proxy, all_args)
    proxy = proxy_mode.tracer.create_proxy(
        "call_function", invoke_leaf_function, proxies, kwargs
    )
    return track_tensor_tree(out, proxy, constant=None, tracer=proxy_mode.tracer)

