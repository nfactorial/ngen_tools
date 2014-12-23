#
# Provides support for creating a string table used by the ngen game engine.
# A string table is a memory block that contains a collection of ASCII strings.
# This table is used by various objects in the ngen data files.
#

import struct
import ctypes

class ngenStringTable:
    def __init__( self ):
        self.rawStrings = []
        self.stringDictionary = {}
        self.stringOffset = 0

    def len( self ):
        return len( self.rawStrings )

    # We use string offset rather than item index, this allows
    # objects to refer to items without needing an index to
    # offset table.

    def addString( self, newString ):
        if newString == None:
            return 0xFFFFFFFF
        itemOffset = self.stringDictionary.get( newString )
        if itemOffset is None:
            itemOffset = self.stringOffset
            self.rawStrings.append( newString )
            self.stringDictionary[ newString ] = itemOffset
            self.stringOffset += len( newString ) + 1   # +1 because of null terminator
        return itemOffset

    def export( self, binaryWriter ):
        if len( self.rawStrings ) > 0:
            binaryWriter.beginChunk( 'S', 'T', 'T', 'B' )
            for exportString in self.rawStrings:
                binaryWriter.writeAscii( exportString )
            binaryWriter.endChunk()
