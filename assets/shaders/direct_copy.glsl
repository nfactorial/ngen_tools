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

in vec2	fragTexCoord;

uniform sampler2D		inputResourceA;

void main()
{
	outColor = texture2D( inputResourceA, fragTexCoord );
//	outColor = vec4( fragTexCoord.y, fragTexCoord.x, 0.0, 1.0 );
}
