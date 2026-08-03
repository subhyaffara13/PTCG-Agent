import sys

def print_memory_profile(run_gc: bool = True) -> None:
    if not sys.platform.startswith("win"):
        import resource

        system_memuse = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    else:
        system_memuse = -1  # TODO: Support this on Windows
    if run_gc:
        gc.collect()
    freqs, memuse = collect_memory_stats()
    print("%7s  %7s  %7s  %s" % ("Freq", "Size(k)", "AvgSize", "Type"))
    print("-------------------------------------------")
    totalmem = 0
    i = 0
    for n, mem in sorted(memuse.items(), key=lambda x: -x[1]):
        f = freqs[n]
        if i < 50:
            print("%7d  %7d  %7.0f  %s" % (f, mem // 1024, mem / f, n))
        i += 1
        totalmem += mem
    print()
    print("Mem usage RSS   ", system_memuse // 1024)
    print("Total reachable ", totalmem // 1024)

