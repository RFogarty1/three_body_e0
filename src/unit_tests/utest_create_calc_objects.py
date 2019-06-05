#!/usr/bin/python3

import os
import sys
import unittest

sys.path.append('..')

import create_calc_objects as tCode
import conv_cart_internal_geoms as intGeoms

import plato_pylib.shared.ucell_class as UCell

class testCalcObjectSingleTrimerJob(unittest.TestCase):

	def setUp(self):
		self.trimerGeomA = loadTrimerGeomObjA()
		self.startFolderA = os.path.join("test","path")
		self.testStrDictA = {"e0method":"0"}
		self.extraExtA = "twoBody"
		self.progStrA = "dft2"
		self.calcObjA = tCode.CalcObjectSingleTrimerJob(self.trimerGeomA, self.testStrDictA, 
		                                                self.progStrA, self.startFolderA, self.extraExtA)

	def testInpPath(self):
		expInpName = "H_Li_Ge_2pt000_4pt000_180pt000_twoBody.in"
		expInpPath = os.path.abspath( os.path.join(self.startFolderA, expInpName) )
		self.assertEqual(expInpPath, self.calcObjA.inpPath)

	def testUCellGeom(self):
		boxLength = 100 
		self.assertTrue(boxLength==self.calcObjA._boxLength)
		expLattAngles = [90.0, 90.0, 90.0]
		expLattParams = [boxLength for x in range(3)]
		expCartCoords = [ [boxLength/2, boxLength/2, 49.0, "H"],
		                  [boxLength/2, boxLength/2, 51.0, "Li"],
		                  [boxLength/2, boxLength/2, 54.0, "Ge"] ]
		expUCell = UCell.UnitCell(lattParams=expLattParams, lattAngles=expLattAngles)
		expUCell.cartCoords = expCartCoords
		actUCell = self.calcObjA.uCellGeom
		self.assertEqual(expUCell,actUCell)


def loadTrimerGeomObjA():
	sankeyVals = [2.0, 4.0,180.0]
	elementList = ["H","Li","Ge"]
	internCoords = intGeoms.TrimerInternGeom.fromSankeyRep(*sankeyVals)
	return intGeoms.TrimerGeom(elementList, internCoords)


if __name__ == '__main__':
	unittest.main()


