
def kldivloss_reference(input, target, reduction='mean', log_target=False):
    if log_target:
        result = torch.exp(target) * (target - input)
    else:
        result = target * (target.log() - input)
    if reduction == 'mean':
        return result.mean()
    elif reduction == 'sum':
        return result.sum()
    elif reduction == 'batchmean' and result.dim() != 0:
        return result.sum() / result.size(0)
    return result

