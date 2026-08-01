
def _createOffsetArrayIndexSubTableMixin(formatStringForDataType):
    # Prep the data size for the offset array data format.
    dataFormat = ">" + formatStringForDataType
    offsetDataSize = struct.calcsize(dataFormat)

    class OffsetArrayIndexSubTableMixin(object):
        def decompile(self):
            numGlyphs = self.lastGlyphIndex - self.firstGlyphIndex + 1
            indexingOffsets = [
                glyphIndex * offsetDataSize for glyphIndex in range(numGlyphs + 2)
            ]
            indexingLocations = zip(indexingOffsets, indexingOffsets[1:])
            offsetArray = [
                struct.unpack(dataFormat, self.data[slice(*loc)])[0]
                for loc in indexingLocations
            ]

            glyphIds = list(range(self.firstGlyphIndex, self.lastGlyphIndex + 1))
            modifiedOffsets = [offset + self.imageDataOffset for offset in offsetArray]
            self.locations = list(zip(modifiedOffsets, modifiedOffsets[1:]))

            self.names = list(map(self.ttFont.getGlyphName, glyphIds))
            self.removeSkipGlyphs()
            del self.data, self.ttFont

        def compile(self, ttFont):
            # First make sure that all the data lines up properly. Formats 1 and 3
            # must have all its data lined up consecutively. If not this will fail.
            for curLoc, nxtLoc in zip(self.locations, self.locations[1:]):
                assert (
                    curLoc[1] == nxtLoc[0]
                ), "Data must be consecutive in indexSubTable offset formats"

            glyphIds = list(map(ttFont.getGlyphID, self.names))
            # Make sure that all ids are sorted strictly increasing.
            assert all(glyphIds[i] < glyphIds[i + 1] for i in range(len(glyphIds) - 1))

            # Run a simple algorithm to add skip glyphs to the data locations at
            # the places where an id is not present.
            idQueue = deque(glyphIds)
            locQueue = deque(self.locations)
            allGlyphIds = list(range(self.firstGlyphIndex, self.lastGlyphIndex + 1))
            allLocations = []
            for curId in allGlyphIds:
                if curId != idQueue[0]:
                    allLocations.append((locQueue[0][0], locQueue[0][0]))
                else:
                    idQueue.popleft()
                    allLocations.append(locQueue.popleft())

            # Now that all the locations are collected, pack them appropriately into
            # offsets. This is the form where offset[i] is the location and
            # offset[i+1]-offset[i] is the size of the data location.
            offsets = list(allLocations[0]) + [loc[1] for loc in allLocations[1:]]
            # Image data offset must be less than or equal to the minimum of locations.
            # This offset may change the value for round tripping but is safer and
            # allows imageDataOffset to not be required to be in the XML version.
            self.imageDataOffset = min(offsets)
            offsetArray = [offset - self.imageDataOffset for offset in offsets]

            dataList = [EblcIndexSubTable.compile(self, ttFont)]
            dataList += [
                struct.pack(dataFormat, offsetValue) for offsetValue in offsetArray
            ]
            # Take care of any padding issues. Only occurs in format 3.
            if offsetDataSize * len(offsetArray) % 4 != 0:
                dataList.append(struct.pack(dataFormat, 0))
            return bytesjoin(dataList)

    return OffsetArrayIndexSubTableMixin

