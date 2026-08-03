from typing import Any

def _getencoder(
    mode: str, encoder_name: str, args: Any, extra: tuple[Any, ...] = ()
) -> core.ImagingEncoder | ImageFile.PyEncoder:
    # tweak arguments
    if args is None:
        args = ()
    elif not isinstance(args, tuple):
        args = (args,)

    try:
        encoder = ENCODERS[encoder_name]
    except KeyError:
        pass
    else:
        return encoder(mode, *args + extra)

    try:
        # get encoder
        encoder = getattr(core, f"{encoder_name}_encoder")
    except AttributeError as e:
        msg = f"encoder {encoder_name} not available"
        raise OSError(msg) from e
    return encoder(mode, *args + extra)

