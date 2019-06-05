
import copy
import itertools as it
import os
import pathlib

import plato_pylib.plato.mod_plato_inp_files as platoInp
import plato_pylib.plato.parse_plato_out_files as parsePlato
import plato_pylib.shared.ucell_class as UCell
import plato_pylib.utils.job_running_functs as jobRun


def createCalcObjsFromStartFolderTrimerGeomsAndStrDicts(startFolder, trimerGeoms:list, strDictTwoBody, strDictThreeBody):
	allCalcObjs = list()
	for x in trimerGeoms:
		allCalcObjs.append( createCalcObjOneGeom(x, startFolder, strDictTwoBody, strDictThreeBody) )

	return allCalcObjs


def createCalcObjOneGeom(geom, startFolder, strDictTwoBody, strDictThreeBody):
	twoBodyCalc = CalcObjectSingleTrimerJob(geom, strDictTwoBody, "dft2", startFolder, "twoBody")
	threeBodyCalc = CalcObjectSingleTrimerJob(geom, strDictThreeBody, "dft2", startFolder, "threeBody")
	return TrimerE0CalcObject(twoBodyCalc, threeBodyCalc)


def getRunCommsFromListOfCalcObjects(calcObjs):
	outComms = list()
	for x in calcObjs:
		outComms.extend( x.getRunComms() )

	return outComms

class TrimerE0CalcObject():
	
	def __init__(self, twoBodyCalc, threeBodyCalc):
		self.twoBodyCalc = twoBodyCalc
		self.threeBodyCalc = threeBodyCalc

	def writeFiles(self):
		self.twoBodyCalc.writeFile()
		self.threeBodyCalc.writeFile()

	def getRunComms(self):
		return [self.twoBodyCalc.runComm, self.threeBodyCalc.runComm]	

	@property
	def e0Diff(self):
		''' In eV '''
		parsedTwoBody = self.twoBodyCalc.parsedFile
		parsedThreeBody = self.threeBodyCalc.parsedFile
		return parsedThreeBody["energies"].e0Coh - parsedTwoBody["energies"].e0Coh

	@property
	def trimerGeom(self):
		assert self.twoBodyCalc.trimerGeom == self.threeBodyCalc.trimerGeom
		return self.twoBodyCalc.trimerGeom

class CalcObjectSingleTrimerJob():

	def __init__(self, trimerGeom, strDict, progTypeStr, startFolder, extraExt):
		self.trimerGeom = trimerGeom 
		self.strDict = strDict
		self.startFolder = os.path.abspath(startFolder)
		self.extraExt = extraExt
		self.progTypeStr = progTypeStr
		self._boxLength = 100

	@property
	def inpPath(self):
		fileName = self._fileNameWithoutExt
		filePath = os.path.join( self.startFolder, fileName + '.in' )
		return filePath

	@property
	def outPath(self):
		fileName = self._fileNameWithoutExt
		filePath = os.path.join( self.startFolder, fileName + '.out' )
		return filePath

	@property
	def _fileNameWithoutExt(self):
		nameFormat = "{}_{}_{}_{:.3f}_{:.3f}_{:.3f}_{}"
		fileName = nameFormat.format(*self.trimerGeom.elements, *self.trimerGeom.internCoords.sankeyRep, self.extraExt)
		return fileName.replace(".","pt")	

	@property
	def uCellGeom(self):
		lattParams = [self._boxLength for x in range(3)]
		lattAngles = [90.0 for x in range(3)]
		uCell = UCell.UnitCell(lattParams=lattParams, lattAngles = lattAngles)
		fractCoordsPlain = self.trimerGeom.internCoords.getFractCoordsCubicBox(self._boxLength)
		uCell.fractCoords = [x + [y] for x,y in it.zip_longest(fractCoordsPlain, self.trimerGeom.elements)]
		return uCell

	@property
	def parsedFile(self):
		return parsePlato.parsePlatoOutFile_energiesInEv(self.outPath)

	@property
	def runComm(self):
		return jobRun.pathListToPlatoRunComms([self.inpPath],self.progTypeStr)

	def writeFile(self):
		pathlib.Path(self.startFolder).mkdir(exist_ok=True,parents=True)
		geomStrDict = platoInp.getPlatoGeomDictFromUnitCell( self.uCellGeom )
		outStrDict = copy.deepcopy(self.strDict) #Probably overkill, since dict should ONLY contain strings
		outStrDict.update(geomStrDict)
		platoInp.writePlatoOutFileFromDict(self.inpPath, outStrDict)



