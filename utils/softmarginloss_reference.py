
def softmarginloss_reference(input, target, reduction='mean'):
    output = (1 + (-input * target).exp()).log()

    if reduction == 'mean':
        return output.mean()
    elif reduction == 'sum':
        return output.sum()
    return output

