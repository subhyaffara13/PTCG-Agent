import random

def _rb_sample(self, batch_size):
    with self.lock:
        if len(self.expert_buffer) == 0 and len(self.self_play_buffer) == 0:
            raise ValueError("Cannot sample from an empty buffer.")
        act_exp, act_sp = calculate_sample_sizes(batch_size, self.expert_ratio, len(self.expert_buffer), len(self.self_play_buffer))
        combined = sample_proportional(self.expert_buffer, act_exp) + sample_proportional(self.self_play_buffer, act_sp)
        random.shuffle(combined)
        self.total_sampled += len(combined)
        return ([item[0] for item in combined], [item[1] for item in combined], [item[2] for item in combined])

