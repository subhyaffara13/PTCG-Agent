
def load_script_module_with_pickled_rref(pickled_script_module):
    f = io.BytesIO(pickled_script_module)
    m = torch.jit.load(f)
    return m()

