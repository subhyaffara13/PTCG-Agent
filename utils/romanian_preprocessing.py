
def romanian_preprocessing(text):
    """Sennrich's WMT16 scripts for Romanian preprocessing, used by model `FacebookAI/xlm-mlm-enro-1024`"""
    # https://github.com/rsennrich/wmt16-scripts/blob/master/preprocess/normalise-romanian.py
    text = text.replace("\u015e", "\u0218").replace("\u015f", "\u0219")
    text = text.replace("\u0162", "\u021a").replace("\u0163", "\u021b")
    # https://github.com/rsennrich/wmt16-scripts/blob/master/preprocess/remove-diacritics.py
    text = text.replace("\u0218", "S").replace("\u0219", "s")  # s-comma
    text = text.replace("\u021a", "T").replace("\u021b", "t")  # t-comma
    text = text.replace("\u0102", "A").replace("\u0103", "a")
    text = text.replace("\u00c2", "A").replace("\u00e2", "a")
    text = text.replace("\u00ce", "I").replace("\u00ee", "i")
    return text

