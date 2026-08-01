
def get1(obj):  # TODO: make a helper in tm?
    if isinstance(obj, Series):
        return obj.iloc[0]
    else:
        return obj.iloc[0, 0]

