import random

def _sample_weighted(iterator, k, weights, strict):
    # Implementation of "A-ExpJ" from the 2006 paper by Efraimidis et al. :
    # "Weighted random sampling with a reservoir".

    # Log-transform for numerical stability for weights that are small/large
    weight_keys = (log(random()) / weight for weight in weights)

    # Fill up the reservoir (collection of samples) with the first `k`
    # weight-keys and elements, then heapify the list.
    reservoir = take(k, zip(weight_keys, iterator))
    if strict and len(reservoir) < k:
        raise ValueError('Sample larger than population')

    heapify(reservoir)

    # The number of jumps before changing the reservoir is a random variable
    # with an exponential distribution. Sample it using random() and logs.
    smallest_weight_key, _ = reservoir[0]
    weights_to_skip = log(random()) / smallest_weight_key

    for weight, element in zip(weights, iterator):
        if weight >= weights_to_skip:
            # The notation here is consistent with the paper, but we store
            # the weight-keys in log-space for better numerical stability.
            smallest_weight_key, _ = reservoir[0]
            t_w = exp(weight * smallest_weight_key)
            r_2 = uniform(t_w, 1)  # generate U(t_w, 1)
            weight_key = log(r_2) / weight
            heapreplace(reservoir, (weight_key, element))
            smallest_weight_key, _ = reservoir[0]
            weights_to_skip = log(random()) / smallest_weight_key
        else:
            weights_to_skip -= weight

    ret = [element for weight_key, element in reservoir]
    shuffle(ret)
    return ret

