from typing import Any

def _getdecoder(
    mode: str, decoder_name: str, args: Any, extra: tuple[Any, ...] = ()
) -> core.ImagingDecoder | ImageFile.PyDecoder:
    # tweak arguments
    if args is None:
        args = ()
    elif not isinstance(args, tuple):
        args = (args,)

    try:
        decoder = DECODERS[decoder_name]
    except KeyError:
        pass
    else:
        return decoder(mode, *args + extra)

    try:
        # get decoder
        decoder = getattr(core, f"{decoder_name}_decoder")
    except AttributeError as e:
        msg = f"decoder {decoder_name} not available"
        raise OSError(msg) from e
    return decoder(mode, *args + extra)

