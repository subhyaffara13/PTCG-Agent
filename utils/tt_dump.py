
def ttDump(input, output, options):
    input_name = input
    if input == "-":
        input, input_name = sys.stdin.buffer, sys.stdin.name
    output_name = output
    if output == "-":
        output, output_name = sys.stdout, sys.stdout.name
    log.info('Dumping "%s" to "%s"...', input_name, output_name)
    if options.unicodedata:
        setUnicodeData(options.unicodedata)
    ttf = TTFont(
        input,
        0,
        ignoreDecompileErrors=options.ignoreDecompileErrors,
        fontNumber=options.fontNumber,
    )
    ttf.saveXML(
        output,
        tables=options.onlyTables,
        skipTables=options.skipTables,
        splitTables=options.splitTables,
        splitGlyphs=options.splitGlyphs,
        disassembleInstructions=options.disassembleInstructions,
        bitmapGlyphDataFormat=options.bitmapGlyphDataFormat,
        newlinestr=options.newlinestr,
    )
    ttf.close()

