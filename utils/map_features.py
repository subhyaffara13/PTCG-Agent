
def mapFeatures(self, featureMap):
    self.FeatureIndex = [featureMap[i] for i in self.FeatureIndex]
    if self.ReqFeatureIndex != 65535:
        self.ReqFeatureIndex = featureMap[self.ReqFeatureIndex]


def mapFeatures(self, featureMap):
    if self.DefaultLangSys:
        self.DefaultLangSys.mapFeatures(featureMap)
    for l in self.LangSysRecord:
        if not l or not l.LangSys:
            continue
        l.LangSys.mapFeatures(featureMap)


def mapFeatures(self, featureMap):
    for s in self.ScriptRecord:
        if not s or not s.Script:
            continue
        s.Script.mapFeatures(featureMap)

