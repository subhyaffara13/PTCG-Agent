
def _converted_mutables_add_params(
    n, *, donated_invars, in_shardings, in_layouts, **params):
  donated_invars = (False,) * n + donated_invars
  in_shardings = (UNSPECIFIED,) * n + in_shardings
  in_layouts = (None,) * n + in_layouts
  return dict(params, donated_invars=donated_invars, in_shardings=in_shardings,
              in_layouts=in_layouts)

