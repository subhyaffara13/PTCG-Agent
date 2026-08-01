
def substitution(system, symbols, result=[{}], known_symbols=[],
                 exclude=[], all_symbols=None):
    r"""
    Solves the `system` using substitution method. It is used in
    :func:`~.nonlinsolve`. This will be called from :func:`~.nonlinsolve` when any
    equation(s) is non polynomial equation.

    Parameters
    ==========

    system : list of equations
        The target system of equations
    symbols : list of symbols to be solved.
        The variable(s) for which the system is solved
    known_symbols : list of solved symbols
        Values are known for these variable(s)
    result : An empty list or list of dict
        If No symbol values is known then empty list otherwise
        symbol as keys and corresponding value in dict.
    exclude : Set of expression.
        Mostly denominator expression(s) of the equations of the system.
        Final solution should not satisfy these expressions.
    all_symbols : known_symbols + symbols(unsolved).

    Returns
    =======

    A FiniteSet of ordered tuple of values of `all_symbols` for which the
    `system` has solution. Order of values in the tuple is same as symbols
    present in the parameter `all_symbols`. If parameter `all_symbols` is None
    then same as symbols present in the parameter `symbols`.

    Please note that general FiniteSet is unordered, the solution returned
    here is not simply a FiniteSet of solutions, rather it is a FiniteSet of
    ordered tuple, i.e. the first & only argument to FiniteSet is a tuple of
    solutions, which is ordered, & hence the returned solution is ordered.

    Also note that solution could also have been returned as an ordered tuple,
    FiniteSet is just a wrapper `{}` around the tuple. It has no other
    significance except for the fact it is just used to maintain a consistent
    output format throughout the solveset.

    Raises
    ======

    ValueError
        The input is not valid.
        The symbols are not given.
    AttributeError
        The input symbols are not :class:`~.Symbol` type.

    Examples
    ========

    >>> from sympy import symbols, substitution
    >>> x, y = symbols('x, y', real=True)
    >>> substitution([x + y], [x], [{y: 1}], [y], set([]), [x, y])
    {(-1, 1)}

    * When you want a soln not satisfying $x + 1 = 0$

    >>> substitution([x + y], [x], [{y: 1}], [y], set([x + 1]), [y, x])
    EmptySet
    >>> substitution([x + y], [x], [{y: 1}], [y], set([x - 1]), [y, x])
    {(1, -1)}
    >>> substitution([x + y - 1, y - x**2 + 5], [x, y])
    {(-3, 4), (2, -1)}

    * Returns both real and complex solution

    >>> x, y, z = symbols('x, y, z')
    >>> from sympy import exp, sin
    >>> substitution([exp(x) - sin(y), y**2 - 4], [x, y])
    {(ImageSet(Lambda(_n, I*(2*_n*pi + pi) + log(sin(2))), Integers), -2),
     (ImageSet(Lambda(_n, 2*_n*I*pi + log(sin(2))), Integers), 2)}

    >>> eqs = [z**2 + exp(2*x) - sin(y), -3 + exp(-y)]
    >>> substitution(eqs, [y, z])
    {(-log(3), -sqrt(-exp(2*x) - sin(log(3)))),
     (-log(3), sqrt(-exp(2*x) - sin(log(3)))),
     (ImageSet(Lambda(_n, 2*_n*I*pi - log(3)), Integers),
      ImageSet(Lambda(_n, -sqrt(-exp(2*x) + sin(2*_n*I*pi - log(3)))), Integers)),
     (ImageSet(Lambda(_n, 2*_n*I*pi - log(3)), Integers),
      ImageSet(Lambda(_n, sqrt(-exp(2*x) + sin(2*_n*I*pi - log(3)))), Integers))}

    """

    if not system:
        return S.EmptySet

    for i, e in enumerate(system):
        if isinstance(e, Eq):
            system[i] = e.lhs - e.rhs

    if not symbols:
        msg = ('Symbols must be given, for which solution of the '
               'system is to be found.')
        raise ValueError(filldedent(msg))

    if not is_sequence(symbols):
        msg = ('symbols should be given as a sequence, e.g. a list.'
               'Not type %s: %s')
        raise TypeError(filldedent(msg % (type(symbols), symbols)))

    if not getattr(symbols[0], 'is_Symbol', False):
        msg = ('Iterable of symbols must be given as '
               'second argument, not type %s: %s')
        raise ValueError(filldedent(msg % (type(symbols[0]), symbols[0])))

    # By default `all_symbols` will be same as `symbols`
    if all_symbols is None:
        all_symbols = symbols

    old_result = result
    # storing complements and intersection for particular symbol
    complements = {}
    intersections = {}

    # when total_solveset_call equals total_conditionset
    # it means that solveset failed to solve all eqs.
    total_conditionset = -1
    total_solveset_call = -1

    def _unsolved_syms(eq, sort=False):
        """Returns the unsolved symbol present
        in the equation `eq`.
        """
        free = eq.free_symbols
        unsolved = (free - set(known_symbols)) & set(all_symbols)
        if sort:
            unsolved = list(unsolved)
            unsolved.sort(key=default_sort_key)
        return unsolved

    # sort such that equation with the fewest potential symbols is first.
    # means eq with less number of variable first in the list.
    eqs_in_better_order = list(
        ordered(system, lambda _: len(_unsolved_syms(_))))

    def add_intersection_complement(result, intersection_dict, complement_dict):
        # If solveset has returned some intersection/complement
        # for any symbol, it will be added in the final solution.
        final_result = []
        for res in result:
            res_copy = res
            for key_res, value_res in res.items():
                intersect_set, complement_set = None, None
                for key_sym, value_sym in intersection_dict.items():
                    if key_sym == key_res:
                        intersect_set = value_sym
                for key_sym, value_sym in complement_dict.items():
                    if key_sym == key_res:
                        complement_set = value_sym
                if intersect_set or complement_set:
                    new_value = FiniteSet(value_res)
                    if intersect_set and intersect_set != S.Complexes:
                        new_value = Intersection(new_value, intersect_set)
                    if complement_set:
                        new_value = Complement(new_value, complement_set)
                    if new_value is S.EmptySet:
                        res_copy = None
                        break
                    elif new_value.is_FiniteSet and len(new_value) == 1:
                        res_copy[key_res] = set(new_value).pop()
                    else:
                        res_copy[key_res] = new_value

            if res_copy is not None:
                final_result.append(res_copy)
        return final_result

    def _extract_main_soln(sym, sol, soln_imageset):
        """Separate the Complements, Intersections, ImageSet lambda expr and
        its base_set. This function returns the unmasked sol from different classes
        of sets and also returns the appended ImageSet elements in a
        soln_imageset dict: `{unmasked element: ImageSet}`.
        """
        # if there is union, then need to check
        # Complement, Intersection, Imageset.
        # Order should not be changed.
        if isinstance(sol, ConditionSet):
            # extracts any solution in ConditionSet
            sol = sol.base_set

        if isinstance(sol, Complement):
            # extract solution and complement
            complements[sym] = sol.args[1]
            sol = sol.args[0]
            # complement will be added at the end
            # using `add_intersection_complement` method

        # if there is union of Imageset or other in soln.
        # no testcase is written for this if block
        if isinstance(sol, Union):
            sol_args = sol.args
            sol = S.EmptySet
            # We need in sequence so append finteset elements
            # and then imageset or other.
            for sol_arg2 in sol_args:
                if isinstance(sol_arg2, FiniteSet):
                    sol += sol_arg2
                else:
                    # ImageSet, Intersection, complement then
                    # append them directly
                    sol += FiniteSet(sol_arg2)

        if isinstance(sol, Intersection):
            # Interval/Set will be at 0th index always
            if sol.args[0] not in (S.Reals, S.Complexes):
                # Sometimes solveset returns soln with intersection
                # S.Reals or S.Complexes. We don't consider that
                # intersection.
                intersections[sym] = sol.args[0]
            sol = sol.args[1]
        # after intersection and complement Imageset should
        # be checked.
        if isinstance(sol, ImageSet):
            soln_imagest = sol
            expr2 = sol.lamda.expr
            sol = FiniteSet(expr2)
            soln_imageset[expr2] = soln_imagest

        if not isinstance(sol, FiniteSet):
            sol = FiniteSet(sol)
        return sol, soln_imageset

    def _check_exclude(rnew, imgset_yes):
        rnew_ = rnew
        if imgset_yes:
            # replace all dummy variables (Imageset lambda variables)
            # with zero before `checksol`. Considering fundamental soln
            # for `checksol`.
            rnew_copy = rnew.copy()
            dummy_n = imgset_yes[0]
            for key_res, value_res in rnew_copy.items():
                rnew_copy[key_res] = value_res.subs(dummy_n, 0)
            rnew_ = rnew_copy
        # satisfy_exclude == true if it satisfies the expr of `exclude` list.
        try:
            # something like : `Mod(-log(3), 2*I*pi)` can't be
            # simplified right now, so `checksol` returns `TypeError`.
            # when this issue is fixed this try block should be
            # removed. Mod(-log(3), 2*I*pi) == -log(3)
            satisfy_exclude = any(
                checksol(d, rnew_) for d in exclude)
        except TypeError:
            satisfy_exclude = None
        return satisfy_exclude

    def _restore_imgset(rnew, original_imageset, newresult):
        restore_sym = set(rnew.keys()) & \
            set(original_imageset.keys())
        for key_sym in restore_sym:
            img = original_imageset[key_sym]
            rnew[key_sym] = img
        if rnew not in newresult:
            newresult.append(rnew)

    def _append_eq(eq, result, res, delete_soln, n=None):
        u = Dummy('u')
        if n:
            eq = eq.subs(n, 0)
        satisfy = eq if eq in (True, False) else checksol(u, u, eq, minimal=True)
        if satisfy is False:
            delete_soln = True
            res = {}
        else:
            result.append(res)
        return result, res, delete_soln

    def _append_new_soln(rnew, sym, sol, imgset_yes, soln_imageset,
                         original_imageset, newresult, eq=None):
        """If `rnew` (A dict <symbol: soln>) contains valid soln
        append it to `newresult` list.
        `imgset_yes` is (base, dummy_var) if there was imageset in previously
         calculated result(otherwise empty tuple). `original_imageset` is dict
         of imageset expr and imageset from this result.
        `soln_imageset` dict of imageset expr and imageset of new soln.
        """
        satisfy_exclude = _check_exclude(rnew, imgset_yes)
        delete_soln = False
        # soln should not satisfy expr present in `exclude` list.
        if not satisfy_exclude:
            local_n = None
            # if it is imageset
            if imgset_yes:
                local_n = imgset_yes[0]
                base = imgset_yes[1]
                if sym and sol:
                    # when `sym` and `sol` is `None` means no new
                    # soln. In that case we will append rnew directly after
                    # substituting original imagesets in rnew values if present
                    # (second last line of this function using _restore_imgset)
                    dummy_list = list(sol.atoms(Dummy))
                    # use one dummy `n` which is in
                    # previous imageset
                    local_n_list = [
                        local_n for i in range(
                            0, len(dummy_list))]

                    dummy_zip = zip(dummy_list, local_n_list)
                    lam = Lambda(local_n, sol.subs(dummy_zip))
                    rnew[sym] = ImageSet(lam, base)
                if eq is not None:
                    newresult, rnew, delete_soln = _append_eq(
                        eq, newresult, rnew, delete_soln, local_n)
            elif eq is not None:
                newresult, rnew, delete_soln = _append_eq(
                    eq, newresult, rnew, delete_soln)
            elif sol in soln_imageset.keys():
                rnew[sym] = soln_imageset[sol]
                # restore original imageset
                _restore_imgset(rnew, original_imageset, newresult)
            else:
                newresult.append(rnew)
        elif satisfy_exclude:
            delete_soln = True
            rnew = {}
        _restore_imgset(rnew, original_imageset, newresult)
        return newresult, delete_soln

    def _new_order_result(result, eq):
        # separate first, second priority. `res` that makes `eq` value equals
        # to zero, should be used first then other result(second priority).
        # If it is not done then we may miss some soln.
        first_priority = []
        second_priority = []
        for res in result:
            if not any(isinstance(val, ImageSet) for val in res.values()):
                if eq.subs(res) == 0:
                    first_priority.append(res)
                else:
                    second_priority.append(res)
        if first_priority or second_priority:
            return first_priority + second_priority
        return result

    def _solve_using_known_values(result, solver):
        """Solves the system using already known solution
        (result contains the dict <symbol: value>).
        solver is :func:`~.solveset_complex` or :func:`~.solveset_real`.
        """
        # stores imageset <expr: imageset(Lambda(n, expr), base)>.
        soln_imageset = {}
        total_solvest_call = 0
        total_conditionst = 0

        # sort equations so the one with the fewest potential
        # symbols appears first
        for index, eq in enumerate(eqs_in_better_order):
            newresult = []
            # if imageset, expr is used to solve for other symbol
            imgset_yes = False
            for res in result:
                original_imageset = {}
                got_symbol = set()  # symbols solved in one iteration
                # find the imageset and use its expr.
                for k, v in res.items():
                    if isinstance(v, ImageSet):
                        res[k] = v.lamda.expr
                        original_imageset[k] = v
                        dummy_n = v.lamda.expr.atoms(Dummy).pop()
                        (base,) = v.base_sets
                        imgset_yes = (dummy_n, base)
                    assert not isinstance(v, FiniteSet)  # if so, internal error
                # update eq with everything that is known so far
                eq2 = eq.subs(res).expand()
                if imgset_yes and not eq2.has(imgset_yes[0]):
                    # The substituted equation simplified in such a way that
                    # it's no longer necessary to encapsulate a potential new
                    # solution in an ImageSet. (E.g. at the previous step some
                    # {n*2*pi} was found as partial solution for one of the
                    # unknowns, but its main solution expression n*2*pi has now
                    # been substituted in a trigonometric function.)
                    imgset_yes = False

                unsolved_syms = _unsolved_syms(eq2, sort=True)
                if not unsolved_syms:
                    if res:
                        newresult, delete_res = _append_new_soln(
                            res, None, None, imgset_yes, soln_imageset,
                            original_imageset, newresult, eq2)
                        if delete_res:
                            # `delete_res` is true, means substituting `res` in
                            # eq2 doesn't return `zero` or deleting the `res`
                            # (a soln) since it satisfies expr of `exclude`
                            # list.
                            result.remove(res)
                    continue  # skip as it's independent of desired symbols
                depen1, depen2 = eq2.as_independent(*unsolved_syms)
                if (depen1.has(Abs) or depen2.has(Abs)) and solver == solveset_complex:
                    # Absolute values cannot be inverted in the
                    # complex domain
                    continue
                soln_imageset = {}
                for sym in unsolved_syms:
                    not_solvable = False
                    try:
                        soln = solver(eq2, sym)
                        total_solvest_call += 1
                        soln_new = S.EmptySet
                        if isinstance(soln, Complement):
                            # separate solution and complement
                            complements[sym] = soln.args[1]
                            soln = soln.args[0]
                            # complement will be added at the end
                        if isinstance(soln, Intersection):
                            # Interval will be at 0th index always
                            if soln.args[0] != Interval(-oo, oo):
                                # sometimes solveset returns soln
                                # with intersection S.Reals, to confirm that
                                # soln is in domain=S.Reals
                                intersections[sym] = soln.args[0]
                            soln_new += soln.args[1]
                        soln = soln_new if soln_new else soln
                        if index > 0 and solver == solveset_real:
                            # one symbol's real soln, another symbol may have
                            # corresponding complex soln.
                            if not isinstance(soln, (ImageSet, ConditionSet)):
                                soln += solveset_complex(eq2, sym)  # might give ValueError with Abs
                    except (NotImplementedError, ValueError):
                        # If solveset is not able to solve equation `eq2`. Next
                        # time we may get soln using next equation `eq2`
                        continue
                    if isinstance(soln, ConditionSet):
                        if soln.base_set in (S.Reals, S.Complexes):
                            soln = S.EmptySet
                            # don't do `continue` we may get soln
                            # in terms of other symbol(s)
                            not_solvable = True
                            total_conditionst += 1
                        else:
                            soln = soln.base_set

                    if soln is not S.EmptySet:
                        soln, soln_imageset = _extract_main_soln(
                            sym, soln, soln_imageset)

                    for sol in soln:
                        # sol is not a `Union` since we checked it
                        # before this loop
                        sol, soln_imageset = _extract_main_soln(
                            sym, sol, soln_imageset)
                        sol = set(sol).pop()  # XXX what if there are more solutions?
                        free = sol.free_symbols
                        if got_symbol and any(
                            ss in free for ss in got_symbol
                        ):
                            # sol depends on previously solved symbols
                            # then continue
                            continue
                        rnew = res.copy()
                        # put each solution in res and append the new  result
                        # in the new result list (solution for symbol `s`)
                        # along with old results.
                        for k, v in res.items():
                            if isinstance(v, Expr) and isinstance(sol, Expr):
                                # if any unsolved symbol is present
                                # Then subs known value
                                rnew[k] = v.subs(sym, sol)
                        # and add this new solution
                        if sol in soln_imageset.keys():
                            # replace all lambda variables with 0.
                            imgst = soln_imageset[sol]
                            rnew[sym] = imgst.lamda(
                                *[0 for i in range(0, len(
                                    imgst.lamda.variables))])
                        else:
                            rnew[sym] = sol
                        newresult, delete_res = _append_new_soln(
                            rnew, sym, sol, imgset_yes, soln_imageset,
                            original_imageset, newresult)
                        if delete_res:
                            # deleting the `res` (a soln) since it satisfies
                            # eq of `exclude` list
                            result.remove(res)
                    # solution got for sym
                    if not not_solvable:
                        got_symbol.add(sym)
            # next time use this new soln
            if newresult:
                result = newresult
        return result, total_solvest_call, total_conditionst

    new_result_real, solve_call1, cnd_call1 = _solve_using_known_values(
        old_result, solveset_real)
    new_result_complex, solve_call2, cnd_call2 = _solve_using_known_values(
        old_result, solveset_complex)

    # If total_solveset_call is equal to total_conditionset
    # then solveset failed to solve all of the equations.
    # In this case we return a ConditionSet here.
    total_conditionset += (cnd_call1 + cnd_call2)
    total_solveset_call += (solve_call1 + solve_call2)

    if total_conditionset == total_solveset_call and total_solveset_call != -1:
        return _return_conditionset(eqs_in_better_order, all_symbols)

    # don't keep duplicate solutions
    filtered_complex = []
    for i in list(new_result_complex):
        for j in list(new_result_real):
            if i.keys() != j.keys():
                continue
            if all(a.dummy_eq(b) for a, b in zip(i.values(), j.values()) \
                if not (isinstance(a, int) and isinstance(b, int))):
                break
        else:
            filtered_complex.append(i)
    # overall result
    result = new_result_real + filtered_complex

    result_all_variables = []
    result_infinite = []
    for res in result:
        if not res:
            # means {None : None}
            continue
        # If length < len(all_symbols) means infinite soln.
        # Some or all the soln is dependent on 1 symbol.
        # eg. {x: y+2} then final soln {x: y+2, y: y}
        if len(res) < len(all_symbols):
            solved_symbols = res.keys()
            unsolved = list(filter(
                lambda x: x not in solved_symbols, all_symbols))
            for unsolved_sym in unsolved:
                res[unsolved_sym] = unsolved_sym
            result_infinite.append(res)
        if res not in result_all_variables:
            result_all_variables.append(res)

    if result_infinite:
        # we have general soln
        # eg : [{x: -1, y : 1}, {x : -y, y: y}] then
        # return [{x : -y, y : y}]
        result_all_variables = result_infinite
    if intersections or complements:
        result_all_variables = add_intersection_complement(
            result_all_variables, intersections, complements)

    # convert to ordered tuple
    result = S.EmptySet
    for r in result_all_variables:
        temp = [r[symb] for symb in all_symbols]
        result += FiniteSet(tuple(temp))
    return result


def substitution(old, new):
    """
    Return a function that will perform a substitution on a string
    """
    return lambda s: s.replace(old, new)

