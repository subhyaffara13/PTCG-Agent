
def _rb_sample_with_weights(self, batch_size):
    with self.lock:
        if len(self.expert_buffer) == 0 and len(self.self_play_buffer) == 0:
            raise ValueError("Cannot sample from an empty buffer.")
        act_exp, act_sp = calculate_sample_sizes(batch_size, self.expert_ratio, len(self.expert_buffer), len(self.self_play_buffer))
        exp_s, exp_w, exp_idx = _sample_buf(self, self.expert_buffer, act_exp, "expert")
        sp_s, sp_w, sp_idx = _sample_buf(self, self.self_play_buffer, act_sp, "self_play")
        combined = exp_s + sp_s; weights = exp_w + sp_w; indices = exp_idx + sp_idx
        zipped = list(zip(combined, weights, indices)); random.shuffle(zipped)
        self.total_sampled += len(zipped)
        return ([z[0] for z in zipped], [z[1] for z in zipped], [z[2] for z in zipped])

