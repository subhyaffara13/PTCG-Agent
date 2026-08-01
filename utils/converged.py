
def converged(curr_modules, prev_modules, threshold=1e-4):
    """Test whether modules are converged to a specified threshold.

    Tests for the summed norm of the differences between each set of modules
    being less than the given threshold

    Takes two dictionaries mapping names to modules, the set of names for each dictionary
    should be the same, looping over the set of names, for each name take the difference
    between the associated modules in each dictionary

    """
    if curr_modules.keys() != prev_modules.keys():
        raise ValueError(
            "The keys to the given mappings must have the same set of names of modules"
        )

    summed_norms = torch.tensor(0.0)
    if None in prev_modules.values():
        return False
    for name in curr_modules:
        curr_weight = get_module_weight(curr_modules[name])
        prev_weight = get_module_weight(prev_modules[name])

        difference = curr_weight.sub(prev_weight)
        summed_norms += torch.norm(difference)
    return bool(summed_norms < threshold)

