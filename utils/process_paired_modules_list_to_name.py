
def process_paired_modules_list_to_name(model, paired_modules_list):
    """Processes a list of paired modules to a list of names of paired modules."""

    for group in paired_modules_list:
        for i, item in enumerate(group):
            if isinstance(item, torch.nn.Module):
                group[i] = get_name_by_module(model, item)
            elif not isinstance(item, str):
                raise TypeError("item must be a nn.Module or a string")
    return paired_modules_list

