
import itertools as it
import math
import numpy as np

import conv_cart_internal_geoms as internGeom


def getLinSpacedSteps(startVal,endVal,step, inclEnd=True):
	floatTol = 1e-6
	guessList = np.arange(startVal,endVal,step).tolist()
	#TODO: handle the case of an empty list better
	if len(guessList) == 0:
		raise ValueError("startVal={},endVal={},step={} leads to an empty list".format(startVal,endVal,step))
 
	if abs(endVal-startVal) < step:
		return [startVal]

	#At current numpy uses ceil to figure out number of steps which has the consequence that guessList NEVER has too FEW elements
	#But sometimes has 1 too many. This should only occur when number of steps gets us very close to the endVal
	if floatTol > abs(10*step):
		raise ValueError( "step must be < {}, but value of {} given".format( floatTol/10, step ) )

	#First deal with the case where endVal is very close to the last element
	if abs(endVal - guessList[-1]) < floatTol:
		guessList.pop(-1)

	#arange doesnt include an end value by default
	expNumbSteps = (endVal-startVal)/step
	if (abs( expNumbSteps - math.floor(expNumbSteps) ) < floatTol) and inclEnd:
		guessList.append( guessList[-1] + step )
	elif (abs( expNumbSteps - math.ceil(expNumbSteps) ) < floatTol) and inclEnd:
		guessList.append(guessList[-1] + step)

	return guessList

def generateTrimerGeomsOneElementCombo(elementNames:"list, 3 items", geomParamsA:"list of lists,3xn", geomRepr="sankey" ):
	allCombos = it.product(*geomParamsA)
	allGeoms = list()
	for pA,pB,pC in allCombos:
		internCoords = createInternGeomTrimer(pA,pB,pC,geomRepr)
		allGeoms.append( internGeom.TrimerGeom(elementNames,internCoords) )

	return allGeoms


def createInternGeomTrimer(paramA,paramB,paramC,geomRepr):
	if geomRepr=="sankey":
		outVal = internGeom.TrimerInternGeom.fromSankeyRep(paramA,paramB,paramC)
	else:
		raise ValueError("{} is not a supported geometry representaiton".format(geomRepr))

	return outVal

