Pipeline definition files describe a rendering pipeline for a display port within the engine.
A pipeline can contain a set of resources, these resources are typically render textures that
may be used in the pipeline.
The resource name "back_buffer" is reserved by the system and is used to represent the
rendering pipelines back buffer object.

Defining the render pipeline like this allows us to easily alter the way in which the engine
renders the scene and makes it easy to investigate new techniques.

For example, one pipeline definition describes the rendering for a differed shading process,
whilst another may describe a typical forward renderer.

Whilst we can't simply switch between them as materials are written for one pipeline or
another, it does mean the renderer can switch easily between the two techniques or support
a new pipeline technique in the future.

"width"
Specifies the width of the resource in pixels, if the width is not specified or if the
width is specified as 0, the resource will inherit its width from its parent resource.

"height"
Specifies the height of the resource in pixels, if the height is not specified or if the
height is specified as 0, the resource will inherit its height from its parent resource.

"wScale"
Specifies the scaling of the resources pixel width, this value is only taken relevant
if the pixel width has not been specified using the 'width' parameter. If the resource
inherits its width from the parent resource, the pixel width will be scaled by this value.
For example, if you wish for the resource width to be half the pixel width of the parent
then "wScale" would be 0.5. If "wScale" is not specified, it defaults to "1".

"hScale"
Specifies the scaling of the resources pixel height, this value is only taken relevant
if the pixel height has not been specified using the 'height' parameter. If the resource
inherits its height from the parent resource, the pixel height will be scaled by this value.
For example, if you wish for the resource height to be half the pixel height of the parent
then "hScale" would be 0.5. If "hScale" is not specified, it defaults to "1".

"format"
Specifies the pixel format the resource will have. The different formats are as follows:

"D24S8"			- A 32bit surface format with 24bits for depth and 8bits for stencil.
"R8G8B8A8"		- A 32bit surface format with 8bits for each color channel (red, green, blue and alpha).
"R16G16B16A16"	- A 64bit floating point surface format with 16bits for each color channel (red, green, blue and alpha)
"sRGB_R8G8B8A8"	- A 32bit surface format with 8bits for each color channel (red, green, blue and alpha). Stored in sRGB space.
"R11G11B10F"	- A 32bit floating point surface format with 11bits for the red and green channels and 10bits for the blue channel.
				  This format does not contain an alpha channel and only positive values can be represented.

