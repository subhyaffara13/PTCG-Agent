
def compute_curve(labels, predictions, num_thresholds=None, weights=None):
    _MINIMUM_COUNT = 1e-7

    if weights is None:
        weights = 1.0

    # Compute bins of true positives and false positives.
    # pyrefly: ignore [unsupported-operation]
    bucket_indices = np.int32(np.floor(predictions * (num_thresholds - 1)))
    float_labels = labels.astype(np.float64)
    # pyrefly: ignore [unsupported-operation]
    histogram_range = (0, num_thresholds - 1)
    tp_buckets, _ = np.histogram(
        bucket_indices,
        # pyrefly: ignore [bad-argument-type]
        bins=num_thresholds,
        range=histogram_range,
        weights=float_labels * weights,
    )
    fp_buckets, _ = np.histogram(
        bucket_indices,
        # pyrefly: ignore [bad-argument-type]
        bins=num_thresholds,
        range=histogram_range,
        weights=(1.0 - float_labels) * weights,
    )

    # Obtain the reverse cumulative sum.
    tp = np.cumsum(tp_buckets[::-1])[::-1]
    fp = np.cumsum(fp_buckets[::-1])[::-1]
    tn = fp[0] - fp
    fn = tp[0] - tp
    precision = tp / np.maximum(_MINIMUM_COUNT, tp + fp)
    recall = tp / np.maximum(_MINIMUM_COUNT, tp + fn)
    return np.stack((tp, fp, tn, fn, precision, recall))

