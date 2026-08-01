
def _try_convert_to_tensor(obj):
    try:
        tensor = torch.as_tensor(obj)
    except Exception as e:
        mesg = f"failed to convert {obj} to ndarray. \nInternal error is: {str(e)}."
        raise NotImplementedError(mesg)  # noqa: B904
    return tensor

