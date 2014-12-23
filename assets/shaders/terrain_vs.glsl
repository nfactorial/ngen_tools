//
// Copyright 2014 nfactorial
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//  http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.
//

//
// GLSL shader file.
//

#version 400
#extension GL_ARB_separate_shader_objects : enable

layout( location = 0 ) in vec3		vertexPosition;
layout( location = 1 ) in vec3		vertexNormal;

uniform mat4	worldTransform;
uniform mat4	worldViewProjection;			// World * View * Project transform

uniform vec4	surfaceColor;
uniform vec4	texScale1;

out vec3	fragNormal;
out vec4	fragColor;
out vec2	texCoord1;

// GBuffer layout	:	MRT1	-	Channel 1 -	Diffuse Albedo R
//									Channel 2 - Diffuse Albedo G
//									Channel 3 - Diffuse Albedo B
//									Channel 4 - Specular Intensity
//
//						MRT2	-	Channel 1 - Normal X		- TODO: Use compressed normal
//									Channel 2 - Normal Y
//									Channel 3 - Normal Z
//									Channel 4 - Roughness
//
//						MRT3	-	Channel 1 -
//									Channel 2 -
//									Channel 3 - Material ID
//									Channel 4 - 
//

// We multiply vector * matrix, so that the calculation is done in DirectX style. As our matrices are from direct X.
void main()
{
	gl_Position		= worldViewProjection * vec4( vertexPosition, 1.0 );

	vec4 worldPosition = worldTransform * vec4( vertexPosition, 1.0f );

//	fragNormal		= normalize( mat3( worldTransform ) * vertexPosition ).xyz;			// TODO: Use a mat3
	fragNormal		= normalize( mat3( worldTransform ) * vertexNormal ).xyz;			// TODO: Use a mat3
	texCoord1		= worldPosition.xz * texScale1.xy;
	fragColor		= surfaceColor;
}
