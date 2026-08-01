
def apply_delta(cell: BanditCell, delta_alpha: float, delta_beta: float) -> BanditCell:
    """
    Apply a learning update to a cell, enforcing the sample cap.

    SAMPLE_CAP is a HARD cap on (alpha + beta). When the cap would be exceeded,
    we drop the update. (D5: hard cap, no rescaling — keep v0 simple.)
    """
    new_alpha = cell.alpha + delta_alpha
    new_beta = cell.beta + delta_beta
    if new_alpha + new_beta > SAMPLE_CAP:
        return cell
    return BanditCell(alpha=new_alpha, beta=new_beta)

