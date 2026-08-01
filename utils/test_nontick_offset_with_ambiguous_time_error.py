
def test_nontick_offset_with_ambiguous_time_error(original_dt, target_dt, offset, tz):
    # .apply for non-Tick offsets throws ValueError when the target dt
    # is dst-ambiguous
    localized_dt = original_dt.tz_localize(tz)

    msg = f"Cannot infer dst time from {target_dt}, try using the 'ambiguous' argument"
    with pytest.raises(ValueError, match=msg):
        localized_dt + offset

