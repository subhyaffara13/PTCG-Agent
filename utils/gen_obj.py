
def gen_obj(klass, index):
    if klass is Series:
        obj = Series(np.arange(len(index)), index=index)
    else:
        obj = DataFrame(
            np.random.default_rng(2).standard_normal((len(index), len(index))),
            index=index,
            columns=index,
        )
    return obj

