import random
import threading
import pickle
import logging
from dataclasses import dataclass
from collections import deque
from typing import List, Tuple, Any
from factory.replay_buffer_helpers import sample_proportional, calculate_sample_sizes

logger = logging.getLogger(__name__)

@dataclass
class BufferStats:
    expert_count: int
    self_play_count: int
    sample_count: int
    expert_actual_ratio: float

class ReplayBuffer:
    def __init__(self, capacity: int = 100000, expert_ratio: float = 0.4, alpha: float = 0.6, beta: float = 0.4, beta_increment: float = 0.001):
        self.capacity = capacity
        self.expert_ratio = expert_ratio
        self.alpha = alpha
        self.beta = beta
        self.beta_increment = beta_increment
        
        self.expert_buffer = deque(maxlen=capacity)
        self.self_play_buffer = deque(maxlen=capacity)
        self.max_priority = 1.0
        self.lock = threading.Lock()
        self.total_sampled = 0
        
    def add_expert(self, state: Any, action: Any, reward: float, td_error: float = None):
        with self.lock:
            priority = (abs(td_error) + 1e-5) ** self.alpha if td_error is not None else self.max_priority
            self.expert_buffer.append((state, action, reward, priority))
            self.max_priority = max(self.max_priority, priority)
            
    def add_self_play(self, state: Any, action: Any, reward: float, td_error: float = None):
        with self.lock:
            priority = (abs(td_error) + 1e-5) ** self.alpha if td_error is not None else self.max_priority
            self.self_play_buffer.append((state, action, reward, priority))
            self.max_priority = max(self.max_priority, priority)

    def sample(self, batch_size: int = 64) -> Tuple[List, List, List]:
        with self.lock:
            if len(self.expert_buffer) == 0 and len(self.self_play_buffer) == 0:
                raise ValueError("Cannot sample from an empty buffer.")
                
            act_exp, act_sp = calculate_sample_sizes(batch_size, self.expert_ratio, len(self.expert_buffer), len(self.self_play_buffer))
            
            expert_samples = sample_proportional(self.expert_buffer, act_exp)
            self_play_samples = sample_proportional(self.self_play_buffer, act_sp)
            
            combined = expert_samples + self_play_samples
            random.shuffle(combined)
            
            self.total_sampled += len(combined)
            return ([item[0] for item in combined], [item[1] for item in combined], [item[2] for item in combined])

    def sample_with_weights(self, batch_size: int = 64) -> Tuple[List, List, List, List]:
        """Samples a batch with priorities, returning (batch, weights, indices)."""
        with self.lock:
            if len(self.expert_buffer) == 0 and len(self.self_play_buffer) == 0:
                raise ValueError("Cannot sample from an empty buffer.")
                
            act_exp, act_sp = calculate_sample_sizes(batch_size, self.expert_ratio, len(self.expert_buffer), len(self.self_play_buffer))
            
            def sample_buf(buffer, k, name):
                if not buffer or k == 0:
                    return [], [], []
                priorities = [item[3] for item in buffer]
                total_p = sum(priorities)
                probs = [p / total_p for p in priorities]
                indices = random.choices(range(len(buffer)), weights=probs, k=k)
                samples = [buffer[i] for i in indices]
                
                N = len(buffer)
                weights = []
                for idx in indices:
                    prob = priorities[idx] / total_p
                    w = (N * prob) ** (-self.beta)
                    weights.append(w)
                max_w = max(weights) if weights else 1.0
                weights = [w / max_w for w in weights]
                return samples, weights, [(name, idx) for idx in indices]
                
            exp_s, exp_w, exp_idx = sample_buf(self.expert_buffer, act_exp, "expert")
            sp_s, sp_w, sp_idx = sample_buf(self.self_play_buffer, act_sp, "self_play")
            
            combined = exp_s + sp_s
            weights = exp_w + sp_w
            indices = exp_idx + sp_idx
            
            zipped = list(zip(combined, weights, indices))
            random.shuffle(zipped)
            self.total_sampled += len(zipped)
            
            shuffled_combined = [z[0] for z in zipped]
            shuffled_weights = [z[1] for z in zipped]
            shuffled_indices = [z[2] for z in zipped]
            
            return shuffled_combined, shuffled_weights, shuffled_indices

    def update_priorities(self, indices, new_td_errors):
        with self.lock:
            for idx, error in zip(indices, new_td_errors):
                buf_type, i = idx
                priority = (abs(error) + 1e-5) ** self.alpha
                self.max_priority = max(self.max_priority, priority)
                if buf_type == "expert" and i < len(self.expert_buffer):
                    item = self.expert_buffer[i]
                    self.expert_buffer[i] = (item[0], item[1], item[2], priority)
                elif buf_type == "self_play" and i < len(self.self_play_buffer):
                    item = self.self_play_buffer[i]
                    self.self_play_buffer[i] = (item[0], item[1], item[2], priority)

    def anneal_beta(self):
        with self.lock:
            self.beta = min(1.0, self.beta + self.beta_increment)
            
    def __len__(self) -> int:
        with self.lock:
            return len(self.expert_buffer) + len(self.self_play_buffer)
            
    def get_stats(self) -> BufferStats:
        with self.lock:
            exp, sp = len(self.expert_buffer), len(self.self_play_buffer)
            tot = exp + sp
            return BufferStats(exp, sp, self.total_sampled, exp / tot if tot > 0 else 0.0)
            
    def save(self, path: str):
        with self.lock:
            with open(path, 'wb') as f:
                pickle.dump({'expert': list(self.expert_buffer), 'self_play': list(self.self_play_buffer)}, f)
                
    def load(self, path: str):
        with self.lock:
            try:
                with open(path, 'rb') as f:
                    data = pickle.load(f)  # nosec B301
                    self.expert_buffer = deque(data.get('expert', []), maxlen=self.capacity)
                    self.self_play_buffer = deque(data.get('self_play', []), maxlen=self.capacity)
            except Exception as e:
                logger.error(f"Failed to load replay buffer: {e}")
