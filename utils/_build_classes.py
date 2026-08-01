
def _buildClasses():
    import re
    from .otData import otData

    formatPat = re.compile(r"([A-Za-z0-9]+)Format(\d+)$")
    namespace = globals()

    # populate module with classes
    for name, fields in otData:
        baseClass = BaseTable
        m = formatPat.match(name)
        if m:
            # XxxFormatN subtable, we only add the "base" table
            name = m.group(1)
            # the first row of a format-switching otData table describes the Format;
            # the first column defines the type of the Format field.
            # Currently this can be either 'uint16' or 'uint8'.
            formatType = fields[0].type
            baseClass = getFormatSwitchingBaseTableClass(formatType)
        if name not in namespace:
            # the class doesn't exist yet, so the base implementation is used.
            cls = type(name, (baseClass,), {})
            if name in ("GSUB", "GPOS"):
                cls.DontShare = True
            namespace[name] = cls

    # link Var{Table} <-> {Table} (e.g. ColorStop <-> VarColorStop, etc.)
    for name, _ in otData:
        if name.startswith("Var") and len(name) > 3 and name[3:] in namespace:
            varType = namespace[name]
            noVarType = namespace[name[3:]]
            varType.NoVarType = noVarType
            noVarType.VarType = varType

    for base, alts in _equivalents.items():
        base = namespace[base]
        for alt in alts:
            namespace[alt] = base

    global lookupTypes
    lookupTypes = {
        "GSUB": {
            1: SingleSubst,
            2: MultipleSubst,
            3: AlternateSubst,
            4: LigatureSubst,
            5: ContextSubst,
            6: ChainContextSubst,
            7: ExtensionSubst,
            8: ReverseChainSingleSubst,
        },
        "GPOS": {
            1: SinglePos,
            2: PairPos,
            3: CursivePos,
            4: MarkBasePos,
            5: MarkLigPos,
            6: MarkMarkPos,
            7: ContextPos,
            8: ChainContextPos,
            9: ExtensionPos,
        },
        "mort": {
            4: NoncontextualMorph,
        },
        "morx": {
            0: RearrangementMorph,
            1: ContextualMorph,
            2: LigatureMorph,
            # 3: Reserved,
            4: NoncontextualMorph,
            5: InsertionMorph,
        },
    }
    lookupTypes["JSTF"] = lookupTypes["GPOS"]  # JSTF contains GPOS
    for lookupEnum in lookupTypes.values():
        for enum, cls in lookupEnum.items():
            cls.LookupType = enum

    global featureParamTypes
    featureParamTypes = {
        "size": FeatureParamsSize,
    }
    for i in range(1, 20 + 1):
        featureParamTypes["ss%02d" % i] = FeatureParamsStylisticSet
    for i in range(1, 99 + 1):
        featureParamTypes["cv%02d" % i] = FeatureParamsCharacterVariants

    # add converters to classes
    from .otConverters import buildConverters

    for name, fields in otData:
        m = formatPat.match(name)
        if m:
            # XxxFormatN subtable, add converter to "base" table
            name, format = m.groups()
            format = int(format)
            cls = namespace[name]
            if not hasattr(cls, "converters"):
                cls.converters = {}
                cls.convertersByName = {}
            converters, convertersByName = buildConverters(fields[1:], namespace)
            cls.converters[format] = converters
            cls.convertersByName[format] = convertersByName
            # XXX Add staticSize?
        else:
            cls = namespace[name]
            cls.converters, cls.convertersByName = buildConverters(fields, namespace)

