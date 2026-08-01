
def invoke(f, /, *args, **kwargs):
    """
    Call a function for its side effect after initialization.

    The benefit of using the decorator instead of simply invoking a function
    after defining it is that it makes explicit the author's intent for the
    function to be called immediately. Whereas if one simply calls the
    function immediately, it's less obvious if that was intentional or
    incidental. It also avoids repeating the name - the two actions, defining
    the function and calling it immediately are modeled separately, but linked
    by the decorator construct.

    The benefit of having a function construct (opposed to just invoking some
    behavior inline) is to serve as a scope in which the behavior occurs. It
    avoids polluting the global namespace with local variables, provides an
    anchor on which to attach documentation (docstring), keeps the behavior
    logically separated (instead of conceptually separated or not separated at
    all), and provides potential to re-use the behavior for testing or other
    purposes.

    This function is named as a pithy way to communicate, "call this function
    primarily for its side effect", or "while defining this function, also
    take it aside and call it". It exists because there's no Python construct
    for "define and call" (nor should there be, as decorators serve this need
    just fine). The behavior happens immediately and synchronously.

    >>> @invoke
    ... def func(): print("called")
    called
    >>> func()
    called

    Use functools.partial to pass parameters to the initial call

    >>> @functools.partial(invoke, name='bingo')
    ... def func(name): print('called with', name)
    called with bingo
    """
    f(*args, **kwargs)
    return f


def invoke(result: _Optional[_ods_ir.Type], callee_operands: _Sequence[_ods_ir.Value], normal_dest_operands: _Sequence[_ods_ir.Value], unwind_dest_operands: _Sequence[_ods_ir.Value], op_bundle_operands: _Sequence[_ods_ir.Value], op_bundle_sizes: _Union[_Sequence[int], _ods_ir.DenseI32ArrayAttr], normal_dest: _ods_ir.Block, unwind_dest: _ods_ir.Block, *, var_callee_type: _Optional[_Union[_Any, _ods_ir.TypeAttr]] = None, callee: _Optional[_Union[str, _ods_ir.FlatSymbolRefAttr]] = None, arg_attrs: _Optional[_Union[_Any, _ods_ir.ArrayAttr]] = None, res_attrs: _Optional[_Union[_Any, _ods_ir.ArrayAttr]] = None, branch_weights: _Optional[_Union[_Sequence[int], _ods_ir.DenseI32ArrayAttr]] = None, c_conv: _Optional[_Union[_Any, _ods_ir.Attribute]] = None, op_bundle_tags: _Optional[_Union[_Sequence[_ods_ir.Attribute], _ods_ir.ArrayAttr]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _Union[_ods_ir.OpResult, _ods_ir.OpResultList, InvokeOp]:
  op = InvokeOp(result=result, callee_operands=callee_operands, normalDestOperands=normal_dest_operands, unwindDestOperands=unwind_dest_operands, op_bundle_operands=op_bundle_operands, op_bundle_sizes=op_bundle_sizes, normalDest=normal_dest, unwindDest=unwind_dest, var_callee_type=var_callee_type, callee=callee, arg_attrs=arg_attrs, res_attrs=res_attrs, branch_weights=branch_weights, CConv=c_conv, op_bundle_tags=op_bundle_tags, loc=loc, ip=ip); results = op.results
  return results if len(results) > 1 else (results[0] if len(results) == 1 else op)

