
def df_idx(request, df_none):
    levels = request.param
    return df_none.set_index(levels)

