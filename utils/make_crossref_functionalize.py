import itertools
from typing import Callable

def make_crossref_functionalize(
    op: torch._ops.OpOverload[_P, _T], final_key: DispatchKey
) -> Callable[_P, _T] | DispatchKey:
    from torch._subclasses.fake_tensor import FakeTensorMode

    # This case is pretty weird, suppress it for now
    if op is torch.ops.aten.lift_fresh.default:
        return final_key

    def handler(*args: _P.args, **kwargs: _P.kwargs) -> _T:
        fake_mode = FakeTensorMode()

        def fakeify_defun(t: _R) -> _R | torch._subclasses.fake_tensor.FakeTensor:
            if isinstance(t, torch.Tensor):
                if torch._is_functional_tensor(t):
                    r = torch._from_functional_tensor(t)
                    # NB: This assumes that the inner tensor sizes/strides match
                    # the outer tensor sizes/strides.  This doesn't necessarily have to
                    # be the case, see discussion at
                    # https://github.com/pytorch/pytorch/pull/87610/files/401ddeda1d769bedc88a12de332c7357b60e51a4#r1007264456
                    if t.size() != r.size():
                        raise AssertionError(f"size mismatch: {t.size()} != {r.size()}")
                    if t.stride() != r.stride():
                        raise AssertionError(
                            f"stride mismatch: {t.stride()} != {r.stride()}"
                        )
                else:
                    r = t
                # TODO: suppress guards
                return fake_mode.from_tensor(r)
            return t

        def maybe_detach(t: _R) -> _R | torch.Tensor:
            if isinstance(t, torch.Tensor):
                return t.detach()
            else:
                return t

        # TODO: This probably does the wrong thing if you're running other
        # substantive modes with the normal op outside here
        with (
            torch.utils._python_dispatch._disable_current_modes(),
            suspend_functionalization(),
        ):
            f_args, f_kwargs = pytree.tree_map(fakeify_defun, (args, kwargs))
            orig_f_args, orig_f_kwargs = pytree.tree_map(
                maybe_detach, (f_args, f_kwargs)
            )
            with fake_mode:
                f_r = op(*f_args, **f_kwargs)  # pyrefly: ignore [invalid-param-spec]
        r = op._op_dk(final_key, *args, **kwargs)

        def desc() -> str:
            fmt_args = ", ".join(
                itertools.chain(
                    (repr(pytree.tree_map(_fmt, a)) for a in orig_f_args),
                    (
                        f"{k}={pytree.tree_map(_fmt, v)}"
                        for k, v in orig_f_kwargs.items()
                    ),
                )
            )
            return f"{op}({fmt_args})"

        check_metadata_matches(f_r, r, desc)
        return r

    return handler

