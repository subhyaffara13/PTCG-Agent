
def data_gsl(func, dataname, *a, **kw):
    kw.setdefault('dataname', dataname)
    return FuncData(func, DATASETS_GSL[dataname], *a, **kw)

