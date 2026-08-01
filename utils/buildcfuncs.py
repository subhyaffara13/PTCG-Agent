
def buildcfuncs():
    from .capi_maps import c2capi_map
    for k in c2capi_map.keys():
        m = f'pyarr_from_p_{k}1'
        cppmacros[
            m] = f'#define {m}(v) (PyArray_SimpleNewFromData(0,NULL,{c2capi_map[k]},(char *)v))'
    k = 'string'
    m = f'pyarr_from_p_{k}1'
    # NPY_CHAR compatibility, NPY_STRING with itemsize 1
    cppmacros[
        m] = f'#define {m}(v,dims) (PyArray_New(&PyArray_Type, 1, dims, NPY_STRING, NULL, v, 1, NPY_ARRAY_CARRAY, NULL))'

