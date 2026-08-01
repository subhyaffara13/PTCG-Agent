
def df_levels(request, df):
    """DataFrame with columns or index levels 'L1', 'L2', and 'L3'"""
    levels = request.param

    if levels:
        df = df.set_index(levels)

    return df

