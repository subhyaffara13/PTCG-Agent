from typing import Dict

def buildClipList(clipBoxes: Dict[str, _ClipBoxInput]) -> ot.ClipList:
    clipList = ot.ClipList()
    clipList.Format = 1
    clipList.clips = {name: buildClipBox(box) for name, box in clipBoxes.items()}
    return clipList

