
def datsp_math_dtypes(dat1d):
    dat_dtypes = {dtype: dat1d.astype(dtype) for dtype in math_dtypes}
    return {
        sp: [(dtype, dat, sp(dat)) for dtype, dat in dat_dtypes.items()]
        for sp in spcreators
    }


def datsp_math_dtypes(dat1d):
    dat_dtypes = {dtype: dat1d.astype(dtype) for dtype in math_dtypes}
    return {
        spcreator: [(dtype, dat, spcreator(dat)) for dtype, dat in dat_dtypes.items()]
        for spcreator in spcreators
    }

