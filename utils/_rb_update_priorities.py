
def _rb_update_priorities(self, indices, new_td_errors):
    with self.lock:
        for idx, error in zip(indices, new_td_errors):
            buf_type, i = idx; priority = (abs(error) + 1e-5) ** self.alpha
            self.max_priority = max(self.max_priority, priority)
            if buf_type == "expert" and i < len(self.expert_buffer):
                item = self.expert_buffer[i]
                self.expert_buffer[i] = (item[0], item[1], item[2], priority)
            elif buf_type == "self_play" and i < len(self.self_play_buffer):
                item = self.self_play_buffer[i]
                self.self_play_buffer[i] = (item[0], item[1], item[2], priority)

