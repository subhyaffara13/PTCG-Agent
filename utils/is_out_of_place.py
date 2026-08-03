import os

def is_out_of_place(rel_filepath) -> bool:
    if os.path.isabs(rel_filepath):
        raise AssertionError("rel_filepath must be a relative path")
    if rel_filepath.startswith("torch/"):
        return False
    if rel_filepath.startswith("third_party/nvfuser/"):
        return False
    if rel_filepath.startswith("tools/autograd/templates/"):
        return False
    return True

