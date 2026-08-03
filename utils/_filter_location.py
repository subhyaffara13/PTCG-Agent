from typing import Dict

def _filterLocation(
    userRegion: Region,
    location: Dict[str, float],
) -> Dict[str, float]:
    return {
        name: value
        for name, value in location.items()
        if name in userRegion and isinstance(userRegion[name], Range)
    }

