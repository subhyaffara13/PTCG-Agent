import random
import threading
import pickle
import logging
from dataclasses import dataclass
from collections import deque
from typing import List, Tuple, Any

logger = logging.getLogger(__name__)

@dataclass
class BufferStats:
    expert_count: int
    self_play_count: int
    sample_count: int
    expert_actual_ratio: float

class ReplayBuffer:
    def __init__(self, capacity: int = 100000, expert_ratio: float = 0.4, alpha: float = 0.6):
        """
        Mixed dual-source Prioritized Experience Replay buffer.
        expert_ratio controls the exact percentage of expert data in every sampled batch.
        alpha determines how much prioritization is used (0 = uniform, 1 = fully prioritized).
        """
        self.capacity = capacity
        self.expert_ratio = expert_ratio
        self.alpha = alpha
        
        # We store tuples of (state, action, reward, priority)
        self.expert_buffer: deque = deque(maxlen=capacity)
        self.self_play_buffer: deque = deque(maxlen=capacity)
        
        # Max priority seen so far to initialize new elements
        self.max_priority = 1.0
        
        self.lock = threading.Lock()
        self.total_sampled = 0
        
    def add_expert(self, state: Any, action: Any, reward: float, td_error: float = None):
        """Adds an external dataset sample."""
        with self.lock:
            priority = (abs(td_error) + 1e-5) ** self.alpha if td_error is not None else self.max_priority
            self.expert_buffer.append((state, action, reward, priority))
            
    def add_self_play(self, state: Any, action: Any, reward: float, td_error: float = None):
        """Adds a live simulation sample."""
        with self.lock:
            priority = (abs(td_error) + 1e-5) ** self.alpha if td_error is not None else self.max_priority
            self.self_play_buffer.append((state, action, reward, priority))
            
    def _sample_proportional(self, buffer: deque, k: int) -> List[Any]:
        if not buffer:
            return []
        priorities = [item[3] for item in buffer]
        total_p = sum(priorities)
        probs = [p / total_p for p in priorities]
        
        # Convert to list to allow index sampling
        indices = random.choices(range(len(buffer)), weights=probs, k=k)
        return [buffer[i] for i in indices]
            
    def sample(self, batch_size: int = 64) -> Tuple[List, List, List]:
        """
        Returns a mixed batch maintaining exact expert_ratio.
        If not enough expert data, fill with self-play. 
        If not enough self-play, fill with expert.
        """
        with self.lock:
            if len(self.expert_buffer) == 0 and len(self.self_play_buffer) == 0:
                raise ValueError("Cannot sample from an empty buffer.")
                
            target_expert = int(batch_size * self.expert_ratio)
            target_self_play = batch_size - target_expert
            
            # Adjust if either buffer is too small
            actual_expert = min(target_expert, len(self.expert_buffer))
            if actual_expert < target_expert:
                target_self_play += (target_expert - actual_expert)
                
            actual_self_play = min(target_self_play, len(self.self_play_buffer))
            if actual_self_play < target_self_play:
                # If we couldn't get enough self play, go back and try to get more expert
                needed = target_self_play - actual_self_play
                extra_expert = min(needed, len(self.expert_buffer) - actual_expert)
                actual_expert += extra_expert
                
            # Final batch size might be smaller than requested if both buffers combined are small
            expert_samples = self._sample_proportional(self.expert_buffer, actual_expert)
            self_play_samples = self._sample_proportional(self.self_play_buffer, actual_self_play)
            
            combined = expert_samples + self_play_samples
            random.shuffle(combined)
            
            states = [item[0] for item in combined]
            actions = [item[1] for item in combined]
            rewards = [item[2] for item in combined]
            
            self.total_sampled += len(combined)
            
            return states, actions, rewards
            
    def __len__(self) -> int:
        with self.lock:
            return len(self.expert_buffer) + len(self.self_play_buffer)
            
    def get_stats(self) -> BufferStats:
        with self.lock:
            expert = len(self.expert_buffer)
            self_play = len(self.self_play_buffer)
            total = expert + self_play
            ratio = expert / total if total > 0 else 0.0
            
            return BufferStats(
                expert_count=expert,
                self_play_count=self_play,
                sample_count=self.total_sampled,
                expert_actual_ratio=ratio
            )
            
    def save(self, path: str):
        with self.lock:
            with open(path, 'wb') as f:
                pickle.dump({
                    'expert': list(self.expert_buffer),
                    'self_play': list(self.self_play_buffer)
                }, f)
                
    def load(self, path: str):
        with self.lock:
            try:
                with open(path, 'rb') as f:
                    data = pickle.load(f)
                    self.expert_buffer = deque(data.get('expert', []), maxlen=self.capacity)
                    self.self_play_buffer = deque(data.get('self_play', []), maxlen=self.capacity)
            except Exception as e:
                logger.error(f"Failed to load replay buffer: {e}")
