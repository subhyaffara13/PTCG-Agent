
def marginrankingloss_reference(input1, input2, target, margin=0, reduction='mean'):
    output = (-target * (input1 - input2) + margin).clamp(min=0)
    if reduction == 'mean':
        return output.mean()
    elif reduction == 'sum':
        return output.sum()
    return output

