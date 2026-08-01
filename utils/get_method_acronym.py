
def get_method_acronym(method):
  """Gets pretty acronym for specified ResponseGraphUCB method."""
  if method == 'uniform-exhaustive':
    return r'$\mathcal{S}$: UE'
  elif method == 'uniform':
    return r'$\mathcal{S}$: U'
  elif method == 'valence-weighted':
    return r'$\mathcal{S}$: VW'
  elif method == 'count-weighted':
    return r'$\mathcal{S}$: CW'
  elif method == 'ucb-standard':
    return r'$\mathcal{C}(\delta)$: UCB'
  elif method == 'ucb-standard-relaxed':
    return r'$\mathcal{C}(\delta)$: R-UCB'
  elif method == 'clopper-pearson-ucb':
    return r'$\mathcal{C}(\delta)$: CP-UCB'
  elif method == 'clopper-pearson-ucb-relaxed':
    return r'$\mathcal{C}(\delta)$: R-CP-UCB'
  elif method == 'fixedbudget-uniform':
    return r'$\mathcal{S}$: U, $\mathcal{C}(\delta)$: FB'
  else:
    raise ValueError('Unknown sampler method: {}!'.format(method))

