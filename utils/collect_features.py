
def collect_features(self):
    feature_indices = self.FeatureIndex[:]
    if self.ReqFeatureIndex != 65535:
        feature_indices.append(self.ReqFeatureIndex)
    return _uniq_sort(feature_indices)


def collect_features(self):
    feature_indices = [l.LangSys.collect_features() for l in self.LangSysRecord]
    if self.DefaultLangSys:
        feature_indices.append(self.DefaultLangSys.collect_features())
    return _uniq_sort(sum(feature_indices, []))


def collect_features(self):
    return _uniq_sort(sum((s.Script.collect_features() for s in self.ScriptRecord), []))

