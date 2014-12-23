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

out varying vec4		outColor;

in vec2		fragTexCoord;

uniform float		bloomThreshold		= 0.2;
uniform float		exposure			= 0.18;

uniform float A = 0.15;
uniform float B = 0.50;
uniform float C = 0.10;
uniform float D = 0.20;
uniform float E = 0.02;
uniform float F = 0.30;
uniform float W = 11.2;

sampler2D	inputResourceA;

vec3 filmicTonemap( vec3 x )
{
	return ( ( x * ( A * x + C * B ) + D * E ) / ( x * ( A * x + B ) + D * F ) ) - E / F;
}

// Applies the filmic curve from John Hable's presentation
vec3 ToneMapFilmicALU(vec3 color)
{
    color = max(0, color - 0.004f);
    color = (color * (6.2f * color + 0.5f)) / (color * (6.2f * color + 1.7f)+ 0.06f);

    // result has 1/2.2 baked in
    return color;
}

// Approximates luminance from an RGB value
float CalcLuminance(vec3 color)
{
	return max( dot( color, vec3( 0.212656f, 0.715158f, 0.072185f ) ), 0.0001f );	// sRGB
}

// Retrieves the log-average luminance from the texture
float GetAvgLuminance(Texture2D lumTex)
{
    return 0.2f;
}

// Determines the color based on exposure settings
vec3 CalcExposedColor(vec3 color, float avgLuminance, float threshold, out float outExposure)
{
    // Use geometric mean
    avgLuminance = max(avgLuminance, 0.001f);
    float keyValue = exposure;
    float linearExposure = ( keyValue / avgLuminance);
    outExposure = log2(max(linearExposure, 0.0001f));
    outExposure -= threshold;
    return exp2(outExposure) * color;
}

// Uses a lower exposure to produce a value suitable for a bloom pass
vec4 Threshold( vec2 texCoord )
{
    vec3 color = vec3( 0.0, 0.0, 0.0 );

    color = inputResourceA.Sample( linearSampler, texCoord ).rgb;

    // Tone map it to threshold
    float avgLuminance = GetAvgLuminance( inputResourceA );
    float exposure = 0;
    float pixelLuminance = CalcLuminance( color );
	color = CalcExposedColor( color, avgLuminance, bloomThreshold, exposure );

	color = filmicTonemap( color );
	vec3 whiteScale = 1.0f / filmicTonemap( W.xxx );
	color *= whiteScale;

    if(dot(color, 0.333f) <= 0.001f)
        color = 0.0f;

    return vec4(color, 1.0f);
}

void main()
{
	outColor = Threshold( texCoord );
}
