
def _rb_len(self):
    with self.lock: return len(self.expert_buffer) + len(self.self_play_buffer)

