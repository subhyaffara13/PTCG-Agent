
def backward_pass(jaxpr, transform_stack: bool, consts, primals_in, cts_in):
  primals_in = [ValAccum(x.aval) if isinstance(x, UndefinedPrimal) else x
                for x in primals_in]
  backward_pass3(jaxpr, transform_stack, consts, primals_in, cts_in)
  return [x.freeze() if isinstance(x, ValAccum) else p2cz(x)
          for x in primals_in]

