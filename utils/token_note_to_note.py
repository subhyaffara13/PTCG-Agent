
def token_note_to_note(number, current_velocity, default_velocity, note_onsets_ready, current_idx, notes):
    if note_onsets_ready[number] is not None:
        # offset with onset
        onset_idx = note_onsets_ready[number]
        if onset_idx < current_idx:
            # Time shift after previous note_on
            offset_idx = current_idx
            notes.append([onset_idx, offset_idx, number, default_velocity])
            onsets_ready = None if current_velocity == 0 else current_idx
            note_onsets_ready[number] = onsets_ready
    else:
        note_onsets_ready[number] = current_idx
    return notes

