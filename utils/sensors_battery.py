import os

def sensors_battery():
    """Return battery information.
    Implementation note: it appears /sys/class/power_supply/BAT0/
    directory structure may vary and provide files with the same
    meaning but under different names, see:
    https://github.com/giampaolo/psutil/issues/966.
    """
    null = object()

    def multi_bcat(*paths):
        """Attempt to read the content of multiple files which may
        not exist. If none of them exist return None.
        """
        for path in paths:
            ret = bcat(path, fallback=null)
            if ret != null:
                try:
                    return int(ret)
                except ValueError:
                    return ret.strip()
        return None

    bats = [
        x
        for x in os.listdir(POWER_SUPPLY_PATH)
        if x.startswith('BAT') or 'battery' in x.lower()
    ]
    if not bats:
        return None
    # Get the first available battery. Usually this is "BAT0", except
    # some rare exceptions:
    # https://github.com/giampaolo/psutil/issues/1238
    root = os.path.join(POWER_SUPPLY_PATH, min(bats))

    # Base metrics.
    energy_now = multi_bcat(root + "/energy_now", root + "/charge_now")
    power_now = multi_bcat(root + "/power_now", root + "/current_now")
    energy_full = multi_bcat(root + "/energy_full", root + "/charge_full")
    time_to_empty = multi_bcat(root + "/time_to_empty_now")

    # Percent. If we have energy_full the percentage will be more
    # accurate compared to reading /capacity file (float vs. int).
    if energy_full is not None and energy_now is not None:
        try:
            percent = 100.0 * energy_now / energy_full
        except ZeroDivisionError:
            percent = 0.0
    else:
        percent = int(cat(root + "/capacity", fallback=-1))
        if percent == -1:
            return None

    # Is AC power cable plugged in?
    # Note: AC0 is not always available and sometimes (e.g. CentOS7)
    # it's called "AC".
    power_plugged = None
    online = multi_bcat(
        os.path.join(POWER_SUPPLY_PATH, "AC0/online"),
        os.path.join(POWER_SUPPLY_PATH, "AC/online"),
    )
    if online is not None:
        power_plugged = online == 1
    else:
        status = cat(root + "/status", fallback="").strip().lower()
        if status == "discharging":
            power_plugged = False
        elif status in {"charging", "full"}:
            power_plugged = True

    # Seconds left.
    # Note to self: we may also calculate the charging ETA as per:
    # https://github.com/thialfihar/dotfiles/blob/
    #     013937745fd9050c30146290e8f963d65c0179e6/bin/battery.py#L55
    if power_plugged:
        secsleft = _common.POWER_TIME_UNLIMITED
    elif energy_now is not None and power_now is not None:
        try:
            secsleft = int(energy_now / abs(power_now) * 3600)
        except ZeroDivisionError:
            secsleft = _common.POWER_TIME_UNKNOWN
    elif time_to_empty is not None:
        secsleft = int(time_to_empty * 60)
        if secsleft < 0:
            secsleft = _common.POWER_TIME_UNKNOWN
    else:
        secsleft = _common.POWER_TIME_UNKNOWN

    return ntp.sbattery(percent, secsleft, power_plugged)


def sensors_battery():
    """Return battery information."""
    try:
        percent, minsleft, power_plugged = cext.sensors_battery()
    except NotImplementedError:
        # no power source - return None according to interface
        return None
    power_plugged = power_plugged == 1
    if power_plugged:
        secsleft = _common.POWER_TIME_UNLIMITED
    elif minsleft == -1:
        secsleft = _common.POWER_TIME_UNKNOWN
    else:
        secsleft = minsleft * 60
    return ntp.sbattery(percent, secsleft, power_plugged)


def sensors_battery():
    """Return battery information."""
    # For constants meaning see:
    # https://msdn.microsoft.com/en-us/library/windows/desktop/
    #     aa373232(v=vs.85).aspx
    acline_status, flags, percent, secsleft = cext.sensors_battery()
    power_plugged = acline_status == 1
    no_battery = bool(flags & 128)
    charging = bool(flags & 8)

    if no_battery:
        return None
    if power_plugged or charging:
        secsleft = _common.POWER_TIME_UNLIMITED
    elif secsleft == -1:
        secsleft = _common.POWER_TIME_UNKNOWN

    return ntp.sbattery(percent, secsleft, power_plugged)

