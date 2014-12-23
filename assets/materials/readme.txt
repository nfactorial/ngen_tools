Material definitions are used to describe a material resource used by the engine.
A material specifies the attributes necessary for rendering a collection of
geometric primitives, the file is stored as a human readable json definition.

"metaData"

The root element may contain a 'metaData' chunk which contains extra information
about the file itself. The meta data may specify the version number of the
file format and the type of content described by the file. For example, if
the json file contains a material description, version 1, the meta data wlil look:

"metaData": {
	"contentType": "material",
	"contentVersion": 1
}

The meta data section may be extended in the future.



"name"
This attribute contains the name of the material, each material must have a
unique name. The name is usually the same as the material filename without
the .json extension. However this is not required, when processed by the
exporter the produced file will be <material name>.mtl



"layer"
This specifies the name of the render layer the material expects to be
processed in. If the layer does not exist at run time, the material
will be ignored and the geometry will not be rendered.



"shadowShader"
This specifies the shader to be used when rendering shadow geometry using
the material. This is typically a simplified copy of the vertex shader
with any colour calculations removed. If a shadow shader is not specified
then shadows wll not be drawn for the geometry.


"vertexShader"
Specifies the shader to be used when rendering the geometry normally
with the material.


"pixelShader"
Specifies the pixel (fragment) shader to be used when rendering geometry
normally with the material.


"instanceParameters"
Specifies the parameters associated with the material that may be changed
on a per-instance basis.

TODO: Also need to add 'shared' parameters.