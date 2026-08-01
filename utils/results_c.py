
def results_c(full_output, r, method):
    if full_output:
        x, funcalls, iterations, flag = r
        results = RootResults(root=x,
                              iterations=iterations,
                              function_calls=funcalls,
                              flag=flag, method=method)
        return x, results
    else:
        return r

