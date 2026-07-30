from collections import deque
from typing import List, Tuple

def process_samples(aligner, samples):
    states = []; actions = []
    frame_stack = deque([[0.0] * aligner.SINGLE_STATE_DIM] * aligner.STACK_SIZE, maxlen=aligner.STACK_SIZE)
    for s in samples:
        try:
            norm_single_state = aligner.normalize_state(s["state"])
            frame_stack.append(norm_single_state)
            stacked_tensor = []
            for frame in frame_stack: stacked_tensor.extend(frame)
            norm_action = aligner.normalize_action(s["action"])
            states.append(stacked_tensor)
            actions.append(norm_action)
            for _ in range(2):
                aug_tensor = aligner.apply_symmetry_augmentation(stacked_tensor)
                states.append(aug_tensor); actions.append(norm_action)
        except Exception as e:
            __import__('logging').getLogger(__name__).warning(f"Skipping malformed sample: {e}")
    return states, actions
