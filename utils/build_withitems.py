
def build_withitems(ctx, items):
    items = [build_withitem(ctx, i) for i in items]
    return list(items)

