#
#
#

from ngen_material import ngenMaterial
from string_table import ngenStringTable
from shader_parameter_exporter import ShaderParameterExporter

# Theory: Derive from 'GenerticExporter', pass content type and version to base
# class. When loading an asset the exporter looks up the object registered for
# the type and version. Then calls 'addItem' or something. The core export
# module then loops through each object and calls it's 'export' method?

class ngenMaterialExporter:
	def __init__( self ):
		self.materials = []
		self.stringTable = ngenStringTable()
		self.parameters = []

	def addMaterial( self, fileName ):
		newMaterial = ngenMaterial()
		newMaterial.load( fileName )
		self.materials.append( newMaterial )
		self.commitMaterial( newMaterial )

	def export( self, binaryWriter ):
		if len( self.materials ) > 0:
			for material in self.materials:
				binaryWriter.beginChunk( 'M', 'T', 'R', 'L' )
				self.stringTable.export( binaryWriter )
				self.exportData( binaryWriter, material )
				self.exportParameters( binaryWriter )
				#self.exportTextures( binaryWriter )
				binaryWriter.endChunk()

	def commitMaterial( self, material ):
		self.stringTable.addString( material.name )
		self.stringTable.addString( material.layer )
		self.stringTable.addString( material.vertexShader )
		self.stringTable.addString( material.pixelShader )
		self.stringTable.addString( material.shadowShader )
		material.baseInstanceParameterIndex = len( self.parameters )
		for parameter in material.instanceParameters:
			parameter.stringIndexName = self.stringTable.addString( parameter.paramName )
			self.parameters.append( parameter )
		material.baseSharedParameterIndex = len( self.parameters )
		for parameter in material.sharedParameters:
			parameter.stringIndexName = self.stringTable.addString( parameter.paramName )
			self.parameters.append( parameter )
		for textureName in material.textures:
			self.stringTable.addString( textureName )

	def exportParameters( self, binaryWriter ):
		binaryWriter.beginChunk( 'P', 'A', 'R', 'M' )
		for parameter in self.parameters:
			binaryWriter.writeUInt32( parameter.stringIndexName )
			binaryWriter.writeUInt32( parameter.typeIndex )
			binaryWriter.writeUInt32( parameter.dataOffset )
			binaryWriter.writeUInt32( parameter.textureUnit )
		binaryWriter.endChunk()

	def exportData( self, binaryWriter, material ):
		binaryWriter.beginChunk( 'I', 'N', 'F', 'O' )
		self.exportMaterialInfo( binaryWriter, material )
		binaryWriter.endChunk()

	def exportMaterialInfo( self, binaryWriter, material ):
		binaryWriter.writeUInt32( self.stringTable.addString( material.name ) )
		binaryWriter.writeUInt32( self.stringTable.addString( material.layer ) )
		binaryWriter.writeUInt32( self.stringTable.addString( material.vertexShader ) )
		binaryWriter.writeUInt32( self.stringTable.addString( material.pixelShader ) )
		binaryWriter.writeUInt32( self.stringTable.addString( material.shadowShader ) )
		binaryWriter.writeUInt32( len( material.textures ) )
		binaryWriter.writeUInt32( len( material.sharedParameters ) )
		binaryWriter.writeUInt32( len( material.instanceParameters ) )
