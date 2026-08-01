
def _all_models(models):
    satisfiable = False
    try:
        while True:
            yield next(models)
            satisfiable = True
    except StopIteration:
        if not satisfiable:
            yield False

