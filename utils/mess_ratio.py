
def mess_ratio(
    decoded_sequence: str, maximum_threshold: float = 0.2, debug: bool = False
) -> float:
    """
    Compute a mess ratio given a decoded bytes sequence. The maximum threshold does stop the computation earlier.
    """

    seq_len: int = len(decoded_sequence)

    if seq_len < 511:
        step: int = 32
    elif seq_len < 1024:
        step = 64
    else:
        step = 128

    # Create each detector as a named local variable (unrolled from the generic loop).
    # This eliminates per-character iteration over the detector list and
    # per-character eligible() virtual dispatch, while keeping every plugin class
    # intact and fully readable.
    d_sp: TooManySymbolOrPunctuationPlugin = TooManySymbolOrPunctuationPlugin()
    d_ta: TooManyAccentuatedPlugin = TooManyAccentuatedPlugin()
    d_up: UnprintablePlugin = UnprintablePlugin()
    d_sda: SuspiciousDuplicateAccentPlugin = SuspiciousDuplicateAccentPlugin()
    d_sr: SuspiciousRange = SuspiciousRange()
    d_sw: SuperWeirdWordPlugin = SuperWeirdWordPlugin()
    d_cu: CjkUncommonPlugin = CjkUncommonPlugin()
    d_au: ArchaicUpperLowerPlugin = ArchaicUpperLowerPlugin()
    d_ai: ArabicIsolatedFormPlugin = ArabicIsolatedFormPlugin()

    # Local references for feed_info methods called in the hot loop.
    d_sp_feed = d_sp.feed_info
    d_ta_feed = d_ta.feed_info
    d_up_feed = d_up.feed_info
    d_sda_feed = d_sda.feed_info
    d_sr_feed = d_sr.feed_info
    d_sw_feed = d_sw.feed_info
    d_cu_feed = d_cu.feed_info
    d_au_feed = d_au.feed_info
    d_ai_feed = d_ai.feed_info

    # Single reusable CharInfo object (avoids per-character allocation).
    info: CharInfo = CharInfo()
    info_update = info.update

    mean_mess_ratio: float

    for block_start in range(0, seq_len, step):
        for character in decoded_sequence[block_start : block_start + step]:
            # Pre-compute all character properties once (shared across all plugins).
            info_update(character)

            # Detectors with eligible() == always True
            d_up_feed(character, info)
            d_sw_feed(character, info)
            d_au_feed(character, info)

            # Detectors with eligible() == isprintable
            if info.printable:
                d_sp_feed(character, info)
                d_sr_feed(character, info)

            # Detectors with eligible() == isalpha
            if info.alpha:
                d_ta_feed(character, info)
                # SuspiciousDuplicateAccent: isalpha() and is_latin()
                if info.latin:
                    d_sda_feed(character, info)
                # CjkUncommon: is_cjk()
                if info.is_cjk:
                    d_cu_feed(character, info)
                # ArabicIsolatedForm: is_arabic()
                if info.is_arabic:
                    d_ai_feed(character, info)

        mean_mess_ratio = (
            d_sp.ratio
            + d_ta.ratio
            + d_up.ratio
            + d_sda.ratio
            + d_sr.ratio
            + d_sw.ratio
            + d_cu.ratio
            + d_au.ratio
            + d_ai.ratio
        )

        if mean_mess_ratio >= maximum_threshold:
            break
    else:
        # Flush last word buffer in SuperWeirdWordPlugin via trailing newline.
        info_update("\n")
        d_sw_feed("\n", info)
        d_au_feed("\n", info)
        d_up_feed("\n", info)

        mean_mess_ratio = (
            d_sp.ratio
            + d_ta.ratio
            + d_up.ratio
            + d_sda.ratio
            + d_sr.ratio
            + d_sw.ratio
            + d_cu.ratio
            + d_au.ratio
            + d_ai.ratio
        )

    if debug:  # Defensive:
        logger = getLogger("charset_normalizer")

        logger.log(
            TRACE,
            "Mess-detector extended-analysis start. "
            f"intermediary_mean_mess_ratio_calc={step} mean_mess_ratio={mean_mess_ratio} "
            f"maximum_threshold={maximum_threshold}",
        )

        if seq_len > 16:
            logger.log(TRACE, f"Starting with: {decoded_sequence[:16]}")
            logger.log(TRACE, f"Ending with: {decoded_sequence[-16::]}")

        for dt in [d_sp, d_ta, d_up, d_sda, d_sr, d_sw, d_cu, d_au, d_ai]:
            logger.log(TRACE, f"{dt.__class__}: {dt.ratio}")

    return round(mean_mess_ratio, 3)

