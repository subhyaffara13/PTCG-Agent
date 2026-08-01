
def reorderFontTables(
    inFile: BinaryIO,  # Takes file-like object as per original
    outFile: BinaryIO,  # Takes file-like object
    tableOrder: Sequence[str] | None = None,
    checkChecksums: bool = False,  # Keep param even if reader handles it
) -> None:
    """Rewrite a font file, ordering the tables as recommended by the
    OpenType specification 1.4.
    """
    inFile.seek(0)
    outFile.seek(0)
    reader = SFNTReader(inFile, checkChecksums=checkChecksums)
    writer = SFNTWriter(
        outFile,
        len(reader.tables),
        reader.sfntVersion,
        reader.flavor,
        reader.flavorData,
    )
    tables = list(reader.keys())
    for tag in sortedTagList(tables, tableOrder):
        writer[tag] = reader[tag]
    writer.close()

