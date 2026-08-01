
def _test_particular_example(our_hint, ode_example, solver_flag=False):
    eq = ode_example['eq']
    expected_sol = ode_example['sol']
    example = ode_example['example_name']
    xfail = our_hint in ode_example['XFAIL']
    func = ode_example['func']
    result = {'msg': '', 'xpass_msg': ''}
    simplify_flag=ode_example['simplify_flag']
    checkodesol_XFAIL = ode_example['checkodesol_XFAIL']
    dsolve_too_slow = ode_example['dsolve_too_slow']
    checkodesol_too_slow = ode_example['checkodesol_too_slow']
    xpass = True
    if solver_flag:
        if our_hint not in classify_ode(eq, func):
            message = hint_message.format(example=example, eq=eq, our_hint=our_hint)
            raise AssertionError(message)

    if our_hint in classify_ode(eq, func):
        result['match_list'] = example
        try:
            if not (dsolve_too_slow):
                dsolve_sol = dsolve(eq, func, simplify=simplify_flag,hint=our_hint)
            else:
                if len(expected_sol)==1:
                    dsolve_sol = expected_sol[0]
                else:
                    dsolve_sol = expected_sol

        except Exception as e:
            dsolve_sol = []
            result['exception_list'] = example
            if not solver_flag:
                traceback.print_exc()
            result['msg'] = exception_msg.format(e=str(e), hint=our_hint, example=example, eq=eq)
            if solver_flag and not xfail:
                print(result['msg'])
                raise
            xpass = False

        if solver_flag and dsolve_sol!=[]:
            expect_sol_check = False
            if type(dsolve_sol)==list:
                for sub_sol in expected_sol:
                    if sub_sol.has(Dummy):
                        expect_sol_check = not _test_dummy_sol(sub_sol, dsolve_sol)
                    else:
                        expect_sol_check = sub_sol not in dsolve_sol
                    if expect_sol_check:
                        break
            else:
                expect_sol_check = dsolve_sol not in expected_sol
                for sub_sol in expected_sol:
                    if sub_sol.has(Dummy):
                        expect_sol_check = not _test_dummy_sol(sub_sol, dsolve_sol)

            if expect_sol_check:
                message = expected_sol_message.format(example=example, eq=eq, sol=expected_sol, dsolve_sol=dsolve_sol)
                raise AssertionError(message)

            expected_checkodesol = [(True, 0) for i in range(len(expected_sol))]
            if len(expected_sol) == 1:
                expected_checkodesol = (True, 0)

            if not checkodesol_too_slow:
                if not checkodesol_XFAIL:
                    if checkodesol(eq, dsolve_sol, func, solve_for_func=False) != expected_checkodesol:
                        result['unsolve_list'] = example
                        xpass = False
                        message = dsol_incorrect_msg.format(hint=our_hint, eq=eq, sol=expected_sol,dsolve_sol=dsolve_sol)
                        if solver_flag:
                            message = checkodesol_msg.format(example=example, eq=eq)
                            raise AssertionError(message)
                        else:
                            result['msg'] = 'AssertionError: ' + message

        if xpass and xfail:
            result['xpass_msg'] = example + "is now passing for the hint" + our_hint
    return result

