#!/usr/bin/python3

import itertools as it
import math


class TrimerGeom():
	def __init__(self, elements:"list of 3 str", internCoords:"TrimerInternGeom object"):
		self.elements = elements
		self.internCoords = internCoords 

	def __eq__(self,other):
		if self.internCoords != other.internCoords:
			return False
		if self.elements != other.elements:		
			return False
		return True

class TrimerInternGeom():
	def __init__(self, cartCoords):
		''' NEVER call this directly unless you know what your doing '''
		assert len(cartCoords)==3, "TimerInternGeom only works for trimers, but you've given it {} atoms".format(len(cartCoords))
		self.cartCoords = cartCoords
		self._translateCartCoordsToBondAxisAB()
		self._eqTol = 1e-6

	def _translateCartCoordsToBondAxisAB(self):
		atomATransVector = [x for x in self.cartCoords[0]]
		for idx,atom in enumerate(self.cartCoords):
			self.cartCoords[idx] = [x-tVect for x,tVect in it.zip_longest(atom,atomATransVector)]

	@classmethod
	def fromSankeyRep(self, dAB, dC, theta:"In degrees"):
		''' Get Geometry from bondlength (dAB), distance of neighbour from bond center and angle between bond center and neighbour '''
		atomAPos = [0,0,0]
		atomBPos = [0,0,dAB]

		bondCenterPos = [0,0,dAB/2]
		dB = 0.5*dAB

		cZ = ( ( math.cos( math.radians(theta) ) * dC * dB ) / (-dB) ) + (0.5*dAB)

		dZMinusCz = dB - cZ

		cY = math.sqrt( (dC**2) - (dZMinusCz**2) )
		atomCPos = [0,cY,cZ]


		return TrimerInternGeom([atomAPos,atomBPos,atomCPos])

	@property
	def sankeyRep(self):
		bondCentPos = [(x-y)/2 for x,y in it.zip_longest(self.cartCoords[1],self.cartCoords[0])]
		dAB = math.sqrt( sum( [ (x-y)**2 for x,y in it.zip_longest(self.cartCoords[0],self.cartCoords[1]) ]) )
		dC =  math.sqrt( sum( [ (x-y)**2 for x,y in it.zip_longest(bondCentPos,self.cartCoords[2]) ] ) )
		
		#Get the angle from bond center to the neighbour
		errorTol=1e-4
		bToD = [(x-y) for x,y in it.zip_longest(bondCentPos, self.cartCoords[1])]
		dToC = [(x-y) for x,y in it.zip_longest(self.cartCoords[2],bondCentPos)]
		lenBD = math.sqrt( sum( [ x**2 for x in bToD ] ) )
		lenDC = math.sqrt(sum( [ x**2 for x in dToC ] ) )
		dotProd = sum([x*y for x,y in it.zip_longest(bToD,dToC)])

		cosTheta = dotProd / (lenBD*lenDC)

		if abs(cosTheta-1) < errorTol:
			cosTheta = 1.0
		elif abs(cosTheta+1) < errorTol:
			cosTheta = -1.0

		return dAB,dC,math.degrees(math.acos(cosTheta))

	@property
	def bondLengths(self):
		lenAB = getDistBetweenTwoVects(self.cartCoords[0],self.cartCoords[1])
		lenBC = getDistBetweenTwoVects(self.cartCoords[1],self.cartCoords[2])
		lenAC = getDistBetweenTwoVects(self.cartCoords[0],self.cartCoords[2]) 
		bondLengths = [lenAB,lenBC,lenAC]
		return bondLengths

	def getFractCoordsCubicBox(self, boxLength:float):
		centerZ = (self.cartCoords[1][2] - self.cartCoords[0][2])/2 #ASSUMES atom 0 is at origin, and atom1 aligned along z already(i.e. only z components)
		centerPos = [0,0,centerZ] 

		outGeom = list()
		for atom in self.cartCoords:
			relToCent = [x-centerPos for x,centerPos in it.zip_longest(atom,centerPos)]
			currFractCoords = [0.5 + (x/boxLength) for x in relToCent]
			outGeom.append(currFractCoords)
		return outGeom

	def __eq__(self, other):
		eqTol = min(self._eqTol, other._eqTol)
		for x,y in it.zip_longest(self.sankeyRep, other.sankeyRep):
			if abs(x-y) > eqTol:
				return False
		return True


def getDistBetweenTwoVects(vectA,vectB):
	return math.sqrt( sum( [ (x-y)**2 for x,y in it.zip_longest(vectA,vectB) ]) )

