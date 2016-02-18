#
# Copyright 2014 nfactorial
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#  http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#


class ngenStringTable:
    """
    Provides support for creating a string table used by the ngen game engine.
    A string table is a memory block that contains a collection of ASCII strings.
    This table is used by various objects in the ngen data files.
    """
    def __init__( self ):
        self.rawStrings = []
        self.stringDictionary = {}
        self.stringOffset = 0

    def __len__(self):
        """
        :return: The number of strings contained within the string table.
        """
        return len(self.rawStrings)

    # We use string offset rather than item index, this allows
    # objects to refer to items without needing an index to
    # offset table.

    def addString(self, newString):
        if newString is None:
            return 0xFFFFFFFF
        itemOffset = self.stringDictionary.get(newString)
        if itemOffset is None:
            itemOffset = self.stringOffset
            self.rawStrings.append(newString)
            self.stringDictionary[newString] = itemOffset
            self.stringOffset += len(newString) + 1   # +1 because of null terminator
        return itemOffset

    def export(self, binaryWriter):
        """
        Writes the contents of the string table to the specified binary data file.
        :param binaryWriter: The writer to be used when exporting the table.
        :return: Nothing
        """
        if len(self.rawStrings) > 0:
            binaryWriter.beginChunk('S', 'T', 'T', 'B')
            for exportString in self.rawStrings:
                binaryWriter.writeAscii(exportString)
            binaryWriter.endChunk()
