
def _check_input_constraints_pre_hook(self, args, kwargs):
    # preserve current behavior for clients that do not want any validation
    if not self.validate_inputs:
        return

    # when a guards function exists, assume that the graph does calls it!
    # so we do not need to check input constraints...but we still want
    # to check inputs match, otherwise we'd get obscure pytree errors
    if hasattr(self, "_guards_fn"):
        _check_inputs_match(args, kwargs, self._in_spec)
        return

    # NOTE: for some reason, Dynamo is tracing into this, we should see why and
    # put compile at the right place. Until then, we can skip the input
    # constraint checks.
    if not torch.compiler.is_dynamo_compiling():
        _check_input_constraints_for_module(self, args, kwargs)

