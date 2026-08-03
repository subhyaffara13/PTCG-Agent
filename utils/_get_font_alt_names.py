import re

def _get_font_alt_names(font, primary_name):
    """
    Return ``(name, weight)`` pairs for alternate family names of *font*.

    A font file can advertise its family name in several places.  FreeType
    exposes ``font.family_name``, which is typically derived from the
    Macintosh-platform Name ID 1 entry.  However, other entries may carry
    different (equally valid) names that users reasonably expect to work:

    - **Name ID 1, other platform** — some fonts store a different family name
      on the Microsoft platform than on the Macintosh platform.
    - **Name ID 16** — "Typographic Family" (a.k.a. preferred family): groups
      more than the traditional four styles under one name.
    - **Name ID 21** — "WWS Family": an even narrower grouping used by some
      fonts (weight/width/slope only).

    Each name is paired with a weight derived from the corresponding subfamily
    entry on the *same* platform.  This ensures that the weight of the alternate entry
    reflects the font's role *within that named family* rather than its absolute
    typographic weight.

    Parameters
    ----------
    font : `.FT2Font`
    primary_name : str
        The family name already extracted from the font (``font.family_name``).

    Returns
    -------
    list of (str, int)
        ``(alternate_family_name, weight)`` pairs, not including *primary_name*.
    """
    try:
        sfnt = font.get_sfnt()
    except ValueError:
        return []

    mac_key = (1,  # platform: macintosh
               0,  # id: roman
               0)  # langid: english
    ms_key = (3,   # platform: microsoft
              1,   # id: unicode_cs
              0x0409)  # langid: english_united_states

    seen = {primary_name}
    result = []

    def _weight_from_subfam(subfam):
        subfam = subfam.replace(" ", "")
        for regex, weight in _weight_regexes:
            if re.search(regex, subfam, re.I):
                return weight
        return 400  # "Regular" or unrecognised

    def _try_add(name, subfam):
        name = name.strip()
        if not name or name in seen:
            return
        seen.add(name)
        result.append((name, _weight_from_subfam(subfam.strip())))

    # Each family-name ID is paired with its corresponding subfamily ID on the
    # same platform: (family_id, subfamily_id).
    for fam_id, subfam_id in ((1, 2), (16, 17), (21, 22)):
        _try_add(
            sfnt.get((*mac_key, fam_id), b'').decode('latin-1'),
            sfnt.get((*mac_key, subfam_id), b'').decode('latin-1'),
        )
        _try_add(
            sfnt.get((*ms_key, fam_id), b'').decode('utf-16-be'),
            sfnt.get((*ms_key, subfam_id), b'').decode('utf-16-be'),
        )

    return result

