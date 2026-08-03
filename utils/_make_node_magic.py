import functools
from typing import Callable

def _make_node_magic(method: str, func: Callable[..., sympy.Basic]) -> None:
    func = lru_cache(256)(func)

    if method in magic_methods_on_operator_with_trailing_underscore:
        method_attr = f"{method}_"
    else:
        method_attr = method

    def uninteresting_files() -> set[str]:
        import torch

        mods = [
            torch._dynamo.eval_frame,
            torch._dynamo.utils,
            torch.fx.experimental.sym_node,
            torch,
        ]
        import torch._dynamo.guards

        return (
            {inspect.getfile(m) for m in mods}
            | torch._dynamo.guards.uninteresting_files()
            | {"<string>"}
        )

    def capture_provenance(fn: Callable[..., SymNode]) -> Callable[..., SymNode]:
        @functools.wraps(fn)
        def wrapper(self: SymNode, other: SymNode | None = None) -> SymNode:
            if other is None:
                result = fn(self)
            else:
                result = fn(self, other)
            if torch._logging._internal.GET_DTRACE_STRUCTURED:
                if other is not None:
                    arguments = [self, other]
                else:
                    arguments = [self]

                def get_id(sym_node: SymNode) -> int | None:
                    # We don't want to return an ID if the input is a constant
                    import sympy

                    if sym_node.constant is not None:
                        return None
                    elif id(sym_node) == id(result):
                        return None
                    elif isinstance(sym_node.expr, (sympy.Integer, sympy.Float)):
                        return None
                    elif sym_node.expr in (sympy.true, sympy.false):
                        return None
                    return id(sym_node)

                dtrace_structured(
                    "expression_created",
                    metadata_fn=lambda: {
                        "method": method,
                        "result": str(result),
                        "result_id": id(result),
                        "arguments": [str(a) for a in arguments],
                        "argument_ids": [
                            get_id(i) for i in arguments if get_id(i) is not None
                        ],
                        "user_stack": structured.get_user_stack(3),
                        "stack": structured.get_framework_stack(3),
                    },
                )

            return result

        return wrapper

    @capture_provenance
    def binary_magic_impl(self: SymNode, other: SymNode) -> SymNode:
        from torch.fx.experimental.proxy_tensor import (
            get_proxy_mode,
            handle_sym_dispatch,
        )

        op = method_to_operator(method)

        out_hint: object = _NO_HINT
        if self.hint is not None and other.hint is not None:
            out_hint = op(self.hint, other.hint)

        if get_proxy_mode():
            return to_node(
                self, handle_sym_dispatch(op, (wrap_node(self), wrap_node(other)), {})
            )
        if not isinstance(other, SymNode):
            raise AssertionError(f"Expected SymNode, got {type(other)}")
        optimized_summation = False
        try:
            if method == "mod":
                from torch.utils._sympy.functions import Mod, PythonMod

                # Special handling for mod that requires access to the value
                # ranges
                shape_env = self.shape_env
                if shape_env is None:
                    raise AssertionError("shape_env is required for mod")
                if (
                    self.expr.is_nonnegative
                    or shape_env.bound_sympy(self.expr).lower >= 0
                ) and (
                    other.expr.is_nonnegative
                    or shape_env.bound_sympy(other.expr).lower >= 0
                ):
                    out = Mod(self.expr, other.expr)
                else:
                    out = PythonMod(self.expr, other.expr)
            elif method == "add":
                # see Note [optimized_summation]
                (optimized_summation, out) = _optimized_add(
                    self.expr,
                    other.expr,
                    self._optimized_summation,
                    other._optimized_summation,
                )
            elif method in ("eq", "ne", "ge", "gt", "le", "lt"):
                import sympy

                from torch.utils._sympy.symbol import symbol_is_type, SymT

                # Optimization: when one side is a single unbacked symbol
                # and other is constant, use evaluate=False to skip expensive
                # relational evaluation. We only do this for unbacked symbols
                # because they have no assumptions (like positive=True) that
                # sympy would use during evaluation.
                lhs_is_unbacked = self.expr.is_symbol and symbol_is_type(
                    self.expr, SymT.UNBACKED_INT
                )
                rhs_is_unbacked = other.expr.is_symbol and symbol_is_type(
                    other.expr, SymT.UNBACKED_INT
                )
                if (lhs_is_unbacked and other.expr.is_number) or (
                    rhs_is_unbacked and self.expr.is_number
                ):
                    rel_class = {
                        "eq": sympy.Eq,
                        "ne": sympy.Ne,
                        "ge": sympy.Ge,
                        "gt": sympy.Gt,
                        "le": sympy.Le,
                        "lt": sympy.Lt,
                    }[method]
                    out = rel_class(self.expr, other.expr, evaluate=False)
                else:
                    out = func(self.expr, other.expr)

            else:
                # TODO: consider constant prop here
                out = func(self.expr, other.expr)
        except Exception:
            log.warning("failed to eval %s(%s, %s)", method, self.expr, other.expr)
            raise
        sym_node_log.debug("%s %s %s -> %s", method, self.expr, other.expr, out)
        pytype: type
        # This is not strictly correct. In Python, a**b may return complex when
        # a < 0 and b is a float: (-1)**2.1. Same for sympy.sqrt(-3.14). This
        # returns a float while both arguments are ints: 2**(-1). Also, max and
        # min do not type promote. To avoid having data-dependent control flow
        # here, we just set the type to float if one of the args is a float. In
        # case of a type mismatch, we assume that it will be detected during
        # evaluation.
        if method in always_float_magic_methods:
            pytype = float
        elif method in always_bool_magic_methods:
            pytype = bool
        elif self.pytype is float or other.pytype is float:
            pytype = float
        else:
            pytype = self.pytype

        if (
            pytype is not None
            and out_hint is not _NO_HINT
            and out_hint is not None
            and not isinstance(out_hint, SymTypes)
        ):
            out_hint = pytype(out_hint)  # type: ignore[arg-type]

        # Create a FX node that corresponds to the operation being applied to
        # this node.
        if self.shape_env is None:
            raise RuntimeError("shape_env is required for binary op")
        fx_node, _ = self.shape_env._create_fx_call_function(
            op, (self.fx_node, other.fx_node)
        )

        result = SymNode(
            out,
            self.shape_env,
            pytype,
            out_hint,  # type: ignore[arg-type]
            fx_node=fx_node,
            optimized_summation=optimized_summation,  # see Note [optimized_summation]
        )
        return result

    @capture_provenance
    def unary_magic_impl(self: SymNode) -> SymNode:
        from torch.fx.experimental.proxy_tensor import (
            get_proxy_mode,
            handle_sym_dispatch,
        )

        op = method_to_operator(method)
        if get_proxy_mode():
            return to_node(self, handle_sym_dispatch(op, (wrap_node(self),), {}))
        # TODO: consider constant prop here
        expr = self.expr
        if self.shape_env is None:
            raise RuntimeError("shape_env is required for unary op")
        if method == "floor" or method == "ceiling":
            expr = self.shape_env._simplify_floor_div(expr)

        try:
            out = func(expr)
        except Exception:
            log.warning("failed to eval %s(%s)", method, expr)
            raise
        sym_node_log.debug("%s %s -> %s", func, expr, out)
        out_hint: object = _NO_HINT
        if self.hint is not None:
            out_hint = op(self.hint)
        pytype: type
        if method in always_int_magic_methods:
            pytype = int
        elif method in always_bool_magic_methods:
            pytype = bool
        elif method in always_float_magic_methods:
            pytype = float
        else:
            pytype = self.pytype

        fx_node, _ = self.shape_env._create_fx_call_function(op, (self.fx_node,))
        return SymNode(out, self.shape_env, pytype, out_hint, fx_node=fx_node)  # type: ignore[arg-type]

    if method in unary_methods:
        setattr(SymNode, f"_{method_attr}", unary_magic_impl)
    elif method == "sym_ite":

        def sym_ite_impl(
            pred_node: SymNode, then_node: SymNode, else_node: SymNode
        ) -> SymNode:
            from torch.fx.experimental.proxy_tensor import (
                get_proxy_mode,
                handle_sym_dispatch,
            )

            if pred_node.hint is None:
                out_hint = None
            elif pred_node.hint:
                out_hint = then_node.hint
            else:
                out_hint = else_node.hint
            if get_proxy_mode():
                return to_node(
                    pred_node,
                    handle_sym_dispatch(
                        sym_ite,
                        (
                            wrap_node(pred_node),
                            wrap_node(then_node),
                            wrap_node(else_node),
                        ),
                        {},
                    ),
                )

            try:
                out = func(pred_node.expr, then_node.expr, else_node.expr)
            except Exception:
                log.warning(
                    "failed to eval %s(%s, %s, %s)",
                    method,
                    pred_node.expr,
                    then_node.expr,
                    else_node.expr,
                )
                raise

            if pred_node.shape_env is None:
                raise RuntimeError("shape_env is required for sym_ite")
            fx_node, _ = pred_node.shape_env._create_fx_call_function(
                sym_ite, (pred_node.fx_node, then_node.fx_node, else_node.fx_node)
            )
            return SymNode(
                out, pred_node.shape_env, then_node.pytype, out_hint, fx_node=fx_node
            )

        setattr(SymNode, f"_{method_attr}", sym_ite_impl)
    elif method == "round":

        def round_impl(self: SymNode, ndigits: int | None = None) -> SymNode:
            from torch.fx.experimental.proxy_tensor import (
                get_proxy_mode,
                handle_sym_dispatch,
            )

            op = builtins.round
            if get_proxy_mode():
                return to_node(
                    self, handle_sym_dispatch(op, (wrap_node(self), ndigits), {})
                )

            expr = self.expr
            try:
                out = func(expr, ndigits)
            except Exception:
                log.warning("failed to eval %s(%s, ndigits=%s)", method, expr, ndigits)
                raise

            if ndigits is None:
                pytype = int
            else:
                pytype = self.pytype

            out_hint = None
            if self.hint is not None:
                out_hint = op(  # pyrefly: ignore[no-matching-overload]
                    self.hint, ndigits
                )

            # Internally, None is used as sentinel to indicate that a something is not a node on an FX graph. At the
            # same time, there is no way to wrap a plain None into an FX node. Thus, there is no way to pass None here
            # without triggering some asserts that check whether we are mixing FX nodes with untracked arguments. The
            # hack down below works, because all round function down the line all take ndigits=None as default in their
            # signature.
            # TODO: Remove the args construction below if a different sentinel is used by FX.
            # ezyang(May 2024): LOL
            args = [self.fx_node]
            if ndigits is not None:
                args.append(ndigits)
            if self.shape_env is None:
                raise RuntimeError("shape_env is required for round")
            fx_node, _ = self.shape_env._create_fx_call_function(op, tuple(args))
            return SymNode(out, self.shape_env, pytype, out_hint, fx_node=fx_node)

        setattr(SymNode, f"_{method_attr}", round_impl)
    else:
        setattr(SymNode, f"_{method_attr}", binary_magic_impl)

