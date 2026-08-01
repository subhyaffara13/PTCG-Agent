
def _gr_init(self, log_dir, perspective_flag):
    from . import BaseAgent, logger
    super(type(self), self).__init__(perspective_flag)
    self.log_dir = Path(log_dir); self.log_dir.mkdir(parents=True, exist_ok=True)
    if type(self)._executor is None:
        os.environ["OPENBLAS_NUM_THREADS"] = "1"; os.environ["OMP_NUM_THREADS"] = "1"; os.environ["MKL_NUM_THREADS"] = "1"
        max_w = min(2, os.cpu_count() or 2)
        type(self)._executor = ProcessPoolExecutor(max_workers=max_w)

