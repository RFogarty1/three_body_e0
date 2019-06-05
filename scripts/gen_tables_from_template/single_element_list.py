
import sys

from get_main_code_dir import getMainCodeDir


import plato_pylib.utils.job_running_functs as jobRun

sys.path.append( getMainCodeDir() )
import create_calc_objects as createObjs
import gen_trimer_geoms as genGeoms
import store_final_data as storeFinal

def genTablesSingleElementList(elementList, geomParams, geomReprStr, startFolder, twoBodyStrDict, threeBodyStrDict, runJobs=True, nCores=1):
	allCalcObjs = createCalcObjs(elementList, geomParams, geomReprStr, startFolder, twoBodyStrDict, threeBodyStrDict)
	[x.writeFiles() for x in allCalcObjs]
	if runJobs:
		allRunComms = createObjs.getRunCommsFromListOfCalcObjects(allCalcObjs)
		jobRun.executeRunCommsParralel(allRunComms,nCores)
	finalData = storeFinal.getE0DataObjFromCalcObjs(allCalcObjs,geomReprStr)
	return finalData

#Note - geomParams is a list of lists. Each contains all values to scan over for one of the geometric parameters
def createCalcObjs(elementList, geomParams, geomReprStr, startFolder, twoBodyStrDict, threeBodyStrDict):
	trimerGeoms = genGeoms.generateTrimerGeomsOneElementCombo(elementList, geomParams, geomRepr=geomReprStr)
	return createObjs.createCalcObjsFromStartFolderTrimerGeomsAndStrDicts(startFolder, trimerGeoms, twoBodyStrDict, threeBodyStrDict)

