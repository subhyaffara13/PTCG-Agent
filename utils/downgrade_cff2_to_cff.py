
def downgradeCFF2ToCFF(varfont):
    # Save these properties
    recalcTimestamp = varfont.recalcTimestamp
    recalcBBoxes = varfont.recalcBBoxes

    # Disable them
    varfont.recalcTimestamp = False
    varfont.recalcBBoxes = False

    # Save to memory, reload, downgrade and save again, reload.
    # We do this dance because the convertCFF2ToCFF changes glyph
    # names, so following save would fail if any other table was
    # loaded and referencing glyph names.
    #
    # The second save+load is unfortunate but also necessary.

    stream = io.BytesIO()
    log.info("Saving CFF2 font to memory for downgrade")
    varfont.save(stream)
    stream.seek(0)
    varfont = TTFont(stream, recalcTimestamp=False, recalcBBoxes=False)

    convertCFF2ToCFF(varfont)

    stream = io.BytesIO()
    log.info("Saving downgraded CFF font to memory")
    varfont.save(stream)
    stream.seek(0)
    varfont = TTFont(stream, recalcTimestamp=False, recalcBBoxes=False)

    # Uncomment, to see test all tables can be loaded. This fails without
    # the extra save+load above.
    """
    for tag in varfont.keys():
        print("Loading", tag)
        varfont[tag]
    """

    # Restore them
    varfont.recalcTimestamp = recalcTimestamp
    varfont.recalcBBoxes = recalcBBoxes

    return varfont

