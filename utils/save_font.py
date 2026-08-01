
def save_font(font, outfile, options):
    if options.with_zopfli and options.flavor == "woff":
        from fontTools.ttLib import sfnt

        sfnt.USE_ZOPFLI = True
    font.flavor = options.flavor
    font.cfg[USE_HARFBUZZ_REPACKER] = options.harfbuzz_repacker
    font.save(outfile, reorderTables=options.canonical_order)

