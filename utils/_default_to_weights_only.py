
def _default_to_weights_only(pickle_module):
    is_fbcode = not hasattr(torch.version, "git_version")
    return pickle_module is None and not is_fbcode

