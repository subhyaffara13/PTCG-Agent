
def buildGSUB():
    """Build a GSUB table from scratch."""
    fontTable = newTable("GSUB")
    gsub = fontTable.table = ot.GSUB()
    gsub.Version = 0x00010001  # allow gsub.FeatureVariations

    gsub.ScriptList = ot.ScriptList()
    gsub.ScriptList.ScriptRecord = []
    gsub.FeatureList = ot.FeatureList()
    gsub.FeatureList.FeatureRecord = []
    gsub.LookupList = ot.LookupList()
    gsub.LookupList.Lookup = []

    srec = ot.ScriptRecord()
    srec.ScriptTag = "DFLT"
    srec.Script = ot.Script()
    srec.Script.DefaultLangSys = None
    srec.Script.LangSysRecord = []
    srec.Script.LangSysCount = 0

    langrec = ot.LangSysRecord()
    langrec.LangSys = ot.LangSys()
    langrec.LangSys.ReqFeatureIndex = 0xFFFF
    langrec.LangSys.FeatureIndex = []
    srec.Script.DefaultLangSys = langrec.LangSys

    gsub.ScriptList.ScriptRecord.append(srec)
    gsub.ScriptList.ScriptCount = 1
    gsub.FeatureVariations = None

    return fontTable

