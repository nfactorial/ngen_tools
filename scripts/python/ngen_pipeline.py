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

# This map is used to convert the named surface pixel format to our enumerated value type.
surfaceFormatMap = {"R8G8B8A8": 1, "sRGB_R8G8B8A8": 2, "R16G16B16A16": 3, "R11G11B10F": 4, "D24S8": 5}


# Represents a resource in the display pipeline.
# A display resource is a texture surface, its width and height can be
# specified explicitly or taken from the inherited resource.
# It also has a texture format, which specifies how the surface is
# stored in video memory.
# If a display resources width or height is zero, their actual width is
# taken from the inherited resource.
# The surfaces width and height is multiplied by wScale and hScale
# respectively to determine the actual surface size.
# The rendering pipeline provides an intrinsic surface called "back_buffer"
# which refers to the output backbuffer. The name "back_buffer" is reserved
# by the system.
class ngenDisplayResource:
    def __init__(self):
        self.name = -1
        self.inherit = -1
        self.format = 0
        self.width = 0
        self.height = 0
        self.wScale = 1.0
        self.hScale = 1.0

    def loadJson(self, stringTable, jsonData):
        self.name = stringTable.addString(jsonData["name"])
        self.inherit = stringTable.addString(jsonData["inherit"])
        if surfaceFormatMap[jsonData["format"]]:
            self.format = surfaceFormatMap[jsonData["format"]]
        else:
            print("Unknown texture format " + jsonData["format"] + " specified in display resource.")

        if jsonData.get("width") is not None:
            self.width = jsonData["width"]
        if jsonData.get("height") is not None:
            self.height = jsonData["height"]
        if jsonData.get("wScale") is not None:
            self.wScale = jsonData["wScale"]
        if jsonData.get("hScale") is not None:
            self.hScale = jsonData["hScale"]

    def export(self, binaryWriter):
        binaryWriter.writeUInt32(self.name)
        binaryWriter.writeUInt32(self.inherit)
        binaryWriter.writeUInt32(self.format)
        binaryWriter.writeUInt32(self.width)
        binaryWriter.writeUInt32(self.height)
        binaryWriter.writeFloat32(self.wScale)
        binaryWriter.writeFloat32(self.hScale)


# This class defines the clear operation to be performed before a layer is executed.
class ngenClearInfo:
    def __init__(self):
        self.clearColor = False
        self.clearDepth = False
        self.stencilValue = 0
        self.depthValue = 1.0
        self.color = [0.0, 0.0, 0.0, 0.0]

    def loadJson(self, jsonData):
        if jsonData.get("clearColor") is not None:
            self.clearColor = jsonData["clearColor"]
        if jsonData.get("clearDepth") is not None:
            self.clearDepth = jsonData["clearDepth"]
        if jsonData.get("stencilValue") is not None:
            self.stencilValue = jsonData["stencilValue"]
        if jsonData.get("depthValue") is not None:
            self.depthValue = jsonData["depthValue"]
        if jsonData.get("colorValue") is not None:
            self.depthColor = jsonData["colorValue"]

    def export(self, writer):
        writer.writeBool32(self.clearColor)
        writer.writeBool32(self.clearDepth)
        writer.writeUInt32(self.stencilValue)
        writer.writeFloat32(self.depthValue)
        writer.writeFloat32(self.color[0])
        writer.writeFloat32(self.color[1])
        writer.writeFloat32(self.color[2])
        writer.writeFloat32(self.color[3])


# Descrtibes a frame-buffer used as a target for rendering.
class ngenFrameBuffer:
    def __init__(self):
        self.name = -1
        self.targets = []
        self.depthTarget = -1
        self.readOnlyDepth = false

    def loadJson(self, stringTable, jsonData):
        self.name = stringTable.addString(jsonData["name"])
        if jsonData.get("targets") is not None:
            for target in jsonData["targets"]:
                self.targets.append(stringTable.addString(target))
        if jsonData.get("depthTarget") is not None:
            self.depthTarget = stringTable.addString(jsonData["depthTarget"])
        if jsonData.get("readOnlyDepth") is not None:
            self.readOnlyDepth = jsonData["readOnlyDepth"]

    def export(self, binaryWriter):
        binaryWriter.writeUInt32(self.name)
        # TODO: Write 4 entries (maximum supported targets)
        for target in self.targets:
            binaryWriter.writeUInt32(target)
        binaryWriter.writeInt32(self.depthTarget)
        binaryWriter.writeBool32(self.readOnlyDepth)


class ngenGenerator:
    def __init__(self):
        self.name = -1
        self.frameBuffer = -1
        self.resources = []
        self.material = -1

    def loadJson(self, stringTable, jsonData):
        self.name = stringTable.addString(jsonData["name"])
        if jsonData.get("frameBuffer") is not None:
            self.frameBuffer = stringTable.addString(jsonData["frameBuffer"])
        if jsonData.get("material") is not None:
            self.material = stringTable.addString(jsonData["material"])
        if jsonData.get("resources") is not None:
            for resource in jsonData.get("resources"):
                self.resources.append(stringTable.addString(resource))

    def export(self, binaryWriter):
        binaryWriter.writeUInt32(self.name)
        binaryWriter.writeInt32(self.frameBuffer)
        binaryWriter.writeInt32(self.material)

    # TODO: Write out four integers for the resources referenced by the generator


class ngenRenderLayer:
    """
    Descrribes a single layer in the rendering pipeline. Render layers specify a render layer
    which is used as a target for all rendering performed in the layer, if no target is
    specified then objects cannot be rendered within the layer.
    Layers may also specify generators (probably needs to be renamed), generators perform
    special rendering operatons. Such as bloom, hdr etc.
    """
    def __init__(self):
        self.name = -1
        self.frameBuffer = -1
        self.inverted = False
        self.generators = []
        self.clearInfo = ngenClearInfo()

    def loadJson(self, stringTable, jsonData):
        self.name = stringTable.addString(jsonData["name"])
        if jsonData.get("inverted"):
            self.inverted = jsonData.get("inverted")
        if jsonData.get("frameBuffer"):
            self.frameBuffer = stringTable.addString(jsonData["frameBuffer"])
        # TODO: Load generators
        if jsonNData.get("clear"):
            self.clearInfo.loadJson(jsonData["clear"])

    def export(self, binaryWriter):
        binaryWriter.writeUInt32(self.name)
        binaryWriter.writeInt32(self.frameBuffer)
        binaryWriter.writeBool32(self.inverted)
        # TODO: Write start generator index
        # 		Write number of generators
        self.clearInfo.export(binaryWriter)


# Defines a rendering pipeline within the engine, a rendering pipeline consists of multiple
# render layers which are executed in-order. Materials, used for rendering geometry, specify
# which layer they belong to.
class ngenPipeline:
    def __init__(self):
        self.name = ""
        self.stringTable = ngenStringTable()
        self.layers = []
        self.resources = []
        self.frameBuffers = []
        self.generators = []

    # TODO: Store strings locally when loading, add them to table during export.
    #		This allows us to work in terms of a Material exporter rather than us
    #		having to know how everything works.
    #		Also allows us to completely redo the exporter if necessary without
    #		having to change the material definition object

    def loadJson(self, jsonData):
        self.name = jsonData["name"]
        if jsonData.get("resources") is not None:
            self.loadResources(jsonData["resources"])
        if jsonData.get("frameBuffers") is not None:
            self.loadFrameBuffers(jsonData["frameBuffers"])
        if jsonData.get("layers") is not None:
            self.loadLayers(jsonData["layers"])

    def loadResources(self, jsonData):
        for resource in jsonData:
            newResource = ngenDisplayResource()
            newResource.loadJson(self.stringTable, resource)
            self.resources.append(newResource)

    def loadFrameBuffers(self, jsonData):
        for frameBuffer in jsonData:
            newFrameBuffer = ngenFrameBuffer()
            newFrameBuffer.loadJson(self.stringTable, frameBuffer)
            self.frameBuffers.append(newFrameBuffer)

    def loadLayers(self, jsonData):
        for layer in jsonData:
            newLayer = ngenRenderLayer()
            newLayer.loadJson(layer)
            self.layers.append(newLayer)

    def export(self, binaryWriter):
        binaryWriter.beginChunk('P', 'I', 'P', 'E')
        self.stringTable.export(binaryWriter)
        self.exportInfo(binaryWriter)
        self.exportResources(binaryWriter)
        self.exportFrameBuffers(binaryWriter)
        self.exportLayers(binaryWriter)
        binaryWriter.endChunk()

    def exportInfo(self, binaryWriter):
        binaryWriter.beginChunk('I', 'N', 'F', 'O')
        binaryWriter.writeUInt32(len(self.layers))
        binaryWriter.writeUInt32(len(self.resources))
        binaryWriter.endChunk()

    def exportResources(self, binaryWriter):
        if len(self.resources) > 0:
            binaryWriter.beginChunk('R', 'S', 'C', 'E')
            for resource in self.resources:
                resource.export(binaryWriter)
            binaryWriter.endChunk()

    def exportFrameBuffers(self, binaryWriter):
        if len(self.frameBuffers) > 0:
            binaryWriter.beginChunk('F', 'M', 'B', 'F')
            for frameBuffer in self.frameBuffers:
                frameBuffer.export(binaryWriter)
            binaryWriter.endChunk()

    def exportLayers(self, binaryWriter):
        if len(self.layers) > 0:
            binaryWriter.beginChunk('L', 'A', 'Y', 'R')
            for layer in self.layers:
                layer.export(binaryWriter)
            binaryWriter.endChunk()
