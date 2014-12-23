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
uniform sampler2D		inputResourceB;

void main()
{
	vec3 diffuseColor = texture2D( inputResourceA, fragTexCoord ).xyz;
	vec3 lighting = texture2D( inputResourceB, fragTexCoord ).xyz;

	outColor = vec4( diffuseColor * lighting, 0.0 );
}
