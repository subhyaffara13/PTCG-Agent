
def _traced_args_info(self):
  don8_rgn = tuple(i for i, d in enumerate(self._params['donated_invars']) if d)
  arg_avals = self.jaxpr.in_avals[self._num_consts:]
  return make_args_info(self._in_tree, arg_avals, don8_rgn)

