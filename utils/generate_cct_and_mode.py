
def generate_cct_and_mode(autograd_view_consistency=True):
    # This function returns a new class CompositeCompliantTensor
    # The two arguments control the behaviour described below.

    # autograd_view_consistency:
    #   If True, alias result using `set_` if func returns a view
    #   (See Note [Alias Result]).
    #   Since Forward AD doesn't work with `set_`
    #   we disable it by setting alias to False.

    class CompositeCompliantTensor(torch.Tensor):
        elem: torch.Tensor

        __slots__ = ['elem']

        @staticmethod
        def __new__(cls, elem, mode, *args, **kwargs):
            if type(elem) is cls:
                raise AssertionError(
                    "Wrapping a CompositeCompliantTensor in a CompositeCompliantTensor is not supported"
                )

            # The storage of CompositeCompliantTensor should never be used directly
            # by a Composite operation; if the Composite
            # operator attempts to read from the storage without dispatching then it'll
            # raise a RuntimeError due to it being a meta storage.
            r = torch.Tensor._make_wrapper_subclass(
                cls, elem.size(),
                dtype=elem.dtype, layout=elem.layout,
                device=elem.device, requires_grad=elem.requires_grad,
                strides=elem.stride(), storage_offset=elem.storage_offset())

            if elem.requires_grad:
                # CompositeCompliantTensor steals the "requires_grad"-ness.
                # Why a new copy of `elem`? Because sometimes OpInfo shares inputs between tests...
                tmp = torch.empty(
                    (),
                    dtype=elem.dtype,
                    device=elem.device,
                    layout=elem.layout,
                    requires_grad=False,
                )
                # Use set_ rather than empty_strided() + copy_ so that we can preserve
                # things like storage_offset.
                tmp.set_(
                    source=elem.untyped_storage().clone(),
                    storage_offset=elem.storage_offset(),
                    size=elem.size(),
                    stride=elem.stride(),
                )
                r.elem = tmp
            else:
                r.elem = elem

            if r.stride() != r.elem.stride():
                raise AssertionError(f"Expected r.stride() == r.elem.stride(), got {r.stride()} != {r.elem.stride()}")

            # Propagate conjugate bits to the wrapper tensor
            # Ref: https://github.com/albanD/subclass_zoo/issues/24
            # Ref: https://github.com/albanD/subclass_zoo/issues/21
            torch._C._set_conj(r, r.elem.is_conj())
            torch._C._set_neg(r, r.elem.is_neg())

            r.mode = mode
            return r

        def __repr__(self):
            return f"CompositeCompliantTensor({self.elem})"

        @classmethod
        def __torch_dispatch__(cls, func, types, args=(), kwargs=None):
            all_args = pytree.arg_tree_leaves(*args, **(kwargs or {}))
            modes = tuple(e.mode for e in all_args if isinstance(e, CompositeCompliantTensor))
            if not all_same_mode(modes):
                raise RuntimeError("Multiple CompositeCompliantTensorModes NYI")
            with modes[0]:
                return func(*args, **kwargs)

    class CompositeCompliantTensorMode(TorchDispatchMode):
        def __torch_dispatch__(self, func, types, args=(), kwargs=None):
            def unwrap(e):
                return e.elem if isinstance(e, CompositeCompliantTensor) else e

            def wrap(e):
                return CompositeCompliantTensor(e, self) if isinstance(e, torch.Tensor) else e

            if func is torch.ops.aten._local_scalar_dense.default:
                raise RuntimeError(
                    ".item() is not allowed to be called inside of composite "
                    "functions in the PyTorch library because not all backends "
                    "and/or Tensor subclasses (e.g. vmap, ProxyTensor) support them.")

            if func.overloadpacket.__name__ in ('set_', 'resize_'):
                raise RuntimeError(
                    f"{func.__name__} is not allowed to be called inside of "
                    f"Composite operators.")

            if is_inplace(func):
                # NB: We are making an assumption that if the function is in-place,
                # then the first argument is being written to. Introspection please save us!
                mutated_argument = args[0]
                if not isinstance(mutated_argument, CompositeCompliantTensor) and \
                        any(isinstance(a, CompositeCompliantTensor) for a in args[1:]):
                    raise RuntimeError(
                        'Not composite compliant: performing in-place operation '
                        f'{func.__name__} where the Tensor being written to is '
                        'regular Tensor but the other tensors are Tensor Subclasses. '
                        'Please try to avoid this in-place operation.')

            unwrapped_args = tree_map(unwrap, args)
            unwrapped_kwargs = tree_map(unwrap, kwargs)
            unwrapped_rs = func(*unwrapped_args, **unwrapped_kwargs)
            rs = tree_map(wrap, unwrapped_rs)

            if is_view_fn(func) and autograd_view_consistency:
                # Note [Alias Result]
                # Autograd asserts that for B = A.view_fn(...), B and A's storages
                # are the same. Here we try to make B alias A to avoid those asserts.
                # See https://github.com/pytorch/pytorch/issues/65339 for more information
                # about the issue.
                with no_dispatch():
                    # Idea: this is a weird way of getting a storage that aliases the input.
                    # This is a workaround for #65339.
                    # 1. under no_dispatch, all of the wrapper tensors look like regular
                    #    tensors with special storage (the storage is nullptr and
                    #    advertises CPU/CUDA device.
                    # 2. we run func, which ends up running the view operation
                    # 3. All view operations reuse the input's storage and return
                    #    result Tensor(s) with new sizes/strides/offset that alias
                    #    the input.
                    # 4. we set the storage (and sizes/strides/offset) of the wrapper
                    #    tensor results to be that of the tensors that alias the input
                    result = func(*args, **kwargs)
                    if isinstance(result, (tuple, list)):
                        for a, b in zip(rs, result, strict=True):
                            a.set_(b)
                    else:
                        rs.set_(result)

            # Some operations are allowed to in-place modify the metadata of the
            # inputs. The only ones are the "inplace view functions"; when we
            # run into these, we manually modify the metadata of the input.
            with no_dispatch():
                if is_inplace_view_fn(func):
                    func(*args, **kwargs)

            # For each CompositeCompliantTensor t, we check that t and t.elem
            # have consistent metadata. If they don't have consistent metadata,
            # that means the operator did something fishy.
            check = partial(check_metadata_consistency, CCT=CompositeCompliantTensor)
            pytree.tree_map_(check, args)
            pytree.tree_map_(check, kwargs)
            pytree.tree_map_(check, rs)
            return rs

    return CompositeCompliantTensor, CompositeCompliantTensorMode()

