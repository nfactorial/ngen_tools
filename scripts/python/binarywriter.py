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

#
# Implements a general binary writer support object to help in writing our
# data to a file. Also supports different endian encodings for the target
# binrary file.
#

import struct


class Endian:
    def __init__(self):
        self.i8Fmt = "=b"
        self.u8Fmt = "=B"
        self.i16Fmt = "=h"
        self.u16Fmt = "=H"
        self.i32Fmt = "=i"
        self.u32Fmt = "=I"
        self.i64Fmt = "=q"
        self.u64Fmt = "=Q"
        self.f32Fmt = "=f"
        self.f64Fmt = "=d"

    def bigEndian(self):
        self.i8Fmt = ">b"
        self.u8Fmt = ">B"
        self.i16Fmt = ">h"
        self.u16Fmt = ">H"
        self.i32Fmt = ">i"
        self.u32Fmt = ">I"
        self.i64Fmt = ">q"
        self.u64Fmt = ">Q"
        self.f32Fmt = ">f"
        self.f64Fmt = ">d"

    def littleEndian(self):
        self.i8Fmt = "<b"
        self.u8Fmt = "<B"
        self.i16Fmt = "<h"
        self.u16Fmt = "<H"
        self.i32Fmt = "<i"
        self.u32Fmt = "<I"
        self.i64Fmt = "<q"
        self.u64Fmt = "<Q"
        self.f32Fmt = "<f"
        self.f64Fmt = "<d"


class BinaryWriter:
    def __init__(self):
        self.endian = Endian()
        self.file = None
        self.fileName = None
        self.nullTerminator = struct.pack('b', 0)
        self.chunks = []

    def littleEndian(self):
        self.endian.littleEndian()

    def bigEndian(self):
        self.endian.bigEndian()

    # TODO: We should update the class to support the 'with' operator when we get the chance
    def open(self, fileName):
        self.file = open(fileName, 'wb')

    def close(self):
        self.file.close()

    # Marks the start of a new chunk with the specified four-cc.
    # Each chunk begins with a FourCC code along with the length of the contained data
    def beginChunk(self, a, b, c, d):
        self.writeFourCC(a, b, c, d)
        self.writeUInt32(0)
        self.chunks.append(self.file.tell())

    def endChunk(self):
        chunkEnd = self.file.tell()
        chunkStart = self.chunks.pop()
        chunkLength = chunkEnd - chunkStart
        self.file.seek(chunkStart - 4, 0)
        self.writeUInt32(chunkLength)
        self.file.seek(0, 2)  # Seek back to end of file

    def writeAscii(self, stringValue):
        self.file.write(stringValue.encode('ascii'))
        self.file.write(self.nullTerminator)

    # Not sure if 'writeInt8' should be called for the characters, will check
    def writeFourCC(self, a, b, c, d):
        self.file.write(a.encode('ascii'))
        self.file.write(b.encode('ascii'))
        self.file.write(c.encode('ascii'))
        self.file.write(d.encode('ascii'))

    def writeBool32(self, value):
        if value:
            self.writeUInt32(1)
        else:
            self.writeUInt32(0)

    def writeInt8(self, value):
        self.file.write(struct.pack(self.endian.i8Fmt, value))

    def writeUInt8(self, value):
        self.file.write(struct.pack(self.endian.u8Fmt, value))

    def writeInt16(self, value):
        self.file.write(struct.pack(self.endian.i16Fmt, value))

    def writeUInt16(self, value):
        self.file.write(struct.pack(self.endian.u16Fmt, value))

    def writeInt32(self, value):
        self.file.write(struct.pack(self.endian.i32Fmt, value))

    def writeUInt32(self, value):
        self.file.write(bytes(struct.pack(self.endian.u32Fmt, value)))

    def writeInt64(self, value):
        self.file.write(struct.pack(self.endian.i64Fmt, value))

    def writeUInt64(self, value):
        self.file.write(struct.pack(self.endian.u64Fmt, value))

    def writeFloat32(self, value):
        self.file.write(struct.pack(self.endian.f32Fmt, value))

    def writeFloat64(self, value):
        self.file.write(struct.pack(self.endian.f64Fmt, value))
