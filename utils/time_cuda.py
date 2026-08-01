
def time_cuda(fn, inputs, test_runs):
    t = Timer(stmt="fn(*inputs)", globals={"fn": fn, "inputs" : inputs})
    times = t.blocked_autorange()
    return times.median * 1000  # time in ms

