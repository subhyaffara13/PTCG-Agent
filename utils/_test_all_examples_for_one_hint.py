
def _test_all_examples_for_one_hint(our_hint, all_examples=[], runxfail=None):
    if all_examples == []:
        all_examples = _get_all_examples()
    match_list, unsolve_list, exception_list = [], [], []
    for ode_example in all_examples:
        xfail = our_hint in ode_example['XFAIL']
        if runxfail and not xfail:
            continue
        if xfail:
            continue
        result = _test_particular_example(our_hint, ode_example)
        match_list += result.get('match_list',[])
        unsolve_list += result.get('unsolve_list',[])
        exception_list += result.get('exception_list',[])
        if runxfail is not None:
            msg = result['msg']
            if msg!='':
                print(result['msg'])
            # print(result.get('xpass_msg',''))
    if runxfail is None:
        match_count = len(match_list)
        solved = len(match_list)-len(unsolve_list)-len(exception_list)
        msg = check_hint_msg.format(hint=our_hint, matched=match_count, solve=solved, unsolve=unsolve_list, exceptions=exception_list)
        print(msg)

