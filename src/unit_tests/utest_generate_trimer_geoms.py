#!/usr/bin/python3

import itertools as it
import sys
import unittest

sys.path.append('..')
import gen_trimer_geoms as tCode
import conv_cart_internal_geoms as convCartInternal

class testGetStepValuesFromParams(unittest.TestCase):

	def setUp(self):
		self.valSetA = [1.0, 1.3, 0.1] #End point falls on one of the vals; hence tricky case that arange fails on
		self.valSetB = [0.9, 1.3, 0.15 ] #Should be a simple case

	def testForValsA_exclEnd(self):
		expList = [1.0,1.1,1.2]
		actList = tCode.getLinSpacedSteps(*self.valSetA, inclEnd=False)
		[self.assertAlmostEqual(a,b) for a,b in it.zip_longest(expList,actList)]


	def testForValsA_inclEnd(self):
		expList = [1.0,1.1,1.2,1.3]
		actList = tCode.getLinSpacedSteps(*self.valSetA, inclEnd=True)
		[self.assertAlmostEqual(a,b) for a,b in it.zip_longest(expList,actList)]

	
	def testForValsB_inclEnd(self):
		expList = [0.9, 1.05,1.20]
		actList = tCode.getLinSpacedSteps(*self.valSetB, inclEnd=True)
		[self.assertAlmostEqual(a,b) for a,b in it.zip_longest(expList,actList)]


	def testForValsA_exclEnd_reversed(self):
		expList = [1.3,1.2,1.1]
		actList = tCode.getLinSpacedSteps(self.valSetA[1], self.valSetA[0], -1*self.valSetA[2], inclEnd=False)
		[self.assertAlmostEqual(a,b) for a,b in it.zip_longest(expList,actList)]



class testGenTrimerGeoms(unittest.TestCase):

	def setUp(self):
		self.elementNamesA = ["H","Li","Mg"]
		self.geomParamsA = [ [0.1,0.2], [3.3,3.4], [120.0] ]
		self.geomReprA = "sankey"
		self.expResA = loadTrimerGeomListA()

	def testCorrectGeomsSetA(self):
		actGeoms = tCode.generateTrimerGeomsOneElementCombo(self.elementNamesA, self.geomParamsA, geomRepr=self.geomReprA)
		[self.assertEqual(x,y) for x,y in it.zip_longest(self.expResA,actGeoms)]


def loadTrimerGeomListA():
	elementList = ["H","Li","Mg"]
	allGeomsIntern = list()
	allGeomsIntern.append( convCartInternal.TrimerInternGeom.fromSankeyRep(0.1,3.3,120.0) )
	allGeomsIntern.append( convCartInternal.TrimerInternGeom.fromSankeyRep(0.1,3.4,120.0) )
	allGeomsIntern.append( convCartInternal.TrimerInternGeom.fromSankeyRep(0.2,3.3,120.0) )
	allGeomsIntern.append( convCartInternal.TrimerInternGeom.fromSankeyRep(0.2,3.4,120.0) )

	allGeoms = [convCartInternal.TrimerGeom(elementList, x) for x in allGeomsIntern]
	return allGeoms



if __name__ == '__main__':
	unittest.main()


