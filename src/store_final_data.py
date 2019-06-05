
import os
import itertools as it
import numpy as np


import conv_cart_internal_geoms as trimerGeom

def getE0DataObjFromCalcObjs(calcObjList, geomRepStr):

	allDeltaE0 = list()
	allGeoms = list()
	for x in calcObjList:
		allDeltaE0.append( x.e0Diff )

	for x in calcObjList:
		allGeoms.append( x.trimerGeom )

	return ThreeBodyE0Contribs(allGeoms, allDeltaE0, geomRep=geomRepStr)


class ThreeBodyE0Contribs():
	def __init__(self, trimerGeomList:list, deltaE0Values, geomRep="sankey", folder=None, outPath=None):
		self._eqTol = 1e-6
		self.trimerGeomList = trimerGeomList
		self.deltaE0Values = deltaE0Values
		self.geomRep = geomRep.lower()
		self._folder = folder
		self._outPath = outPath

	@classmethod
	def fromFile(cls, inpPath):

		with open(inpPath,"rt") as f:
			fileAsList = f.readlines()

		counter = 0
		dataList = list()
		while counter < len(fileAsList):
			currLine = fileAsList[counter].lower()
			if "elements" in currLine:
				counter += 1
				elements = [x for x in fileAsList[counter].strip().split(",")]
			elif currLine.startswith("#"):
				pass
			elif "geomrepstr" in currLine:
				counter += 1
				geomStr= fileAsList[counter].strip().lower()
			elif "data" in currLine:
				trimerGeomList, deltaE0Values, counter = cls._parseDataSectionOfInpFile(fileAsList, counter, elements, geomStr)
			counter += 1

		return cls(trimerGeomList, deltaE0Values, geomStr, outPath=inpPath)

	@classmethod
	def _parseDataSectionOfInpFile(self, fileAsList, counter, elements, geomRep):
		geomStrToMethod = {"sankey":trimerGeom.TrimerInternGeom.fromSankeyRep,
		                   "bondLengths".lower():trimerGeom.TrimerInternGeom.fromBondLengths}
		getInternGeom = geomStrToMethod[geomRep]

		counter+= 1
		nPoints = int( fileAsList[counter].strip() )
		counter+=1
		allGeoms, allE0 = list(), list()
		for x in range(nPoints):
			currParams = [float(x) for x in fileAsList[counter].strip().split(",")]
			internCoords = getInternGeom(*currParams[:3])
			allGeoms.append( trimerGeom.TrimerGeom(elements, internCoords) )
			allE0.append( currParams[-1] )
			counter += 1	

		return allGeoms, allE0, counter


	def getArrayParamsAgainstValues(self):
		keywordToRepProp = {"sankey":"sankeyRep", "bondLengths".lower():"bondLengths"}
		nCols = len( getattr(self.trimerGeomList[0].internCoords, keywordToRepProp[self.geomRep]) ) + 1
		nRows = len( self.trimerGeomList )
		outArray = np.zeros( (nRows,nCols) )
	
		for rowIdx, (geom, deltaE0) in enumerate(it.zip_longest(self.trimerGeomList, self.deltaE0Values)):
			geomParams = getattr( geom.internCoords, keywordToRepProp[self.geomRep] )
			outArray[rowIdx,:nCols-1] = geomParams
			outArray[rowIdx,-1] = deltaE0

		#Sort final array by each column in turn (Never worked + mine was just naturally in the correct order anyway so....)
#		nDecimals = 1
#		intArray =  np.array(outArray*(10**nDecimals))
#		intArray = intArray.astype(int) #Im relying on behaviour that numbers after the decimal are truncated on conversion
#		intArrayDtypes = [('colA',int), ('colB',int), ('colC',int), ('colD',int)]
#		structIntArray = np.array(intArray, dtype=intArrayDtypes)
#		sortOrder = np.argsort(structIntArray,order=('colA','colB','colC'))
#		sortOrder = np.lexsort( (intArray[:,2],intArray[:,1], intArray[:,0]) )
##		intArray = intArray[sortOrder]


		return outArray


	@property
	def outPath(self):
		if self._outPath is not None:
			return self._outPath
		if self._folder is None:
			folder = os.path.abspath( os.getcwd() )
		else:
			folder = self._folder

		fileName = "{}_{}_{}.e03b".format(*self.elements)
		return os.path.join(folder,fileName) 

	@outPath.setter
	def outPath(self,value):
		self._outPath = value


	@property
	def elements(self):
		return list(self.trimerGeomList[0].elements)

	def writeFile(self):
		outStr = ""
		outStr += "geomRepStr\n{}\n".format(self.geomRep)
		outStr += "elements\n" + ",".join(self.elements) + "\n"
		outStr += "#" + ",".join(self._getArrayHeadings() + ["Delta E0 / eV"]) + "\n"

		outStr += "data\n"
		outStr += "{}\n".format(len(self.trimerGeomList))
		for row in self.getArrayParamsAgainstValues():
			outStr += "{:17.10g}, {:17.10g}, {:17.10g}, {:17.10g}\n".format(*row)

		with open(self.outPath, "wt") as f:
			f.write(outStr)


	def _getArrayHeadings(self):
		if self.geomRep=="sankey":
			headings = ["r_ij", "r_ck", "theta_ick"]
		elif self.geomRep.lower()=="bondlengths":
			headings = ["r_ij", "r_jk", "r_kj"]
		else:
			raise ValueError("{} is an unsupported geomRep".format(self.geomRep))
		return headings


	def __eq__(self,other):
		absTol = min(self._eqTol, other._eqTol)
		if not np.allclose( self.getArrayParamsAgainstValues(), other.getArrayParamsAgainstValues() ,atol=absTol):
			return False

		if self.outPath != other.outPath:
			return False

		return True
