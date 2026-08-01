
def softmax_projection(logits):
  max_l = max(logits)
  exp_l = [np.exp(l - max_l) for l in logits]
  norm_exp = sum(exp_l)
  return [l / norm_exp for l in exp_l]

