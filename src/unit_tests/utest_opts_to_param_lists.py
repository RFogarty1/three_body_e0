#!/usr/bin/python3

import itertools as it
import sys
import unittest

sys.path.append('..')
import opts_to_param_lists as tCode

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

	def testForValsB_addOne(self):
		expList = [1.0,1.1,1.2,1.3,1.4]
		actList = tCode.getLinSpacedSteps(*self.valSetA, inclEnd=True, addOneStep=True)
		[self.assertAlmostEqual(a,b) for a,b in it.zip_longest(expList,actList)]		



class testGetElementsCombinationsFromParams(unittest.TestCase):

	def setUp(self):
		self.testListA = ["Ba", "Bc", "Ab"]
		self.expectedElementsA = set( [  ("Ab", "Ab", "Ab"),
		                                 ("Ab", "Ab", "Ba"),
		                                 ("Ab", "Ab", "Bc"),
		                                 ("Ab", "Ba", "Ba"),
		                                 ("Ab", "Ba", "Bc"),
		                                 ("Ab", "Bc", "Bc"),
		                                 ("Ba", "Ba", "Ba"),
		                                 ("Ba", "Ba", "Bc"),
		                                 ("Ba", "Bc", "Bc"),
		                                 ("Bc", "Bc", "Bc")  ] )


	def testForTripletOfElements(self):
		actResult = tCode.getAllThreeBodyElementCombos(self.testListA)
		self.assertEqual(self.expectedElementsA, actResult)

if __name__ == '__main__':
	unittest.main()

