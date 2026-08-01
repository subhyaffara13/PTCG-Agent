
def ttCompile(input, output, options):
    input_name = input
    if input == "-":
        input, input_name = sys.stdin, sys.stdin.name
    output_name = output
    if output == "-":
        output, output_name = sys.stdout.buffer, sys.stdout.name
    log.info('Compiling "%s" to "%s"...' % (input_name, output))
    if options.useZopfli:
        from fontTools.ttLib import sfnt

        sfnt.USE_ZOPFLI = True
    ttf = TTFont(
        options.mergeFile,
        flavor=options.flavor,
        recalcBBoxes=options.recalcBBoxes,
        recalcTimestamp=options.recalcTimestamp,
    )
    if options.optimizeFontSpeed:
        ttf.cfg[OPTIMIZE_FONT_SPEED] = options.optimizeFontSpeed
    ttf.importXML(input)

    if options.recalcTimestamp is None and "head" in ttf and input is not sys.stdin:
        # use TTX file modification time for head "modified" timestamp
        mtime = os.path.getmtime(input)
        ttf["head"].modified = timestampSinceEpoch(mtime)

    ttf.save(output)

