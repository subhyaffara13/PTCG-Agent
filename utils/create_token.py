
def create_token(*, results: _Optional[_Sequence[_ods_ir.Type]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult:
  return CreateTokenOp(results=results, loc=loc, ip=ip).result


def create_token(*, results: _Optional[_Sequence[_ods_ir.Type]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult:
  return CreateTokenOp(results=results, loc=loc, ip=ip).result


def create_token(_=None):
  """Creates an XLA token value with no preconditions for sequencing effects.

  Experimental.

  The argument is ignored. It exists for backward compatibility.
  """
  return create_token_p.bind()

