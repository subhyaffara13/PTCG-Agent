
def _rb_add_self_play(self, state, action, reward, td_error):
    with self.lock:
        priority = (abs(td_error) + 1e-5) ** self.alpha if td_error is not None else self.max_priority
        self.self_play_buffer.append((state, action, reward, priority))
        self.max_priority = max(self.max_priority, priority)

