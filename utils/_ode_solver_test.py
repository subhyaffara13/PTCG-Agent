
def _ode_solver_test(ode_examples, run_slow_test=False):
    for example in ode_examples:
        if ((not run_slow_test) and example['slow']) or (run_slow_test and (not example['slow'])):
            continue

        result = _test_particular_example(example['hint'], example, solver_flag=True)
        if result['xpass_msg'] != "":
            print(result['xpass_msg'])

