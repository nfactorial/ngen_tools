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

layout ( location = 0 ) out vec4		outDiffuse;
layout ( location = 1 ) out vec4		outNormal;

in vec3	fragNormal;
in vec4	fragColor;
in vec2 texCoord1;

uniform sampler2D		grassTexture;
uniform sampler2D		rockTexture;

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

vec3 CompressNormal( vec3 normal )
{
	return 0.5 + ( normal * 0.5 );
}

// We multiply vector * matrix, so that the calculation is done in DirectX style. As our matrices are from direct X.
void main()
{
	vec3 normal = normalize( fragNormal );

	vec4 grassColor = texture2D( grassTexture, texCoord1 );
	vec4 rockColor  = texture2D( rockTexture, texCoord1 );

//	float slope = saturate( pow( normal.y, slopePower ) );			// per-pixel slope, pow value should also be a shader parameter to allow it to be controlled within the editor
	float slope = clamp( pow( normal.y, 8.0 ), 0.0, 1.0 );			// per-pixel slope, pow value should also be a shader parameter to allow it to be controlled within the editor
///	float slope = normal.y;

	vec4 terrainColor = mix( rockColor, grassColor, slope );
//	vec4 terrainColor = mix( grassColor, rockColor, slope );

//	outDiffuse	= vec4( 1.0f, 1.0f, 1.0f, 1.0f );
//	outDiffuse	= vec4( slope, slope, slope, 1.0 );
	outDiffuse	= terrainColor;
//	outDiffuse	= grassColor;
//	outDiffuse	= rockColor;
//	outDiffuse	= grassColor + rockColor;
	outNormal	= vec4( CompressNormal( normal ), 0.0 );

//	mrtDiffuse	= surfaceColor;
//	mrtNormal	= vec4( CompressNormal( normalize( surfaceNormal ) ), roughness );
//	mrtMaterial	= vec4( 0.0f, 0.0f, 0.0f, 0.0f );
}
