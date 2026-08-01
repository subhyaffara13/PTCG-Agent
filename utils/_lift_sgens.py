
def _lift_sgens(size, fixed_slots, free, s):
    a = []
    j = k = 0
    fd = [y for _, y in sorted(zip(fixed_slots, free))]
    num_free = len(free)
    for i in range(size):
        if i in fixed_slots:
            a.append(fd[k])
            k += 1
        else:
            a.append(s[j] + num_free)
            j += 1
    return a

