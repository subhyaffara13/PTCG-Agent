import os
import subprocess
import sys
from typing import Any, Callable

def call(libname, flag, encoding=sys.getfilesystemencoding()):
    """Calls pkg-config and returns the output if found
    """
    a = ["pkg-config", "--print-errors"]
    a.append(flag)
    a.append(libname)
    try:
        pc = subprocess.Popen(a, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except EnvironmentError as e:
        raise PkgConfigError("cannot run pkg-config: %s" % (str(e).strip(),))

    bout, berr = pc.communicate()
    if pc.returncode != 0:
        try:
            berr = berr.decode(encoding)
        except Exception:
            pass
        raise PkgConfigError(berr.strip())

    if sys.version_info >= (3,) and not isinstance(bout, str):   # Python 3.x
        try:
            bout = bout.decode(encoding)
        except UnicodeDecodeError:
            raise PkgConfigError("pkg-config %s %s returned bytes that cannot "
                                 "be decoded with encoding %r:\n%r" %
                                 (flag, libname, encoding, bout))

    if os.altsep != '\\' and '\\' in bout:
        raise PkgConfigError("pkg-config %s %s returned an unsupported "
                             "backslash-escaped output:\n%r" %
                             (flag, libname, bout))
    return bout


def call(
    o: Any,
    default: Any = None,
    path: list[str] | None = None,
    args: list[Any] | None = None,
    kwargs: dict[str, Any] | None = None,
) -> Any:
    if path is None:
        path = []
    if args is None:
        args = []
    if kwargs is None:
        kwargs = {}
    o = get(o, default=False, path=path, is_callable=True)
    if o is not False:
        return o(*args, **kwargs)
    else:
        return default


def call(*args, cwd=None):
    python_location = os.environ.get("PIPAPI_PYTHON_LOCATION", sys.executable)
    env = {**os.environ, **{"PIP_YES": "true", "PIP_DISABLE_PIP_VERSION_CHECK": "true"}}
    result = subprocess.check_output(
        [python_location, "-m", "pip"] + list(args), cwd=cwd, env=env
    )
    return result.decode()


def call(result: _Sequence[_ods_ir.Type], callee: _Union[str, _ods_ir.FlatSymbolRefAttr], operands_: _Sequence[_ods_ir.Value], *, arg_attrs: _Optional[_Union[_Any, _ods_ir.ArrayAttr]] = None, res_attrs: _Optional[_Union[_Any, _ods_ir.ArrayAttr]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _Union[_ods_ir.OpResult, _ods_ir.OpResultList, CallOp]:
  op = CallOp(result=result, callee=callee, operands_=operands_, arg_attrs=arg_attrs, res_attrs=res_attrs, loc=loc, ip=ip); results = op.results
  return results if len(results) > 1 else (results[0] if len(results) == 1 else op)


def call(result: _Sequence[_ods_ir.Type], callee: _Union[str, _ods_ir.FlatSymbolRefAttr], operands_: _Sequence[_ods_ir.Value], *, arg_attrs: _Optional[_Union[_Any, _ods_ir.ArrayAttr]] = None, res_attrs: _Optional[_Union[_Any, _ods_ir.ArrayAttr]] = None, no_inline: _Optional[bool] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _Union[_ods_ir.OpResult, _ods_ir.OpResultList, CallOp]:
  op = CallOp(result=result, callee=callee, operands_=operands_, arg_attrs=arg_attrs, res_attrs=res_attrs, no_inline=no_inline, loc=loc, ip=ip); results = op.results
  return results if len(results) > 1 else (results[0] if len(results) == 1 else op)


def call(result: _Optional[_ods_ir.Type], callee_operands: _Sequence[_ods_ir.Value], op_bundle_operands: _Sequence[_ods_ir.Value], op_bundle_sizes: _Union[_Sequence[int], _ods_ir.DenseI32ArrayAttr], *, var_callee_type: _Optional[_Union[_Any, _ods_ir.TypeAttr]] = None, callee: _Optional[_Union[str, _ods_ir.FlatSymbolRefAttr]] = None, fastmath_flags: _Optional[_Union[_Any, _ods_ir.Attribute]] = None, c_conv: _Optional[_Union[_Any, _ods_ir.Attribute]] = None, tail_call_kind: _Optional[_Union[_Any, _ods_ir.Attribute]] = None, memory_effects: _Optional[_Union[_Any, _ods_ir.Attribute]] = None, convergent: _Optional[bool] = None, no_unwind: _Optional[bool] = None, will_return: _Optional[bool] = None, noreturn: _Optional[bool] = None, returns_twice: _Optional[bool] = None, hot: _Optional[bool] = None, cold: _Optional[bool] = None, noduplicate: _Optional[bool] = None, no_caller_saved_registers: _Optional[bool] = None, nocallback: _Optional[bool] = None, modular_format: _Optional[_Union[str, _ods_ir.StringAttr]] = None, nobuiltins: _Optional[_Union[_Sequence[_ods_ir.Attribute], _ods_ir.ArrayAttr]] = None, allocsize: _Optional[_Union[_Sequence[int], _ods_ir.DenseI32ArrayAttr]] = None, optsize: _Optional[bool] = None, minsize: _Optional[bool] = None, builtin: _Optional[bool] = None, nobuiltin: _Optional[bool] = None, save_reg_params: _Optional[bool] = None, zero_call_used_regs: _Optional[_Union[str, _ods_ir.StringAttr]] = None, trap_func_name: _Optional[_Union[str, _ods_ir.StringAttr]] = None, default_func_attrs: _Optional[_Union[dict, _ods_ir.DictAttr]] = None, op_bundle_tags: _Optional[_Union[_Sequence[_ods_ir.Attribute], _ods_ir.ArrayAttr]] = None, arg_attrs: _Optional[_Union[_Any, _ods_ir.ArrayAttr]] = None, res_attrs: _Optional[_Union[_Any, _ods_ir.ArrayAttr]] = None, no_inline: _Optional[bool] = None, always_inline: _Optional[bool] = None, inline_hint: _Optional[bool] = None, access_groups: _Optional[_Union[_Any, _ods_ir.ArrayAttr]] = None, alias_scopes: _Optional[_Union[_Any, _ods_ir.ArrayAttr]] = None, noalias_scopes: _Optional[_Union[_Any, _ods_ir.ArrayAttr]] = None, tbaa: _Optional[_Union[_Any, _ods_ir.ArrayAttr]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _Union[_ods_ir.OpResult, _ods_ir.OpResultList, CallOp]:
  op = CallOp(result=result, callee_operands=callee_operands, op_bundle_operands=op_bundle_operands, op_bundle_sizes=op_bundle_sizes, var_callee_type=var_callee_type, callee=callee, fastmathFlags=fastmath_flags, CConv=c_conv, TailCallKind=tail_call_kind, memory_effects=memory_effects, convergent=convergent, no_unwind=no_unwind, will_return=will_return, noreturn=noreturn, returns_twice=returns_twice, hot=hot, cold=cold, noduplicate=noduplicate, no_caller_saved_registers=no_caller_saved_registers, nocallback=nocallback, modular_format=modular_format, nobuiltins=nobuiltins, allocsize=allocsize, optsize=optsize, minsize=minsize, builtin=builtin, nobuiltin=nobuiltin, save_reg_params=save_reg_params, zero_call_used_regs=zero_call_used_regs, trap_func_name=trap_func_name, default_func_attrs=default_func_attrs, op_bundle_tags=op_bundle_tags, arg_attrs=arg_attrs, res_attrs=res_attrs, no_inline=no_inline, always_inline=always_inline, inline_hint=inline_hint, access_groups=access_groups, alias_scopes=alias_scopes, noalias_scopes=noalias_scopes, tbaa=tbaa, loc=loc, ip=ip); results = op.results
  return results if len(results) > 1 else (results[0] if len(results) == 1 else op)


def call(result: _Sequence[_ods_ir.Type], tensors: _Sequence[_ods_ir.Value], callee: _Union[str, _ods_ir.FlatSymbolRefAttr], *, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _Union[_ods_ir.OpResult, _ods_ir.OpResultList, CallOp]:
  op = CallOp(result=result, tensors=tensors, callee=callee, loc=loc, ip=ip); results = op.results
  return results if len(results) > 1 else (results[0] if len(results) == 1 else op)


def call(exported: Exported) -> Callable[..., typing.Array]:
  if not isinstance(exported, Exported):
    raise ValueError(
      "The exported argument must be an export.Exported. "
      f"Found {exported}.")
  @custom_derivatives.custom_vjp
  def f_flat(*args_flat):
    return call_exported_p.bind(*args_flat, exported=exported)

  def f_flat_vjp_fwd(*args_flat):
    # Return the primal arguments as the residual
    # TODO: keep as residuals only the arguments that are needed
    return f_flat(*args_flat), args_flat

  def f_flat_vjp_bwd(residual, ct_res_flat):
    args_flat = residual  # residual is the primal argument flat tuple
    exp_vjp = exported.vjp()
    # ct_res_flat may contain arrays of zeros where exp_vjp expect float0.
    # We make the proper arrays of float0 to invoke exp_vjp.
    def fix_float0_ct(ct_res, expected_aval):
      if expected_aval.dtype != dtypes.float0:
        return ct_res
      return ad_util.zeros_like_jaxval(ct_res)

    ct_res_fixed = map(fix_float0_ct,
                       ct_res_flat, exp_vjp.in_avals[len(args_flat):])
    in_ct_flat = call_exported(exp_vjp)(*args_flat, *ct_res_fixed)
    return in_ct_flat

  f_flat.defvjp(f_flat_vjp_fwd, f_flat_vjp_bwd)

  def f_imported(*args, **kwargs):
    # since custom_vjp does not support kwargs, flatten the function first.
    args_flat, in_tree = tree_util.tracing_registry.flatten((args, kwargs))
    if in_tree != exported.in_tree:
      # Give errors with the precise tree difference; use fake leaves so we can
      # use tree_util.equality_errors.
      in_args = in_tree.unflatten([0] * in_tree.num_leaves)
      exp_in_args = exported.in_tree.unflatten([0] * exported.in_tree.num_leaves)

      msg = (
          "The invocation args and kwargs must have the same pytree structure "
          f"as when the function '{exported.fun_name}' was exported, but they "
          "have the following structural differences:\n" +
          ("\n".join(
             f"   - {shape_poly.args_kwargs_path_to_str(path)} is a {thing1} in the invocation and a "
             f"{thing2} when exported, so {explanation}.\n"
             for path, thing1, thing2, explanation
             in tree_util.equality_errors(in_args, exp_in_args))))
      raise ValueError(msg)

    res_flat = f_flat(*args_flat)
    return exported.out_tree.unflatten(res_flat)
  return f_imported


def call(
  graphdef_state: tuple[GraphDef[A], State], /
) -> ApplyCaller[tuple[GraphDef[A], State]]:
  """Calls a method underlying graph node defined by a (GraphDef, State) pair.

  ``call`` takes a ``(GraphDef, State)`` pair and creates a proxy object that can be
  used to call methods on the underlying graph node. When a method is called, the
  output is returned along with a new (GraphDef, State) pair that represents the
  updated state of the graph node. ``call`` is equivalent to :func:`merge` > ``method``
  > :func:`split` but is more convenient to use in pure JAX functions.

  Example::

    >>> from flax import nnx
    >>> import jax
    >>> import jax.numpy as jnp
    ...
    >>> class StatefulLinear(nnx.Module):
    ...   def __init__(self, din, dout, rngs):
    ...     self.w = nnx.Param(jax.random.uniform(rngs(), (din, dout)))
    ...     self.b = nnx.Param(jnp.zeros((dout,)))
    ...     self.count = Variable(jnp.array(0, dtype=jnp.uint32))
    ...
    ...   def increment(self):
    ...     self.count[...] += 1
    ...
    ...   def __call__(self, x):
    ...     self.increment()
    ...     return x @ self.w + self.b
    ...
    >>> linear = StatefulLinear(3, 2, nnx.Rngs(0))
    >>> linear_state = nnx.split(linear)
    ...
    >>> @jax.jit
    ... def forward(x, linear_state):
    ...   y, linear_state = nnx.call(linear_state)(x)
    ...   return y, linear_state
    ...
    >>> x = jnp.ones((1, 3))
    >>> y, linear_state = forward(x, linear_state)
    >>> y, linear_state = forward(x, linear_state)
    ...
    >>> linear = nnx.merge(*linear_state)
    >>> linear.count[...]
    Array(2, dtype=uint32)

  The proxy object returned by ``call`` supports indexing and attribute access
  to access nested methods. In the example below, the ``increment`` method indexing
  is used to call the ``increment`` method of the ``StatefulLinear`` module
  at the ``b`` key of a ``nodes`` dictionary.

    >>> class StatefulLinear(nnx.Module):
    ...   def __init__(self, din, dout, rngs):
    ...     self.w = nnx.Param(jax.random.uniform(rngs(), (din, dout)))
    ...     self.b = nnx.Param(jnp.zeros((dout,)))
    ...     self.count = nnx.Variable(jnp.array(0, dtype=jnp.uint32))
    ...
    ...   def increment(self):
    ...     self.count[...] += 1
    ...
    ...   def __call__(self, x):
    ...     self.increment()
    ...     return x @ self.w + self.b
    ...
    >>> rngs = nnx.Rngs(0)
    >>> nodes = dict(
    ...   a=StatefulLinear(3, 2, rngs),
    ...   b=StatefulLinear(2, 1, rngs),
    ... )
    ...
    >>> node_state = nnx.split(nodes)
    >>> # use attribute access
    >>> _, node_state = nnx.call(node_state)['b'].increment()
    ...
    >>> nodes = nnx.merge(*node_state)
    >>> nodes['a'].count[...]
    Array(0, dtype=uint32)
    >>> nodes['b'].count[...]
    Array(1, dtype=uint32)
  """

  def pure_caller(accessor: DelayedAccessor, *args, **kwargs):
    node = merge(*graphdef_state)
    method = accessor(node)
    out = method(*args, **kwargs)
    return out, split(node)

  return CallableProxy(pure_caller)  # type: ignore

