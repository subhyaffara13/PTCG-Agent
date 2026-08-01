
def reference_mse_loss(input, target, reduction="mean"):
    se = (input - target) ** 2
    if reduction == "mean":
        return np.mean(se)
    elif reduction == "sum":
        return np.sum(se)
    else:  # reduction == "none"
        return se

