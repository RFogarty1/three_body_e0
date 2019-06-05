
import os

def getMainCodeDir():
	thisFile = os.path.realpath(__file__) #Should call abs path aswell, but not expanduser (i.e. ~ for HOME will break things)
	basePath = os.path.split( os.path.split( os.path.split(thisFile)[0] )[0] ) [0]
	codePath = os.path.join(basePath,"src")
	return codePath
