from . import BufferStats, deque, logger, pickle

def _rb_save(self, path):
    with self.lock:
        with open(path, 'wb') as f: pickle.dump({'expert': list(self.expert_buffer), 'self_play': list(self.self_play_buffer)}, f)

def _rb_load(self, path):
    with self.lock:
        try:
            with open(path, 'rb') as f:
                data = pickle.load(f)
                self.expert_buffer = deque(data.get('expert', []), maxlen=self.capacity)
                self.self_play_buffer = deque(data.get('self_play', []), maxlen=self.capacity)
        except Exception as e: logger.error(f"Failed to load replay buffer: {e}")

def _rb_len(self):
    with self.lock: return len(self.expert_buffer) + len(self.self_play_buffer)

def _rb_get_stats(self):
    with self.lock:
        exp, sp = len(self.expert_buffer), len(self.self_play_buffer)
        return BufferStats(exp, sp, self.total_sampled, exp / (exp + sp) if (exp + sp) > 0 else 0.0)
