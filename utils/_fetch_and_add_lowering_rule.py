from typing import Any

def _fetch_and_add_lowering_rule(ctx: sc_lowering.LoweringRuleContext, *args):
  del ctx  # Unused.
  x_ref, value, *indices, subcore_id = args
  kwargs: dict[str, Any] = {}
  if "core_type" in inspect.signature(tpu.fetch_and_add_sync).parameters:
    kwargs = {"core_type": ir.Attribute.parse("#tpu.core_type<sc_vector_subcore>")}
  return tpu.fetch_and_add_sync(x_ref, indices, value, core_id=subcore_id, **kwargs)

