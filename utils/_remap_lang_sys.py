
def _remapLangSys(langSys, featureRemap):
    if langSys.ReqFeatureIndex != 0xFFFF:
        langSys.ReqFeatureIndex = featureRemap[langSys.ReqFeatureIndex]
    langSys.FeatureIndex = [featureRemap[index] for index in langSys.FeatureIndex]

