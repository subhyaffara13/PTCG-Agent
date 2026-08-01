
def _default_xpu_bench(self, f, *, warmup, rep, **kw):
    return self.benchmark_gpu(f, warmup=warmup, rep=rep, **kw)

