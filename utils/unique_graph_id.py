
def unique_graph_id(proxy_mode, prefix):
    """Returns a unique name and id for a graph to be added to a proxy_mode tracer"""
    # There are probably better ways - I know that create_arg has some self incrementing name
    # magic to it, but since we explicitly have to get the name for register_module,
    # I was not sure how to do that. This kinda simulates it.
    return unique_graph_name_with_root(proxy_mode.tracer.root, prefix)

