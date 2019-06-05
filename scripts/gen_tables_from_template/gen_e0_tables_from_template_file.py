#!/usr/bin/python3

import argparse
import itertools as it
import os
import sys
import types

import plato_pylib.plato.mod_plato_inp_files as platoInp
import plato_pylib.plato.parse_tbint_files as parseTbint

from get_main_code_dir import getMainCodeDir
sys.path.append(getMainCodeDir())

import opts_to_param_lists as optsToParams
import conv_cart_internal_geoms as internGeoms

import single_element_list as runner

def main():
	allArgs = parseCmdLineArgs()
	opts = createInputOptionsFromCmdLineArgs(allArgs)
	allTables = getAllTables(opts)
	for x in allTables:
		x._folder = opts.startFolder
		x.writeFile()


def parseCmdLineArgs():
	helpMsg = "Generate tables of 3-body e0 corrections for plato"
	parser = argparse.ArgumentParser(description=helpMsg)

	parser.add_argument(dest='templatePath', 
	                    help="Path to a plato input file, only the geometry and e0method will be changed by code")

	parser.add_argument(dest='elementList', nargs='*', 
	                    help="List (just space separated) of elements you want to calculate this for. Order doesnt matter")

	parser.add_argument('--nocalcs', action='store_false', dest='runCalcs',
	                    help = "Flag, include this if you dont want plato calcs to run (only makes sense if you've "
	                           "already run the calcs")

	parser.add_argument('--geomRepr', dest='geomRepr', choices={'sankey','bondlengths'}, default='bondlengths',
	                    action='store', help="How to represent geometry of trimers, e.g. bondlengths works by "
	                    " specifying all the bond lengths in the order r_IJ, r_JK, r_KL (I,J,L in same order as elementList)")

	parser.add_argument('--geomSteps', dest='geomSteps', nargs=3, action='store', default=None,
	                    help = "Step size for each geometric parameter. If using bondlengths best is to pass a a single value "
	                           "three times")

	parser.add_argument('--nCores', dest='nCores', action='store', default=1,
	                    help = "Number of processors to use for running the calculations")	

	parser.add_argument('--startFolder', dest='startFolder', action='store', default="work_folder",
	                    help = "Path (abs or rel) to folder where the calculations will be run/calcd. Will create if doesnt exist")

	return parser.parse_args()



def createInputOptionsFromCmdLineArgs(cmdArgs):
	outObj = InputOptions()
	outObj.elementComboLists = optsToParams.getAllThreeBodyElementCombos(cmdArgs.elementList)
	baseStrDict = {k.lower():v for k,v in platoInp.tokenizePlatoInpFile(cmdArgs.templatePath).items()}

	outObj.geomRepStr = cmdArgs.geomRepr
	outObj.nCores = int(cmdArgs.nCores)

	dFolderPath = getDataFolderPathFromStrDict(baseStrDict)

	cutoffDict = getCutoffValuesAllElements(cmdArgs.elementList, dFolderPath)
	if cmdArgs.geomSteps is None:
		cmdArgs.geomSteps = getDefaultStepValues(cmdArgs.geomRepr)
	outObj.geomParams = getGeomParamsAllElementLists( outObj.elementComboLists, [float(x) for x in cmdArgs.geomSteps] , cutoffDict, cmdArgs.geomRepr) 


	outObj.twoBodyStrDict = getStrDictTwoBodyCalc(baseStrDict)
	outObj.threeBodyStrDict = getStrDictThreeBodyCalc(baseStrDict)
	outObj.startFolder = os.path.abspath(cmdArgs.startFolder)
	outObj.runJobs = cmdArgs.runCalcs



	return outObj


def getStrDictTwoBodyCalc(baseStrDict):
	newDict = {k.lower():v for k,v in baseStrDict.items()}
	newDict["e0method"] = "1"
	return newDict

def getStrDictThreeBodyCalc(baseStrDict):
	newDict = {k.lower():v for k,v in baseStrDict.items()}
	newDict["e0method"] = "0"
	return newDict

def getDataFolderPathFromStrDict(baseStrDict):
	platoRelPath = baseStrDict["dataset"]
	basePath = os.path.join(platoInp.getPlatoRcPath(), platoInp.getTightBindingDataPath())
	dPath = os.path.join(basePath,platoRelPath)
	return dPath


def getCutoffValuesAllElements(elementList, dFolderPath):
	outDict = dict()
	for ele in elementList:
		adtPath = os.path.join(dFolderPath, ele+".adt")
		cutoffVal = parseTbint.parseAdtFile(adtPath)["orbRadius"]
		outDict[ele] = cutoffVal
	return outDict


def getDefaultStepValues(geomRepStr):
	if geomRepStr.lower() == "bondLengths".lower():
		return [1.0,1.0,1.0]
	else:
		raise ValueError("{} is not a supported geometry type".format(geomRepStr))


def getGeomParamsAllElementLists(elementLists, stepValues:"list of lists;x3", orbCutoffs:dict, geomRepStr:str):
	outList = list()
	for x in elementLists:
		outList.append( _getGeomParamsSingleElementList(x, stepValues, orbCutoffs, geomRepStr) )

	return outList

def _getGeomParamsSingleElementList(elementList, stepValues, orbCutoffs:dict, geomRepStr:str):
	if geomRepStr=="bondlengths":
		outVal = _getBondLengthsGeomParams(elementList, stepValues, orbCutoffs)
	else:
		raise ValueError("{} is currently not a supported geometry type".format(geomRepStr))	

	return outVal

def _getBondLengthsGeomParams(elementList, stepValues, orbCutoffs):
	outList = list()

	rijMin, rijMax = 0.1, orbCutoffs[elementList[0]] + orbCutoffs[elementList[1]] #Min=zero means div by zero errors
	rjkMin, rjkMax = 0.1, orbCutoffs[elementList[1]] + orbCutoffs[elementList[2]]
	rikMin, rikMax = 0.1, orbCutoffs[elementList[0]] + orbCutoffs[elementList[2]]

	allMins = [rijMin, rjkMin, rikMin]
	allMaxes = [rijMax, rjkMax, rikMax]
	for minVal, maxVal, stepVal in it.zip_longest(allMins, allMaxes, stepValues):
		currList = optsToParams.getLinSpacedSteps(minVal, maxVal, stepVal, inclEnd=False, addOneStep=True)
		outList.append(currList)

	return outList

def getAllTables(inpArgsObj):
	allTables = list()
	for eleList, geomVals in it.zip_longest(inpArgsObj.elementComboLists , inpArgsObj.geomParams ):
		currTable = runner.genTablesSingleElementList(eleList, geomVals, inpArgsObj.geomRepStr, inpArgsObj.startFolder,
		                                              inpArgsObj.twoBodyStrDict, inpArgsObj.threeBodyStrDict,
		                                              runJobs=inpArgsObj.runJobs ,nCores=inpArgsObj.nCores)
		allTables.append( currTable )
	return allTables





#Goal of this class will be to take the options as a namespace, and use properties
#to translate them into what the code actually needs. (e.g. the elementsList property can check if
#we wanted to use all element combos, and if so figure out all the relevant ones. else take the usr 
#elements and return those ones
class InputOptions:
	def __init__(self):
		self.elementComboLists = None
		self.geomParams = None
		self.geomRepStr = None
		self.startFolder = None
		self.twoBodyStrDict = None
		self.threeBodyStrDict = None
		self.runJobs = False
		self.nCores = None


	def __eq__(self, other):
		return False


def loadTestArgs():
	templatePath = os.path.abspath( os.path.join("test","si.in") )
	nameSpace = types.SimpleNamespace( elementList=["Mg"],
	                                   templatePath = templatePath )
	return nameSpace


if __name__ == '__main__':
	main()
