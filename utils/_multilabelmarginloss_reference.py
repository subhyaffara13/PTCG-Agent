
def _multilabelmarginloss_reference(input, target):
    targets = []
    for target_index in target:
        if target_index < 0:
            break
        targets.append(target_index)

    sum = 0
    for target_index in targets:
        for i in range(len(input)):
            if i not in targets:
                sum += max(0, 1 - input[target_index] + input[i])

    return sum

