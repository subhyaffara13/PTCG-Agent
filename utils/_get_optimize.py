from typing import Any

def _get_optimize(im: Image.Image, info: dict[str, Any]) -> list[int] | None:
    """
    Palette optimization is a potentially expensive operation.

    This function determines if the palette should be optimized using
    some heuristics, then returns the list of palette entries in use.

    :param im: Image object
    :param info: encoderinfo
    :returns: list of indexes of palette entries in use, or None
    """
    if (
        im.mode in ("P", "L")
        and info
        and info.get("optimize")
        and im.width != 0
        and im.height != 0
    ):
        # Potentially expensive operation.

        # The palette saves 3 bytes per color not used, but palette
        # lengths are restricted to 3*(2**N) bytes. Max saving would
        # be 768 -> 6 bytes if we went all the way down to 2 colors.
        # * If we're over 128 colors, we can't save any space.
        # * If there aren't any holes, it's not worth collapsing.
        # * If we have a 'large' image, the palette is in the noise.

        # create the new palette if not every color is used
        optimise = _FORCE_OPTIMIZE or im.mode == "L"
        if optimise or im.width * im.height < 512 * 512:
            # check which colors are used
            used_palette_colors = []
            for i, count in enumerate(im.histogram()):
                if count:
                    used_palette_colors.append(i)

            if optimise or max(used_palette_colors) >= len(used_palette_colors):
                return used_palette_colors

            assert im.palette is not None
            num_palette_colors = len(im.palette.palette) // Image.getmodebands(
                im.palette.mode
            )
            current_palette_size = 1 << (num_palette_colors - 1).bit_length()
            if (
                # check that the palette would become smaller when saved
                len(used_palette_colors) <= current_palette_size // 2
                # check that the palette is not already the smallest possible size
                and current_palette_size > 2
            ):
                return used_palette_colors
    return None

