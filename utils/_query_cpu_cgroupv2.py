
def _query_cpu_cgroupv2() -> int | None:
    avail_cpu = None
    with open("/sys/fs/cgroup/cpu.max", encoding="utf-8") as file:
        line = file.read().rstrip()
        fields = line.split()
        if len(fields) == 2:
            str_cpu_quota = fields[0]
            cpu_period = int(fields[1])
            # Make sure this is not in an unconstrained cgroup
            if str_cpu_quota != "max":
                cpu_quota = int(str_cpu_quota)
                avail_cpu = int(cpu_quota / cpu_period)
    return avail_cpu

