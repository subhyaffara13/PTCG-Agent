
def data_local(func, dataname, *a, **kw):
    kw.setdefault('dataname', dataname)
    return FuncData(func, DATASETS_LOCAL[dataname], *a, **kw)

