
def guess_solve_strategy(eq, symbol):
    try:
        solve(eq, symbol)
        return True
    except (TypeError, NotImplementedError):
        return False

