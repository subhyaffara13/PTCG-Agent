
def cross_entropy_loss_reference(input, target, weight=None, ignore_index=-100, reduction='mean',
                                 label_smoothing=0.0):
    if input.shape == target.shape:
        return cross_entropy_loss_prob_target_reference(
            input,
            target,
            weight=weight,
            reduction=reduction,
            label_smoothing=label_smoothing)
    else:
        return cross_entropy_loss_indices_target_reference(
            input, target, weight=weight, reduction=reduction,
            ignore_index=ignore_index, label_smoothing=label_smoothing
        )

