
def _get_font(font_filepaths, *, _kerning_factor, thread_id,
              enable_last_resort):
    (first_fontpath, first_fontindex), *rest = font_filepaths
    fallback_list = [
        ft2font.FT2Font(fpath, face_index=index,
                        _kerning_factor=_kerning_factor)
        for fpath, index in rest
    ]
    last_resort_path = _cached_realpath(
        cbook._get_data_path('fonts', 'ttf', 'LastResortHE-Regular.ttf'))
    try:
        last_resort_index = font_filepaths.index((last_resort_path, 0))
    except ValueError:
        last_resort_index = -1
        # Add Last Resort font so we always have glyphs regardless of font, unless we're
        # already in the list.
        if enable_last_resort:
            fallback_list.append(
                ft2font.FT2Font(last_resort_path,
                                _kerning_factor=_kerning_factor,
                                _warn_if_used=True))
            last_resort_index = len(fallback_list)
    font = ft2font.FT2Font(
        first_fontpath, face_index=first_fontindex,
        _fallback_list=fallback_list,
        _kerning_factor=_kerning_factor
    )
    # Ensure we are using the right charmap for the Last Resort font; FreeType picks the
    # Unicode one by default, but this exists only for Windows, and is empty.
    if last_resort_index == 0:
        font.set_charmap(0)
    elif last_resort_index > 0:
        fallback_list[last_resort_index - 1].set_charmap(0)
    return font

