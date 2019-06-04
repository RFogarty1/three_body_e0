#!/usr/bin/python3

import os
import sys
import unittest

def main():
	#Need to add dirs to path; allows the unit-tests to import test-code.
	startDir = os.path.split( os.path.abspath(os.getcwd(),) )[0]
	codeDirs = [os.path.join(startDir,"src")]
	for x in codeDirs:
		sys.path.append(x)

	#Discover the unit-test files. Note this wouldnt work without the __init__.py files
	loader = unittest.TestLoader()
	suite = loader.discover(startDir, pattern='*utest*.py')
	runner = unittest.TextTestRunner(verbosity=2)
	runner.run(suite)


if __name__ == '__main__':
	main()

