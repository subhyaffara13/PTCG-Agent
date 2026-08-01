
def decode_spans(
    start: np.ndarray, end: np.ndarray, topk: int, max_answer_len: int, undesired_tokens: np.ndarray
) -> tuple:
    """
    Take the output of any `ModelForQuestionAnswering` and will generate probabilities for each span to be the actual
    answer.

    In addition, it filters out some unwanted/impossible cases like answer len being greater than max_answer_len or
    answer end position being before the starting position. The method supports output the k-best answer through the
    topk argument.

    Args:
        start (`np.ndarray`): Individual start probabilities for each token.
        end (`np.ndarray`): Individual end probabilities for each token.
        topk (`int`): Indicates how many possible answer span(s) to extract from the model output.
        max_answer_len (`int`): Maximum size of the answer to extract from the model's output.
        undesired_tokens (`np.ndarray`): Mask determining tokens that can be part of the answer
    """
    # Ensure we have batch axis
    if start.ndim == 1:
        start = start[None]

    if end.ndim == 1:
        end = end[None]

    # Compute the score of each tuple(start, end) to be the real answer
    outer = np.matmul(np.expand_dims(start, -1), np.expand_dims(end, 1))

    # Remove candidate with end < start and end - start > max_answer_len
    candidates = np.tril(np.triu(outer), max_answer_len - 1)

    #  Inspired by Chen & al. (https://github.com/facebookresearch/DrQA)
    scores_flat = candidates.flatten()
    if topk == 1:
        idx_sort = [np.argmax(scores_flat)]
    elif len(scores_flat) <= topk:
        idx_sort = np.argsort(-scores_flat)
    else:
        idx = np.argpartition(-scores_flat, topk)[0:topk]
        idx_sort = idx[np.argsort(-scores_flat[idx])]

    starts, ends = np.unravel_index(idx_sort, candidates.shape)[1:]
    desired_spans = np.isin(starts, undesired_tokens.nonzero()) & np.isin(ends, undesired_tokens.nonzero())
    starts = starts[desired_spans]
    ends = ends[desired_spans]
    scores = candidates[0, starts, ends]

    return starts, ends, scores

