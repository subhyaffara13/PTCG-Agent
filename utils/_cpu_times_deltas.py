
def _cpu_times_deltas(t1, t2):
    assert t1._fields == t2._fields, (t1, t2)
    field_deltas = []
    for field in _ntp.scputimes._fields:
        field_delta = getattr(t2, field) - getattr(t1, field)
        # CPU times are always supposed to increase over time
        # or at least remain the same and that's because time
        # cannot go backwards.
        # Surprisingly sometimes this might not be the case (at
        # least on Windows and Linux), see:
        # https://github.com/giampaolo/psutil/issues/392
        # https://github.com/giampaolo/psutil/issues/645
        # https://github.com/giampaolo/psutil/issues/1210
        # Trim negative deltas to zero to ignore decreasing fields.
        # top does the same. Reference:
        # https://gitlab.com/procps-ng/procps/blob/v3.3.12/top/top.c#L5063
        field_delta = max(0, field_delta)
        field_deltas.append(field_delta)
    return _ntp.scputimes(*field_deltas)

