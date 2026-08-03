from typing import Any, Dict, Optional, Tuple, Union

def cancel(f, *gens, _signsimp=True, **args):
    """
    Cancel common factors in a rational function ``f``.

    Examples
    ========

    >>> from sympy import cancel, sqrt, Symbol, together
    >>> from sympy.abc import x
    >>> A = Symbol('A', commutative=False)

    >>> cancel((2*x**2 - 2)/(x**2 - 2*x + 1))
    (2*x + 2)/(x - 1)
    >>> cancel((sqrt(3) + sqrt(15)*A)/(sqrt(2) + sqrt(10)*A))
    sqrt(6)/2

    Note: due to automatic distribution of Rationals, a sum divided by an integer
    will appear as a sum. To recover a rational form use `together` on the result:

    >>> cancel(x/2 + 1)
    x/2 + 1
    >>> together(_)
    (x + 2)/2
    """
    from sympy.simplify.simplify import signsimp
    from sympy.polys.rings import sring
    options.allowed_flags(args, ['polys'])

    f = sympify(f)
    if _signsimp:
        f = signsimp(f)
    opt = {}
    if 'polys' in args:
        opt['polys'] = args['polys']

    if not isinstance(f, Tuple):
        if f.is_Number or isinstance(f, Relational) or not isinstance(f, Expr):
            return f
        f = factor_terms(f, radical=True)
        p, q = f.as_numer_denom()

    elif len(f) == 2:
        p, q = f
        if isinstance(p, Poly) and isinstance(q, Poly):
            opt['gens'] = p.gens
            opt['domain'] = p.domain
            opt['polys'] = opt.get('polys', True)
        p, q = p.as_expr(), q.as_expr()
    else:
        raise ValueError('unexpected argument: %s' % f)

    from sympy.functions.elementary.piecewise import Piecewise
    try:
        if f.has(Piecewise):
            raise PolynomialError()
        R, (F, G) = sring((p, q), *gens, **args)
        if not R.ngens:
            if not isinstance(f, Tuple):
                return f.expand()
            else:
                return S.One, p, q
    except PolynomialError as msg:
        if f.is_commutative and not f.has(Piecewise):
            raise PolynomialError(msg)
        # Handling of noncommutative and/or piecewise expressions
        if f.is_Add or f.is_Mul:
            c, nc = sift(f.args, lambda x:
                x.is_commutative is True and not x.has(Piecewise),
                binary=True)
            nc = [cancel(i) for i in nc]
            return f.func(cancel(f.func(*c)), *nc)
        else:
            reps = []
            pot = preorder_traversal(f)
            next(pot)
            for e in pot:
                if isinstance(e, BooleanAtom) or not isinstance(e, Expr):
                    continue
                try:
                    reps.append((e, cancel(e)))
                    pot.skip()  # this was handled successfully
                except NotImplementedError:
                    pass
            return f.xreplace(dict(reps))

    c, (P, Q) = 1, F.cancel(G)
    if opt.get('polys', False) and 'gens' not in opt:
        opt['gens'] = R.symbols

    if not isinstance(f, Tuple):
        return c*(P.as_expr()/Q.as_expr())
    else:
        P, Q = P.as_expr(), Q.as_expr()
        if not opt.get('polys', False):
            return c, P, Q
        else:
            return c, Poly(P, *gens, **opt), Poly(Q, *gens, **opt)


def cancel(
    interaction_id: str,
    extra_headers: Optional[Dict[str, Any]] = None,
    timeout: Optional[Union[float, httpx.Timeout]] = None,
    custom_llm_provider: Optional[str] = None,
    **kwargs,
) -> Union[CancelInteractionResult, Coroutine[Any, Any, CancelInteractionResult]]:
    """Sync: Cancel an interaction by its ID."""
    local_vars = locals()
    custom_llm_provider = custom_llm_provider or "gemini"

    try:
        litellm_logging_obj: LiteLLMLoggingObj = kwargs.get("litellm_logging_obj")  # type: ignore
        litellm_call_id: Optional[str] = kwargs.get("litellm_call_id", None)
        _is_async = kwargs.pop("acancel_interaction", False) is True

        litellm_params = GenericLiteLLMParams(**kwargs)

        interactions_api_config = get_provider_interactions_api_config(
            provider=custom_llm_provider,
        )

        if interactions_api_config is None:
            raise ValueError(
                f"Interactions API not supported for: {custom_llm_provider}"
            )

        litellm_logging_obj.update_from_kwargs(
            kwargs=kwargs,
            model=None,
            optional_params={"interaction_id": interaction_id},
            litellm_params={"litellm_call_id": litellm_call_id},
            custom_llm_provider=custom_llm_provider,
        )

        return interactions_http_handler.cancel_interaction(
            interaction_id=interaction_id,
            interactions_api_config=interactions_api_config,
            custom_llm_provider=custom_llm_provider,
            litellm_params=litellm_params,
            logging_obj=litellm_logging_obj,
            extra_headers=extra_headers,
            timeout=timeout,
            _is_async=_is_async,
        )
    except Exception as e:
        raise litellm.exception_type(
            model=None,
            custom_llm_provider=custom_llm_provider,
            original_exception=e,
            completion_kwargs=local_vars,
            extra_kwargs=kwargs,
        )

