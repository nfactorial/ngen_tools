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

uniform sampler2D		inputResourceA;

vec3 DecompressNormal( vec3 compressed )
{
	return normalize( compressed * 2.0 - 1.0 );
}

void main()
{
	vec3 sunDirection = normalize( vec3( 0.0, -1.0, 1.0 ) );
//	vec3 sunDirection = normalize( vec3( 0.0, 0.0, 1.0 ) );
//	vec3 sunDirection = vec3( 0.0, -1.0, 0.0 );

	vec3 surfaceNormal = DecompressNormal( texture2D( inputResourceA, fragTexCoord ).xyz );

	float d = max( 0.0f, dot( surfaceNormal, -sunDirection ) );

	// TEMP: Add some ambient:
	d = d + 0.2;

//	d = 0.5 + 0.5 * d;

	outColor = vec4( d, d, d, d );
}
