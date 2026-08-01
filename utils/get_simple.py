
def getSimple(self, attrs, *attr_list):
    for k in attr_list:
        if k in attrs:
            setattr(self, k, int(safeEval(attrs[k])))

