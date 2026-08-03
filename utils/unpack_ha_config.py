from typing import Any, Dict

def unpack_ha_config(strategy_thresholds: Dict[str, Any]) -> dict:
    ha_config = strategy_thresholds.get("hand_analyst", {}) if isinstance(strategy_thresholds, dict) else {}
    if not isinstance(ha_config, dict):
        return dict(DEFAULT_HA_CONFIG)
    
    result = dict(DEFAULT_HA_CONFIG)
    for section, src_key, dst_key in SECTION_MAP:
        sub = ha_config.get(section, {})
        if isinstance(sub, dict) and src_key in sub:
            result[dst_key] = sub[src_key]
    
    profiles = ha_config.get("priority_profiles", {})
    if isinstance(profiles, dict):
        for profile, src_key, dst_key in PROFILE_MAP:
            psub = profiles.get(profile, {})
            if isinstance(psub, dict) and src_key in psub:
                result[dst_key] = psub[src_key]
    return result


def unpack_ha_config(strategy_thresholds: Dict[str, Any]) -> dict:
    ha_config = strategy_thresholds.get("hand_analyst", {}) if isinstance(strategy_thresholds, dict) else {}
    if not isinstance(ha_config, dict):
        return dict(DEFAULT_HA_CONFIG)
    
    result = dict(DEFAULT_HA_CONFIG)
    for section, src_key, dst_key in SECTION_MAP:
        sub = ha_config.get(section, {})
        if isinstance(sub, dict) and src_key in sub:
            result[dst_key] = sub[src_key]
    
    profiles = ha_config.get("priority_profiles", {})
    if isinstance(profiles, dict):
        for profile, src_key, dst_key in PROFILE_MAP:
            psub = profiles.get(profile, {})
            if isinstance(psub, dict) and src_key in psub:
                result[dst_key] = psub[src_key]
    return result


def unpack_ha_config(strategy_thresholds: Dict[str, Any]) -> dict:
    ha_config = strategy_thresholds.get("hand_analyst", {}) if isinstance(strategy_thresholds, dict) else {}
    if not isinstance(ha_config, dict):
        return dict(DEFAULT_HA_CONFIG)
    
    result = dict(DEFAULT_HA_CONFIG)
    for section, src_key, dst_key in SECTION_MAP:
        sub = ha_config.get(section, {})
        if isinstance(sub, dict) and src_key in sub:
            result[dst_key] = sub[src_key]
    
    profiles = ha_config.get("priority_profiles", {})
    if isinstance(profiles, dict):
        for profile, src_key, dst_key in PROFILE_MAP:
            psub = profiles.get(profile, {})
            if isinstance(psub, dict) and src_key in psub:
                result[dst_key] = psub[src_key]
    return result

