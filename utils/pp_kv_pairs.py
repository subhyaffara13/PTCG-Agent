
def pp_kv_pairs(kv_pairs, context: JaxprPpContext, settings: JaxprPpSettings) -> pp.Doc:
  if not kv_pairs:
    return pp.nil()
  return pp.group(pp.concat([
    pp.nest(2, pp.concat([
      pp.text("["),  pp.brk(""),
      pp.join(pp.brk(), [pp_kv_pair(k, v, context, settings) for k, v in kv_pairs])
    ])),
    pp.brk(""), pp.text("]")
  ]))

