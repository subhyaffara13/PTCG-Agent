
def copy_tensors(src: Sequence[OrtValue], dst: Sequence[OrtValue], stream=None) -> None:
    """
    Copy tensor data from source OrtValue sequence to destination OrtValue sequence.
    """
    c_sources = [s._get_c_value() for s in src]
    c_dsts = [d._get_c_value() for d in dst]
    C.copy_tensors(c_sources, c_dsts, stream)

