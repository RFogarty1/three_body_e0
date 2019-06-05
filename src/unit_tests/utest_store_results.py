#!/usr/bin/python3

import sys
import numpy as np
import unittest
#import unittest.mock as mock

sys.path.append('..')
import store_final_data as tCode
import conv_cart_internal_geoms as geoms

class testReadAndWrite(unittest.TestCase):

	def setUp(self):
		self.outPathA = "test_out_path.e0Test"
		trimerGeoms = createTrimerGeomsA()
		deltaE0Vals = [4.44,5.50]

		self.objA = tCode.ThreeBodyE0Contribs( trimerGeoms, deltaE0Vals, geomRep="bondLengths")
		self.objA.outPath = self.outPathA

	def testReadAndWriteConsistent(self):
		self.objA.writeFile()
		actObj = tCode.ThreeBodyE0Contribs.fromFile( self.outPathA )
		expObj = self.objA
		self.assertEqual(expObj,actObj)




def createTrimerGeomsA():
	params = [ [2.0, 1.0, 1.0], [4.1, 2.9, 1.8] ]
	elements = ["Xa","Xb","Xc"] #Not needed, since i can set my own outpath

	outList = list()
	for x in params:
		internCoords = geoms.TrimerInternGeom.fromBondLengths(*x)
		outList.append( geoms.TrimerGeom(elements, internCoords) )

	return outList

if __name__ == '__main__':
	unittest.main()

