
def _diop_solve(eq, params=None):
    for diop_type in all_diop_classes:
        if diop_type(eq).matches():
            return diop_type(eq).solve(parameters=params)

