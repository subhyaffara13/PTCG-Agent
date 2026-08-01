
def remat_partial_eval_custom_params_updater(*args):
  unks_in, inst_in, *_, params_known, params_staged = args
  prevent_cse = params_known['prevent_cse']
  assert prevent_cse == params_staged['prevent_cse']
  if isinstance(prevent_cse, tuple):
    prevent_cse_known, _ = partition_list(unks_in, prevent_cse)
    _, prevent_cse_staged = partition_list(inst_in, prevent_cse)
    params_known = dict(params_known, prevent_cse=tuple(prevent_cse_known))
    params_staged = dict(params_staged, prevent_cse=tuple(prevent_cse_staged))
  return params_known, dict(params_staged, differentiated=True)

