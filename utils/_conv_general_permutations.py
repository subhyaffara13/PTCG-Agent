
def _conv_general_permutations(dimension_numbers):
  lhs_spec, rhs_spec, out_spec = dimension_numbers
  rhs_perm = ((rhs_spec.index('O'), rhs_spec.index('I'))
              + tuple(i for i, c in enumerate(rhs_spec) if c not in {'O', 'I'}))
  lhs_perm = ((lhs_spec.index('N'), lhs_spec.index('C'))
              + tuple(sorted((i for i, c in enumerate(lhs_spec)
                              if c not in {'N', 'C'}),
                             key=lambda i: rhs_spec.index(lhs_spec[i]))))
  out_perm = ((out_spec.index('N'), out_spec.index('C'))
              + tuple(sorted((i for i, c in enumerate(out_spec)
                              if c not in {'N', 'C'}),
                             key=lambda i: rhs_spec.index(out_spec[i]))))
  return lhs_perm, rhs_perm, out_perm

