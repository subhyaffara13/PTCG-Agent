
def partial_eval_jaxpr_nounits(
    jaxpr: ClosedJaxpr, unknowns: Sequence[bool],
    instantiate: bool | Sequence[bool],
  ) -> tuple[ClosedJaxpr, ClosedJaxpr, list[bool], list[AbstractValue]]:
  """Unzip a jaxpr in two by data dependence into 'known' and 'unknown' parts.

  That is, given a jaxpr and a sequence of booleans indicating which jaxpr
  inputs (i.e. invars) are considered unknown, produce two jaxprs, a list of
  booleans representing which of the original jaxpr's outputs are unknown (i.e.
  have a data dependence on an unknown input), and a list of abstract values
  representing residuals (part of the first jaxpr's output and the second
  jaxpr's input). The two jaxprs result from partitioning the original jaxpr's
  first-order primitive applications based on whether all the inputs to the
  application are known (in which case the application is represented in the
  'known' jaxpr and its result is considered known) or whether any inputs to the
  application are unknown (in which case the application is represented in the
  'unknown' jaxpr and its result is considered unknown). Higher-order primitives
  are recursively unzipped in two.

  The `instantiate` argument can be used to ensure some outputs are lifted into
  the 'unknown' jaxpr.

  For example, give an input jaxpr:

    { lambda ; a:f32[] b:f32[]. let
        c:f32[] = cos a
        d:f32[] = sin a
        e:f32[] = neg d
        f:f32[] = mul e b
      in (c, f) }

  then applying this function with `unknowns=[False, True]` and
  `instantiate=False` produces as an output triple:

    # jaxpr_known
    { lambda ; a:f32[]. let
       b:f32[] = cos a
       c:f32[] = sin a
       d:f32[] = neg c
     in (b, d) }

    # jaxpr_unknown
    { lambda ; a:f32[] b:f32[]. let c:f32[] = mul b a in (c,) }

    # out_unknowns
    [False, True]

  Notice in particular that the first output (jaxpr_known) contains all the
  primitive applications which do not have a data dependence on an unknown
  input. Also notice the input and output types: the input type of the first
  jaxpr produced represents the type of the known inputs of the original jaxpr,
  and the output type of the second jaxpr produced represents the type of the
  unknown outputs of the original jaxpr.

  In the above example, the output of jaxpr_known named `d` is a _residual_
  output, and corresponds to the input named `a` in jaxpr_unknown. In general,
  jaxpr_known will produce extra outputs (at the end of its output list)
  corresponding to intermediate values of the original jaxpr which must be
  passed to jaxpr_unknown (as leading inputs).
  """
  instantiate = tuple(instantiate) if isinstance(instantiate, list) else instantiate
  return _partial_eval_jaxpr_nounits(jaxpr, tuple(unknowns), instantiate, False)[:-1]

