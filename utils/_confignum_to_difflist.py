
def _confignum_to_difflist(config_num, diff, list_len):
    # Determines configuration of diffs into list_len number of slots
    diff_list = []
    for n in range(list_len):
        prev_diff = diff
        # Number of spots after current one
        rem_spots = list_len - n - 1
        # Number of configurations of distributing diff among the remaining spots
        rem_configs = binomial(diff + rem_spots - 1, diff)
        while config_num >= rem_configs:
            config_num -= rem_configs
            diff -= 1
            rem_configs = binomial(diff + rem_spots - 1, diff)
        diff_list.append(prev_diff - diff)
    return diff_list

