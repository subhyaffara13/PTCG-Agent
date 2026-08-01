
def pretty_top10_preds_str(predictions, indices, max_weight=1.01):
  """Pretty string representation of the top 10 predictions."""

  top_10_preds = ""
  sum_weight = 0
  for i in range(10):
    pred_idx = indices[42 - i]
    weight = predictions[pred_idx]
    bar_width = int(weight / 0.01)
    bar_str = "#" * bar_width
    top_10_preds += f"  {pred_idx:2d}: {weight:.5f} {bar_str}\n"
    sum_weight += weight
    if sum_weight > max_weight:
      break
  return top_10_preds

