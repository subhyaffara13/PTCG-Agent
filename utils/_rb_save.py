
def _rb_save(self, path):
    with self.lock:
        with open(path, 'wb') as f: pickle.dump({'expert': list(self.expert_buffer), 'self_play': list(self.self_play_buffer)}, f)

