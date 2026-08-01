
def get_classification_hyperparams(df: pd.DataFrame) -> tuple[int, object]:
    n_classes = df.completion.nunique()
    pos_class = None
    if n_classes == 2:
        pos_class = df.completion.value_counts().index[0]
    return n_classes, pos_class

