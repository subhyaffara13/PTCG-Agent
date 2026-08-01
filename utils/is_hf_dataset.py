
def is_hf_dataset(dataset):
    if not is_datasets_available():
        return False

    from datasets import Dataset, IterableDataset

    return isinstance(dataset, (Dataset, IterableDataset))

