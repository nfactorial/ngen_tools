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

out vec4		outColor;

in vec2	fragTexCoord;

uniform float			exposure		= 0.18;
uniform float			bloomStrength	= 1.0f;

uniform float			A				= 0.15;
uniform float			B				= 0.50;
uniform float			C				= 0.10;
uniform float			D				= 0.20;
uniform float			E				= 0.02;
uniform float			F				= 0.20;
uniform float			W				= 11.2;

uniform sampler2D		inputResourceA;
//uniform sampler2D		inputResourceB;
//uniform sampler2D		inputResourceC;

vec3 filmicTonemap( vec3 x )
{
	return ( ( x * ( A * x + C * B ) + D * E ) / ( x * ( A * x + B ) + D * F ) ) - E / F;
}

// Approximates luminance from an RGB value
float CalcLuminance( vec3 color )
{
	return max( dot( color, vec3( 0.212656, 0.715158, 0.072185 ) ), 0.0001f );	// sRGB
//	return max( dot( color, vec3( 0.299f, 0.587f, 0.114f ) ), 0.0001f );	// PAL/NTSC
}

float GetAverageLuminance()
{
	return 0.2f;
}

vec3 CalcExposedColor( vec3 color, float averageLuminance, float threshold, out float outExposure )
{
	averageLuminance = max( averageLuminance, 0.001 );

	float keyValue = exposure;
	float linearExposure = keyValue / averageLuminance;

	outExposure = log2( max( linearExposure, 0.001 ) );
	outExposure -= threshold;

	return exp2( outExposure ) * color;
}

vec3 ToneMap( vec3 color, float averageLuminance, float threshold, out float exposure )
{
	float pixelLuminance = CalcLuminance( color );
	color = CalcExposedColor( color, averageLuminance, threshold, exposure );

	vec3 whiteScale = 1.0 / filmicTonemap( vec3( W ) );

	return filmicTonemap( color ) * whiteScale;
}

void main()
{
//	float averageLuminance = GetAverageLuminance( inputResourceB );
	float averageLuminance = GetAverageLuminance();

	vec3 color = texture2D( inputResourceA, fragTexCoord ).xyz;

	float exposure = 0.0;
	color = ToneMap( color, averageLuminance, 0, exposure );

	// TODO: Apply bloom texture here...

	outColor = vec4( color, 0.0 );
//	outColor = vec4( texture2D( inputResourceA, fragTexCoord ).xyz, 0.0 );
//	outColor = vec4( 0.0, 1.0, 0.0, 0.0 );
}
