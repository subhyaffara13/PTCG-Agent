
def remove_redundant_langsys(self):
    table = self.table
    if not table.ScriptList or not table.FeatureList:
        return

    features = table.FeatureList.FeatureRecord

    for s in table.ScriptList.ScriptRecord:
        d = s.Script.DefaultLangSys
        if not d:
            continue
        for lr in s.Script.LangSysRecord[:]:
            l = lr.LangSys
            # Compare d and l
            if len(d.FeatureIndex) != len(l.FeatureIndex):
                continue
            if (d.ReqFeatureIndex == 65535) != (l.ReqFeatureIndex == 65535):
                continue

            if d.ReqFeatureIndex != 65535:
                if features[d.ReqFeatureIndex] != features[l.ReqFeatureIndex]:
                    continue

            for i in range(len(d.FeatureIndex)):
                if features[d.FeatureIndex[i]] != features[l.FeatureIndex[i]]:
                    break
            else:
                # LangSys and default are equal; delete LangSys
                s.Script.LangSysRecord.remove(lr)

