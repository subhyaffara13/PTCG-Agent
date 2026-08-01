
def process_nl_constraints(nlcs):
    functions = []
    for nlc in nlcs:
        fun_i = transform_constraint_function(nlc)
        functions.append(fun_i)
    def constraint_function(x):
        values = np.empty(0, dtype=np.float64)
        for fun in functions:
            values = np.concatenate((values, fun(x)))
        return values
    return constraint_function

