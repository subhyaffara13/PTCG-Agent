import os

def _font_to_ps_type42(font_path, subset_index, glyph_indices, fh):
    """
    Subset *glyph_indices* from the font at *font_path* into a Type 42 font at *fh*.

    Parameters
    ----------
    font_path : FontPath
        Path to the font to be subsetted.
    subset_index : int
        The subset of the above font being created.
    glyph_indices : set[int]
        The glyphs to include in the subsetted font.
    fh : file-like
        Where to write the font.
    """
    _log.debug("SUBSET %s:%d characters: %s", font_path, subset_index, glyph_indices)
    try:
        with (fontTools.ttLib.TTFont(font_path.path,
                                     fontNumber=font_path.face_index) as font,
              _backend_pdf_ps.get_glyphs_subset(font_path, glyph_indices) as subset):
            fontdata = _backend_pdf_ps.font_as_file(subset).getvalue()
            _log.debug(
                "SUBSET %s:%d %d -> %d", font_path, subset_index,
                os.stat(font_path).st_size, len(fontdata)
            )
            fh.write(_serialize_type42(font, subset_index, subset, fontdata))
    except RuntimeError:
        _log.warning(
            "The PostScript backend does not currently support the selected font (%s).",
            font_path)
        raise

