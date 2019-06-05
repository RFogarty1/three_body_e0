
import itertools as it
import math

import conv_cart_internal_geoms as internGeom



def generateTrimerGeomsOneElementCombo(elementNames:"list, 3 items", geomParamsA:"list of lists,3xn", geomRepr="sankey" ):
	allCombos = it.product(*geomParamsA)
	allGeoms = list()
	for pA,pB,pC in allCombos:
		try :
			internCoords = createInternGeomTrimer(pA,pB,pC,geomRepr)
		except internGeom.NotATriangleError:
			pass
		else:
			allGeoms.append( internGeom.TrimerGeom(elementNames,internCoords) )

	return allGeoms


def createInternGeomTrimer(paramA,paramB,paramC,geomRepr):
	if geomRepr=="sankey":
		outVal = internGeom.TrimerInternGeom.fromSankeyRep(paramA,paramB,paramC)
	elif geomRepr=="bondlengths":
		outVal = internGeom.TrimerInternGeom.fromBondLengths(paramA,paramB,paramC)
	else:
		raise ValueError("{} is not a supported geometry representaiton".format(geomRepr))

	return outVal

