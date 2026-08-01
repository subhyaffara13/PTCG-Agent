
def multiclass_logistic_loss(logits, labels):
  return softmax_cross_entropy_with_integer_labels(logits, labels)

