
def token_time_to_note(number, cutoff_time_idx, current_idx):
    current_idx += number
    if cutoff_time_idx is not None:
        current_idx = min(current_idx, cutoff_time_idx)

    return current_idx

