import itertools

def get_method_tuple_linespecs(method):
  """Gets plot linespecs for the specified ResponseGraphUCB method."""
  sampling_strats = [
      'uniform-exhaustive', 'uniform', 'valence-weighted', 'count-weighted'
  ]
  conf_methods = ['ucb-standard', 'clopper-pearson-ucb']
  method_to_id_map = dict(
      (m, i)
      for i, m in enumerate(itertools.product(sampling_strats, conf_methods)))

  # Create palette
  num_colors = len(method_to_id_map.keys())
  colors = plt.get_cmap('Set1', num_colors).colors

  # Spec out the linestyle
  base_method = (method[0], method[1].replace('-relaxed', '')
                )  # Method name without -relaxed suffix
  linespecs = {
      'color': colors[method_to_id_map[base_method]]
  }  # Use base method for color (ignoring relaxed vs non-relaxed)
  if 'relaxed' in method[1]:  # Use actual method for linestyle
    linespecs['linestyle'] = 'dashed'
  else:
    linespecs['linestyle'] = 'solid'

  return linespecs

