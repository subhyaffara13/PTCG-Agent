
def _rb_get_stats(self):
    with self.lock:
        exp, sp = len(self.expert_buffer), len(self.self_play_buffer)
        return BufferStats(exp, sp, self.total_sampled, exp / (exp + sp) if (exp + sp) > 0 else 0.0)

