
def cosineembeddingloss_reference(input1, input2, target, margin=0, reduction='mean'):
    def _cos(a, b):
        cos = a.new(a.size(0))
        for i in range(a.size(0)):
            cos[i] = (a[i] * b[i]).sum() / ((((a[i] * a[i]).sum() + 1e-12) * ((b[i] * b[i]).sum() + 1e-12)) ** 0.5)
        return cos

    output = torch.where(target == 1, 1 - _cos(input1, input2), (_cos(input1, input2) - margin).clamp(min=0))

    if reduction == 'mean':
        return output.mean()
    elif reduction == 'sum':
        return output.sum()
    return output

