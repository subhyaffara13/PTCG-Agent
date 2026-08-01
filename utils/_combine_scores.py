
def _combine_scores(
    bm25_scores: List[float],
    emb_scores: List[float],
    bm25_weight: float = 0.4,
) -> List[float]:
    """Weighted average of BM25 and embedding scores, with min-max normalization."""

    def _normalize(scores: List[float]) -> List[float]:
        min_s = min(scores) if scores else 0.0
        max_s = max(scores) if scores else 0.0
        rng = max_s - min_s
        if rng == 0:
            return [0.0] * len(scores)
        return [(s - min_s) / rng for s in scores]

    norm_bm25 = _normalize(bm25_scores)
    norm_emb = _normalize(emb_scores)
    emb_weight = 1.0 - bm25_weight

    return [bm25_weight * b + emb_weight * e for b, e in zip(norm_bm25, norm_emb)]

