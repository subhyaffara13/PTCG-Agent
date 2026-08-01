
def _rb_load(self, path):
    with self.lock:
        try:
            with open(path, 'rb') as f:
                data = pickle.load(f)
                self.expert_buffer = deque(data.get('expert', []), maxlen=self.capacity)
                self.self_play_buffer = deque(data.get('self_play', []), maxlen=self.capacity)
        except Exception as e: logger.error(f"Failed to load replay buffer: {e}")

