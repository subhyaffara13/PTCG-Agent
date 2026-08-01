
def _statistic_dunnett(
    samples: list[np.ndarray], control: np.ndarray, df: int,
    n_samples: np.ndarray, n_control: int
) -> tuple[np.ndarray, float, np.ndarray, np.ndarray]:
    """Statistic of Dunnett's test.

    Computation based on the original single-step test from [1].
    """
    mean_control = np.mean(control)
    mean_samples = np.array([np.mean(sample) for sample in samples])
    all_samples = [control] + samples
    all_means = np.concatenate([[mean_control], mean_samples])

    # Variance estimate s^2 from [1] Eq. 1
    s2 = np.sum([_var(sample, mean=mean)*sample.size
                 for sample, mean in zip(all_samples, all_means)]) / df
    std = np.sqrt(s2)

    # z score inferred from [1] unlabeled equation after Eq. 1
    z = (mean_samples - mean_control) / np.sqrt(1/n_samples + 1/n_control)

    return z / std, std, mean_control, mean_samples

