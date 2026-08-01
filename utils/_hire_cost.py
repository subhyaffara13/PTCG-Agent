
def _hire_cost(n_already_today, mult=FARM_HAND_COST_MULT):
    return mult * _fib(n_already_today)

