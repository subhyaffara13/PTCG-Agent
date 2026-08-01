
def _initialize_preference_map():
    global _DYNAMIC_PREFERENCE_MAP
    _DYNAMIC_PREFERENCE_MAP = {}
    
    # Try locating card_pool_raw.csv
    search_paths = [
        Path("skills/card_pool_raw.csv"),
        Path("../skills/card_pool_raw.csv"),
        Path(__file__).resolve().parent.parent / "skills" / "card_pool_raw.csv"
    ]
    
    type_to_energy = {
        '{g}': '1', '{r}': '2', '{w}': '3', '{l}': '4',
        '{p}': '5', '{f}': '6', '{d}': '7', '{m}': '8'
    }
    
    csv_loaded = False
    for path in search_paths:
        if path.exists():
            try:
                with open(path, "r", encoding="utf-8") as f:
                    reader = csv.DictReader(f)
                    for row in reader:
                        cid = row.get("Card ID", "").strip()
                        t = row.get("Type", "").strip().lower()
                        if cid and t in type_to_energy:
                            _DYNAMIC_PREFERENCE_MAP[str(cid)] = type_to_energy[t]
                csv_loaded = True
                break
            except Exception as e:
                logger.error(f"Error loading {path}: {e}")
                
    if not csv_loaded:
        logger.warning("Could not load dynamic preference map from card_pool_raw.csv, using static fallback.")
        for k, v in ENERGY_PREFERENCE_MAP.items():
            _DYNAMIC_PREFERENCE_MAP[str(k)] = str(v)


def _initialize_preference_map():
    global _DYNAMIC_PREFERENCE_MAP
    if _DYNAMIC_PREFERENCE_MAP is not None:
        return
    _DYNAMIC_PREFERENCE_MAP = {}
    
    # Try locating card_pool_raw.csv
    search_paths = [
        Path("skills/card_pool_raw.csv"),
        Path("../skills/card_pool_raw.csv"),
        Path(__file__).resolve().parent.parent / "skills" / "card_pool_raw.csv"
    ]
    
    type_to_energy = {
        '{g}': '1', '{r}': '2', '{w}': '3', '{l}': '4',
        '{p}': '5', '{f}': '6', '{d}': '7', '{m}': '8',
        '草': '1', '炎': '2', '水': '3', '雷': '4',
        '超': '5', '闘': '6', '悪': '7', '鋼': '8'
    }
    
    csv_loaded = False
    for path in search_paths:
        if path.exists():
            try:
                with open(path, "r", encoding="utf-8") as f:
                    reader = csv.DictReader(f)
                    for row in reader:
                        cid = row.get("Card ID", "").strip()
                        t = row.get("Type", "").strip().lower()
                        if cid and t in type_to_energy:
                            _DYNAMIC_PREFERENCE_MAP[str(cid)] = type_to_energy[t]
                csv_loaded = True
                break
            except Exception as e:
                logger.error(f"Error loading {path}: {e}")
                
    if not csv_loaded:
        logger.warning("Could not load dynamic preference map from card_pool_raw.csv, using static fallback.")
        for k, v in ENERGY_PREFERENCE_MAP.items():
            _DYNAMIC_PREFERENCE_MAP[str(k)] = str(v)


def _initialize_preference_map():
    global _DYNAMIC_PREFERENCE_MAP
    if _DYNAMIC_PREFERENCE_MAP is not None:
        return
    _DYNAMIC_PREFERENCE_MAP = {}

    search_paths = [
        Path("skills/card_pool_raw.csv"),
        Path("../skills/card_pool_raw.csv"),
        Path(__file__).resolve().parent.parent / "skills" / "card_pool_raw.csv"
    ]

    type_to_energy = {
        '{g}': '1', '{r}': '2', '{w}': '3', '{l}': '4',
        '{p}': '5', '{f}': '6', '{d}': '7', '{m}': '8',
        '草': '1', '炎': '2', '水': '3', '雷': '4',
        '超': '5', '闘': '6', '悪': '7', '鋼': '8'
    }

    csv_loaded = False
    for path in search_paths:
        if path.exists():
            try:
                with open(path, "r", encoding="utf-8") as f:
                    reader = csv.DictReader(f)
                    for row in reader:
                        cid = row.get("Card ID", "").strip()
                        t = row.get("Type", "").strip().lower()
                        if cid and t in type_to_energy:
                            _DYNAMIC_PREFERENCE_MAP[str(cid)] = type_to_energy[t]
                csv_loaded = True
                break
            except Exception as e:
                logger.error(f"Error loading {path}: {e}")

    if not csv_loaded:
        logger.warning("Could not load dynamic preference map from card_pool_raw.csv, using static fallback.")
        for k, v in ENERGY_PREFERENCE_MAP.items():
            _DYNAMIC_PREFERENCE_MAP[str(k)] = str(v)


def _initialize_preference_map():
    global _DYNAMIC_PREFERENCE_MAP
    if _DYNAMIC_PREFERENCE_MAP is not None:
        return
    _DYNAMIC_PREFERENCE_MAP = {}
    
    # Try locating card_pool_raw.csv
    search_paths = [
        Path("skills/card_pool_raw.csv"),
        Path("../skills/card_pool_raw.csv"),
        Path(__file__).resolve().parent.parent / "skills" / "card_pool_raw.csv"
    ]
    
    type_to_energy = {
        '{g}': '1', '{r}': '2', '{w}': '3', '{l}': '4',
        '{p}': '5', '{f}': '6', '{d}': '7', '{m}': '8',
        '草': '1', '炎': '2', '水': '3', '雷': '4',
        '超': '5', '闘': '6', '悪': '7', '鋼': '8'
    }
    
    csv_loaded = False
    for path in search_paths:
        if path.exists():
            try:
                with open(path, "r", encoding="utf-8") as f:
                    reader = csv.DictReader(f)
                    for row in reader:
                        cid = row.get("Card ID", "").strip()
                        t = row.get("Type", "").strip().lower()
                        if cid and t in type_to_energy:
                            _DYNAMIC_PREFERENCE_MAP[str(cid)] = type_to_energy[t]
                csv_loaded = True
                break
            except Exception as e:
                logger.error(f"Error loading {path}: {e}")
                
    if not csv_loaded:
        logger.warning("Could not load dynamic preference map from card_pool_raw.csv, using static fallback.")
        for k, v in ENERGY_PREFERENCE_MAP.items():
            _DYNAMIC_PREFERENCE_MAP[str(k)] = str(v)


def _initialize_preference_map():
    global _DYNAMIC_PREFERENCE_MAP
    if _DYNAMIC_PREFERENCE_MAP is not None:
        return
    _DYNAMIC_PREFERENCE_MAP = {}

    search_paths = [
        Path("skills/card_pool_raw.csv"),
        Path("../skills/card_pool_raw.csv"),
        Path(__file__).resolve().parent.parent / "skills" / "card_pool_raw.csv"
    ]

    type_to_energy = {
        '{g}': '1', '{r}': '2', '{w}': '3', '{l}': '4',
        '{p}': '5', '{f}': '6', '{d}': '7', '{m}': '8',
        '草': '1', '炎': '2', '水': '3', '雷': '4',
        '超': '5', '闘': '6', '悪': '7', '鋼': '8'
    }

    csv_loaded = False
    for path in search_paths:
        if path.exists():
            try:
                with open(path, "r", encoding="utf-8") as f:
                    reader = csv.DictReader(f)
                    for row in reader:
                        cid = row.get("Card ID", "").strip()
                        t = row.get("Type", "").strip().lower()
                        if cid and t in type_to_energy:
                            _DYNAMIC_PREFERENCE_MAP[str(cid)] = type_to_energy[t]
                csv_loaded = True
                break
            except Exception as e:
                logger.error(f"Error loading {path}: {e}")

    if not csv_loaded:
        logger.warning("Could not load dynamic preference map from card_pool_raw.csv, using static fallback.")
        for k, v in ENERGY_PREFERENCE_MAP.items():
            _DYNAMIC_PREFERENCE_MAP[str(k)] = str(v)

