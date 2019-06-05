#!/usr/bin/python3

import itertools as it
import sys
import unittest

sys.path.append('..')
import gen_trimer_geoms as tCode
import conv_cart_internal_geoms as convCartInternal




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


