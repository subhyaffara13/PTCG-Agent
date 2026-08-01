
def _default_cuda_bench(self, f, *, warmup, rep, **kw):
    return self.benchmark_gpu(f, warmup=warmup, rep=rep, **kw)

