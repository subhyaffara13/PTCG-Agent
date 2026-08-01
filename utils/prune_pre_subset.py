
def prune_pre_subset(self, font, options):
    cff = self.cff
    # CFF table must have one font only
    cff.fontNames = cff.fontNames[:1]

    if options.notdef_glyph and not options.notdef_outline:
        isCFF2 = cff.major > 1
        for fontname in cff.keys():
            font = cff[fontname]
            _empty_charstring(font, ".notdef", isCFF2=isCFF2)

    # Clear useless Encoding
    for fontname in cff.keys():
        font = cff[fontname]
        # https://github.com/fonttools/fonttools/issues/620
        font.Encoding = "StandardEncoding"

    return True  # bool(cff.fontNames)


def prune_pre_subset(self, font, options):
    # Drop undesired features
    if "*" not in options.layout_scripts:
        self.subset_script_tags(options.layout_scripts)
    if "*" not in options.layout_features:
        self.subset_feature_tags(options.layout_features)
    # Neuter unreferenced lookups
    self.prune_lookups(remap=False)
    return True


def prune_pre_subset(self, font, options):
    # Prune unknown kern table types
    self.kernTables = [t for t in self.kernTables if hasattr(t, "kernTable")]
    return bool(self.kernTables)


def prune_pre_subset(self, font, options):
    if options.notdef_glyph and not options.notdef_outline:
        self.variations[font.glyphOrder[0]] = []
    return True


def prune_pre_subset(self, font, options):
    if not options.glyph_names:
        self.formatType = 3.0
    return True  # Required table


def prune_pre_subset(self, font, options):
    if options.notdef_glyph and not options.notdef_outline:
        g = self[self.glyphOrder[0]]
        # Yay, easy!
        g.__dict__.clear()
        g.data = b""
    return True


def prune_pre_subset(self, font, options):
    if not options.legacy_cmap:
        # Drop non-Unicode / non-Symbol cmaps
        self.tables = [t for t in self.tables if t.isUnicode() or t.isSymbol()]
    if not options.symbol_cmap:
        self.tables = [t for t in self.tables if not t.isSymbol()]
    # TODO(behdad) Only keep one subtable?
    # For now, drop format=0 which can't be subset_glyphs easily?
    self.tables = [t for t in self.tables if t.format != 0]
    self.numSubTables = len(self.tables)
    return True  # Required table


def prune_pre_subset(self, font, options):
    # Drop all signatures since they will be invalid
    self.usNumSigs = 0
    self.signatureRecords = []
    return True


def prune_pre_subset(self, font, options):
    if not options.hinting:
        if self.tableVersion == 0x00010000:
            self.maxZones = 1
            self.maxTwilightPoints = 0
            self.maxStorage = 0
            self.maxFunctionDefs = 0
            self.maxInstructionDefs = 0
            self.maxStackElements = 0
            self.maxSizeOfInstructions = 0
    return True

