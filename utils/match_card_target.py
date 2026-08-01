
def match_card_target(target_str, options, my_hand):
    for i, opt in enumerate(options):
        opt_type = opt.get("type")
        if opt_type in (7, 8, 9):
            hand_idx = opt.get("index", -1)
            if 0 <= hand_idx < len(my_hand) and str(my_hand[hand_idx]) == target_str:
                return [i]
    if target_str.isdigit():
        idx = int(target_str)
        if 0 <= idx < len(options):
            return [idx]
    return None

