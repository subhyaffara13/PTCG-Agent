
def if_(validator, if_schema, instance, schema):
    if validator.evolve(schema=if_schema).is_valid(instance):
        if "then" in schema:
            then = schema["then"]
            yield from validator.descend(instance, then, schema_path="then")
    elif "else" in schema:
        else_ = schema["else"]
        yield from validator.descend(instance, else_, schema_path="else")


def if_(result: _Sequence[_ods_ir.Type], pred: _ods_ir.Value[_ods_ir.RankedTensorType], *, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _Union[_ods_ir.OpResult, _ods_ir.OpResultList, IfOp]:
  op = IfOp(result=result, pred=pred, loc=loc, ip=ip); results = op.results
  return results if len(results) > 1 else (results[0] if len(results) == 1 else op)


def if_(results_: _Sequence[_ods_ir.Type], condition: _ods_ir.Value[_ods_ir.IntegerType], *, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _Union[_ods_ir.OpResult, _ods_ir.OpResultList, IfOp]:
  op = IfOp(results_=results_, condition=condition, loc=loc, ip=ip); results = op.results
  return results if len(results) > 1 else (results[0] if len(results) == 1 else op)


def if_(result: _Sequence[_ods_ir.Type], pred: _ods_ir.Value[_ods_ir.RankedTensorType], *, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _Union[_ods_ir.OpResult, _ods_ir.OpResultList, IfOp]:
  op = IfOp(result=result, pred=pred, loc=loc, ip=ip); results = op.results
  return results if len(results) > 1 else (results[0] if len(results) == 1 else op)

