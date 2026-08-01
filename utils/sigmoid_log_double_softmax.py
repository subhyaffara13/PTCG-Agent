
def sigmoid_log_double_softmax(
    similarity: torch.Tensor, matchability0: torch.Tensor, matchability1: torch.Tensor
) -> torch.Tensor:
    """create the log assignment matrix from logits and similarity"""
    batch_size, num_keypoints_0, num_keypoints_1 = similarity.shape
    certainties = nn.functional.logsigmoid(matchability0) + nn.functional.logsigmoid(matchability1).transpose(1, 2)
    scores0 = nn.functional.log_softmax(similarity, 2)
    scores1 = nn.functional.log_softmax(similarity.transpose(-1, -2).contiguous(), 2).transpose(-1, -2)
    scores = similarity.new_full((batch_size, num_keypoints_0 + 1, num_keypoints_1 + 1), 0)
    scores[:, :num_keypoints_0, :num_keypoints_1] = scores0 + scores1 + certainties
    scores[:, :-1, -1] = nn.functional.logsigmoid(-matchability0.squeeze(-1))
    scores[:, -1, :-1] = nn.functional.logsigmoid(-matchability1.squeeze(-1))
    return scores


def sigmoid_log_double_softmax(
    similarity: torch.Tensor, matchability0: torch.Tensor, matchability1: torch.Tensor
) -> torch.Tensor:
    """create the log assignment matrix from logits and similarity"""
    batch_size, num_keypoints_0, num_keypoints_1 = similarity.shape
    certainties = nn.functional.logsigmoid(matchability0) + nn.functional.logsigmoid(matchability1).transpose(1, 2)
    scores0 = nn.functional.log_softmax(similarity, 2)
    scores1 = nn.functional.log_softmax(similarity.transpose(-1, -2).contiguous(), 2).transpose(-1, -2)
    scores = similarity.new_full((batch_size, num_keypoints_0 + 1, num_keypoints_1 + 1), 0)
    scores[:, :num_keypoints_0, :num_keypoints_1] = scores0 + scores1 + certainties
    scores[:, :-1, -1] = nn.functional.logsigmoid(-matchability0.squeeze(-1))
    scores[:, -1, :-1] = nn.functional.logsigmoid(-matchability1.squeeze(-1))
    return scores

