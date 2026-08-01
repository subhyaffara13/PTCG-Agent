
def _multimarginloss_reference(input, target_idx, p, margin, weight):
    if weight is None:
        weight = input.new(len(input)).fill_(1)

    output = 0
    for i in range(len(input)):
        if i != target_idx:
            output += weight[target_idx] * (max(0, (margin - input[target_idx] + input[i])) ** p)
    return output

