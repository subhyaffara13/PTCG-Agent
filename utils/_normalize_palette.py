from typing import Any

def _normalize_palette(
    im: Image.Image, palette: _Palette | None, info: dict[str, Any]
) -> Image.Image:
    """
    Normalizes the palette for image.
      - Sets the palette to the incoming palette, if provided.
      - Ensures that there's a palette for L mode images
      - Optimizes the palette if necessary/desired.

    :param im: Image object
    :param palette: bytes object containing the source palette, or ....
    :param info: encoderinfo
    :returns: Image object
    """
    source_palette = None
    if palette:
        # a bytes palette
        if isinstance(palette, (bytes, bytearray, list)):
            source_palette = bytearray(palette[:768])
        if isinstance(palette, ImagePalette.ImagePalette):
            source_palette = bytearray(palette.palette)

    if im.mode == "P":
        if not source_palette:
            im_palette = im.getpalette(None)
            assert im_palette is not None
            source_palette = bytearray(im_palette)
    else:  # L-mode
        if not source_palette:
            source_palette = bytearray(i // 3 for i in range(768))
        im.palette = ImagePalette.ImagePalette("RGB", palette=source_palette)
    assert source_palette is not None

    if palette:
        used_palette_colors: list[int | None] = []
        assert im.palette is not None
        for i in range(0, len(source_palette), 3):
            source_color = tuple(source_palette[i : i + 3])
            index = im.palette.colors.get(source_color)
            if index in used_palette_colors:
                index = None
            used_palette_colors.append(index)
        for i, index in enumerate(used_palette_colors):
            if index is None:
                for j in range(len(used_palette_colors)):
                    if j not in used_palette_colors:
                        used_palette_colors[i] = j
                        break
        dest_map: list[int] = []
        for index in used_palette_colors:
            assert index is not None
            dest_map.append(index)
        im = im.remap_palette(dest_map)
    else:
        optimized_palette_colors = _get_optimize(im, info)
        if optimized_palette_colors is not None:
            im = im.remap_palette(optimized_palette_colors, source_palette)
            if "transparency" in info:
                try:
                    info["transparency"] = optimized_palette_colors.index(
                        info["transparency"]
                    )
                except ValueError:
                    del info["transparency"]
            return im

    assert im.palette is not None
    im.palette.palette = source_palette
    return im

