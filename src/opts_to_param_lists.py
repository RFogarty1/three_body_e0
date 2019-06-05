

#Purpose of this module is to convert user-defined run options (e.g. steps to take) into actual run parameters
#(e.g. a list of ALL steps to take for a bond-length)

import itertools as it
import math
import numpy as np


def getLinSpacedSteps(startVal,endVal,step, inclEnd=True, addOneStep=False):
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

	#Add an extra value if requested, so we always go past(or up to) the cutoff if correct settings used(inclEnd=False,addOneStep=True is likely best)
	if addOneStep:
		guessList.append(guessList[-1] + step)

	return guessList


def getAllThreeBodyElementCombos(elementList:"list, each entry is one element")->set:
	''' Pretty inefficient algorithm used, since i doubt this will ever become a rate-limiting step '''
	allProducts = it.product(elementList, elementList ,elementList)
	allCombos = set()

	for elA,elB,elC in allProducts:
		currTuple = tuple( sorted([elA,elB,elC]) )
		allCombos.add(currTuple)	

	return allCombos


