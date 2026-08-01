
def compute_score(boxes):
    """
    Compute logit scores per class for each box (proposal) and an array of class indices
    corresponding to each proposal, flattened across the proposal_num.
    The indices in `classes` will later be used to filter and match the predicted classes
    with the input class names.
    """
    num_classes = boxes.shape[2]
    proposal_num = boxes.shape[1]
    scores = torch.sigmoid(boxes)
    classes = torch.arange(num_classes, device=boxes.device).unsqueeze(0).repeat(proposal_num, 1).flatten(0, 1)
    return scores, classes

