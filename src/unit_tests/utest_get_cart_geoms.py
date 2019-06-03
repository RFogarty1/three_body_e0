#!/usr/bin/python3

import itertools as it
import sys
import unittest

sys.path.append('..')
import conv_cart_internal_geoms as tCode

class testCartFromSankeyForm(unittest.TestCase):

	def setUp(self):
		pass

	def testCaseA_notranslationNeeded(self):
		dAB, dC, theta = 4.0, 3.16227766016838 , 71.565051177078

		expectedGeom = [ [0.0,0.0,0.0],
		                 [0.0,0.0,4.0],
		                 [0.0,3.0,1.0] ]

		testObj = tCode.TrimerInternGeom.fromSankeyRep(dAB,dC,theta)
		actualGeom = testObj.cartCoords

		for posA,posB in it.zip_longest(expectedGeom,actualGeom):
			[self.assertAlmostEqual(exp,act) for exp,act in it.zip_longest(posA,posB)]

	def testCaseA_zeroDegrees(self):
		dAB, dC, theta = 4.0, 5.0, 0.0 

		expectedGeom = [ [0.0,0.0,0.0],
		                 [0.0,0.0,4.0],
		                 [0.0,0.0,-3.0] ]

		testObj = tCode.TrimerInternGeom.fromSankeyRep(dAB,dC,theta)
		actualGeom = testObj.cartCoords

		for posA,posB in it.zip_longest(expectedGeom,actualGeom):
			[self.assertAlmostEqual(exp,act) for exp,act in it.zip_longest(posA,posB)]

	def testCaseA_180Degrees(self):
		dAB, dC, theta = 4.0, 5.0, 180.0 

		expectedGeom = [ [0.0,0.0,0.0],
		                 [0.0,0.0,4.0],
		                 [0.0,0.0,7.0] ]

		testObj = tCode.TrimerInternGeom.fromSankeyRep(dAB,dC,theta)
		actualGeom = testObj.cartCoords

		for posA,posB in it.zip_longest(expectedGeom,actualGeom):
			[self.assertAlmostEqual(exp,act) for exp,act in it.zip_longest(posA,posB)]
		

	def testCaseA_justOver180Degrees(self):
		dAB, dC, theta = 4.0, 5.0, 180.0 +1e-3

		expectedGeom = [ [0.0,0.0,0.0],
		                 [0.0,0.0,4.0],
		                 [0.0,0.0,7.0] ]

		testObj = tCode.TrimerInternGeom.fromSankeyRep(dAB,dC,theta)
		actualGeom = testObj.cartCoords

		for posA,posB in it.zip_longest(expectedGeom,actualGeom):
			[self.assertAlmostEqual(exp,act,places=3) for exp,act in it.zip_longest(posA,posB)]
		

class testGeometryRepOutPuts(unittest.TestCase):

	def setUp(self):
		self.testGeom = [ [0.0,0.0,0.0],
		                 [0.0,0.0,4.0],
		                 [0.0,0.0,7.0] ]
		self.sankeyRep = [4.0, 5.0, 180.0] #dAB, dC, theta


	def testSankeyRep(self):
		tObj = tCode.TrimerInternGeom(self.testGeom)
		sankeyRep = tObj.sankeyRep
		[self.assertAlmostEqual(exp,act) for exp,act in it.zip_longest(self.sankeyRep,sankeyRep)]


class testCartFromCartesian(unittest.TestCase):
	def setUp(self):
		pass

	def testCaseA_onlyTranslationNeeded(self):

		inpGeom = [ [0.5, 1.2, 3.3],
		            [0.5, 1.2, 7.3],
		            [0.5, 4.2, 4.3] ]

		expectedOutGeom = [ [0.0,0.0,0.0],
		                    [0.0,0.0,4.0],
		                    [0.0,3.0,1.0] ]

		testObj = tCode.TrimerInternGeom(inpGeom)
		actualOutGeom = testObj.cartCoords

		for posA,posB in it.zip_longest(expectedOutGeom,actualOutGeom):
			[self.assertAlmostEqual(exp,act) for exp,act in it.zip_longest(posA,posB)]
	

class testFractCoordsInBox(unittest.TestCase):
	def setUp(self):
		pass

	def testCaseA_cubicBox100(self):
		boxSize = 100
		inpGeom = [ [0.0,0.0,0.0],
		            [0.0,0.0,4.0],
		            [0.0,3.0,1.0] ]

		expectedGeom = [ [0.5, 0.50, 0.48],
		                 [0.5, 0.50, 0.52],
		                 [0.5, 0.53, 0.49] ]

		testObj = tCode.TrimerInternGeom(inpGeom)
		actualGeom = testObj.getFractCoordsCubicBox(boxSize)

		for posA,posB in it.zip_longest(expectedGeom,actualGeom):
			[self.assertAlmostEqual(exp,act) for exp,act in it.zip_longest(posA,posB)]


if __name__ == '__main__':
	unittest.main()

