
def _default_cpu_bench(self, f, *, warmup, rep, **kw):
    return self.benchmark_cpu(f, warmup=warmup, rep=rep, **kw)

