
def patch_forward(obj: torch.nn.Module, new_method):
    """Helper method to make it easier to cleanly torch.export() a method on a
    module that is not `forward`.
    """
    # Save the original method
    original_method = obj.forward

    # Patch the method
    obj.forward = new_method.__get__(obj, obj.__class__)

    try:
        yield
    finally:
        # Restore the original method
        obj.forward = original_method

