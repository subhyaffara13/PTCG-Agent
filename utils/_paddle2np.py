from typing import Dict

def _paddle2np(paddle_dict: Dict[str, paddle.Tensor]) -> Dict[str, np.array]:
    for k, v in paddle_dict.items():
        paddle_dict[k] = v.detach().cpu().numpy()
    return paddle_dict

