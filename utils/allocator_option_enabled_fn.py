
def allocator_option_enabled_fn(allocator_config, _, option):
    if allocator_config is None:
        return False
    allocator_config = allocator_config.split(',') if ',' in allocator_config else [allocator_config]
    mapping = dict([var.split(':') for var in allocator_config])

    if option in mapping and mapping[option] == 'True':
        return True
    else:
        return False

