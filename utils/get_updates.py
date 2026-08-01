
def get_updates(
    params,
    muon_weight_dimension_numbers=UNSPECIFIED,
    preconditioning='frobenius',
):
  if muon_weight_dimension_numbers is UNSPECIFIED:
    opt = _muon.muon(learning_rate=1e-3, preconditioning=preconditioning)
  else:
    opt = _muon.muon(
        learning_rate=1e-3,
        preconditioning=preconditioning,
        muon_weight_dimension_numbers=muon_weight_dimension_numbers
    )
  state = opt.init(params)
  # assume loss = 1/2 * sum(params ** 2)
  grad = params
  updates, state = opt.update(grad, state, params=params)
  return updates, state

