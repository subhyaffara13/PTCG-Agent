
def register_prng(impl: PRNGImpl):
  if impl.name in prngs:
    raise ValueError(f'PRNG with name {impl.name} already registered: {impl}')
  prngs[impl.name] = impl

