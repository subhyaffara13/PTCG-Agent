
def pp_ref_transforms(context: core.JaxprPpContext, ref, transforms=()):
  if isinstance(ref, TransformedRef):
    transforms = ref.transforms
    ref = ref.ref
  if isinstance(ref, tuple):
    ref_doc = pp.concat([
        pp.text("("),
        pp.join(pp.text(", "), [pp_ref_transforms(context, r) for r in ref]),
        pp.text(")"),
    ])
  else:
    ref_doc = core.pp_var(ref, context)
  return pp_ref_var(
      pp.concat([
          ref_doc,
          _pp_transforms(context, transforms),
      ])
  )

