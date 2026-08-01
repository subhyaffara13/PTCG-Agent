
def buildConverters(table):
    d = {}
    for op, name, arg, default, conv in table:
        d[name] = conv
    return d


def buildConverters(tableSpec: list[FieldSpec], tableNamespace):
    """Given a table spec from otData.py, build a converter object for each
    field of the table. This is called for each table in otData.py, and
    the results are assigned to the corresponding class in otTables.py."""
    converters = []
    convertersByName = {}
    for spec in tableSpec:
        tableName = spec.name
        if spec.name.startswith("ValueFormat"):
            assert spec.type == "uint16"
            converterClass = ValueFormat
        elif spec.name.endswith("Count") or spec.name in ("StructLength", "MorphType"):
            converterClass = {
                "uint8": ComputedUInt8,
                "uint16": ComputedUShort,
                "uint32": ComputedULong,
            }[spec.type]
        elif spec.name == "SubTable":
            converterClass = SubTable
        elif spec.name == "ExtSubTable":
            converterClass = ExtSubTable
        elif spec.name == "SubStruct":
            converterClass = SubStruct
        elif spec.name == "FeatureParams":
            converterClass = FeatureParams
        elif spec.name in ("CIDGlyphMapping", "GlyphCIDMapping"):
            converterClass = StructWithLength
        else:
            if not spec.type in converterMapping and "(" not in spec.type:
                tableName = spec.type
                converterClass = Struct
            else:
                converterClass = eval(spec.type, tableNamespace, converterMapping)

        conv = converterClass(
            spec.name, spec.repeat, spec.aux, description=spec.description
        )

        if conv.tableClass:
            # A "template" such as OffsetTo(AType) knows the table class already
            tableClass = conv.tableClass
        elif spec.type in ("MortChain", "MortSubtable", "MorxChain"):
            tableClass = tableNamespace.get(spec.type)
        else:
            tableClass = tableNamespace.get(tableName)

        if not conv.tableClass:
            conv.tableClass = tableClass

        if spec.name in ["SubTable", "ExtSubTable", "SubStruct"]:
            conv.lookupTypes = tableNamespace["lookupTypes"]
            # also create reverse mapping
            for t in conv.lookupTypes.values():
                for cls in t.values():
                    convertersByName[cls.__name__] = Table(
                        spec.name, spec.repeat, spec.aux, cls
                    )
        if spec.name == "FeatureParams":
            conv.featureParamTypes = tableNamespace["featureParamTypes"]
            conv.defaultFeatureParams = tableNamespace["FeatureParams"]
            for cls in conv.featureParamTypes.values():
                convertersByName[cls.__name__] = Table(
                    spec.name, spec.repeat, spec.aux, cls
                )
        converters.append(conv)
        assert spec.name not in convertersByName, spec.name
        convertersByName[spec.name] = conv
    return converters, convertersByName

