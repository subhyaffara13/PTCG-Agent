from typing import List

def mask(cfvalues: np.ndarray, infoset: List[InfostateNode], num_actions: int,
         batch_size: int) -> np.ndarray:
  """Returns counterfactual values of legal actions and put 0 for illegal ones.

  Args:
    cfvalues: Numpy array of counterfactual values.
    infoset: List of information states.
    num_actions: Number of possible actions to take.
    batch_size: Batch size.

  Returns:
    Masked counterfactual values. The counterfactual values of legal actions are
    kept as passed to this function and for illegal actions, we consider 0
    counterfactual value.
  """
  legal_actions = [[infoset[i].world_state.state.legal_actions()] *
                   cfvalues.shape[1] for i in range(batch_size)]

  masked_cfvalues = np.zeros(shape=[batch_size, cfvalues.shape[1], num_actions])
  for i in range(cfvalues.shape[0]):
    for j in range(cfvalues.shape[1]):
      np.put(masked_cfvalues[i][j], legal_actions[i][j], cfvalues[i][j])

  return np.stack(masked_cfvalues)


def mask(results_: _Sequence[_ods_ir.Type], mask: _ods_ir.Value[_ods_ir.VectorType], *, passthru: _Optional[_ods_ir.Value] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _Union[_ods_ir.OpResult, _ods_ir.OpResultList, MaskOp]:
  op = MaskOp(results_=results_, mask=mask, passthru=passthru, loc=loc, ip=ip); results = op.results
  return results if len(results) > 1 else (results[0] if len(results) == 1 else op)

