
def _recursive_script_module_receiver(
    recursive_script_module_serialized,
):
    """Deserializes a RecursiveScriptModule that does not contain a script RemoteModule."""
    f = io.BytesIO(recursive_script_module_serialized)
    m = torch.jit.load(f)
    return m

