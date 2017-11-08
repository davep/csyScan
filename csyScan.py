#!/usr/local/bin/python

# csyScan - Simple Clipper/Class(y) class scanner.
#
# This is a simple script to run thru a set of Clipper sources and locate
# any Class(y) class definitions. The method used is pretty brain dead
# and could be a lot more elegant. Also, the output format is pretty
# simple too.
#
# Dave Pearson <davep@davep.org>
#
# Revision History
# ================
# $Log: csyscan.py,v $
# Revision 1.5  1998/03/20 11:25:21  davep
# Added the *group instance variables to allow sub-classes to
# override the regular expressions without breaking the code.
#
# Revision 1.4  1998/02/08 16:15:41  davep
# Support for writing output to files. Add the __repr__ method.
#
# Revision 1.3  1998/02/04 13:02:47  davep
# Added support for writing Norton Guide source code.
#
# Revision 1.2  1998/02/02 15:08:03  davep
# Changed the scanner to support FROM as well as INHERIT in the
# Create Class lines.
#
# Revision 1.1  1998/01/31 15:45:22  davep
# Initial revision
#

import re
import sys
import glob

class csyStringAsFile :
    "Build up a string when a file.write() would normally be used"

    def __init__( self ) :
	"Constructor"
	self.text = ""

    def write( self, text ) :
	"Write to the end of the string"
	self.text = self.text + text

    def __repr__( self ) :
	"Represent the object as a string"
	return( self.text )

class ClassyScan :
    "Scan Clipper source code and look for Class(y) class definitions"

    def __init__( self, fileSpec = glob.glob( "*.prg" ) ) :
	"Constructor"
	self.fileSpec          = fileSpec
	self.classes           = {}
	self.definitions       = {}
	self.breakOnFirstMatch = 1
	self.breakOnFuncDef    = 1
	self.writeGuideSource  = 0
	self.indentStr         = "   "
	self.baseGroup         = 1
	self.childGroup        = 3
	self.baseClass         = re.compile( r"^\s*Create\s+Class" + \
					     "\s+([^\s]+)\s*$", \
					     re.IGNORECASE )
	self.childClass        = re.compile( r"^\s*Create\s+Class" + \
					     "\s+([^\s]+)\s+" + \
					     "(Inherit|From)" + \
					     "\s+([^\s]+)\s*$", \
					     re.IGNORECASE )
	self.funcDef           = re.compile( r"^\s*(Static)*\s*Function", \
					     re.IGNORECASE )
	self.endClass          = re.compile( r"\s*End *Class", \
					     re.IGNORECASE )

    def __repr__( self ) :
	"Represent the object as a string"
	text = csyStringAsFile()
	self.writeResults( text )
	return( str( text ) )

    def scan( self ) :
	"Scan source files, building up a class hierarchy"
	self.classes = {}
	for file in self.fileSpec :
	    hFile = open( file, "r" )
	    if hFile :
		while 1 :
		    line = hFile.readline()
		    if not line :
			break
		    if not self.scanBaseClass( hFile, line ) :
			if self.scanChildClass( hFile, line ) :
			    if self.breakOnFirstMatch :
				break
		    elif self.breakOnFirstMatch :
			break
		    if self.funcDef.match( line ) and self.breakOnFuncDef :
			break
		hFile.close()
	return( self )

    def scanBaseClass( self, hFile, line ) :
	"Does the line contain a base class definition?"
	match = self.baseClass.match( line )
	if match :
	    self.classes[ match.group( self.baseGroup ) ]     = None
	    self.definitions[ match.group( self.baseGroup ) ] = self.getDefinition( hFile, line )
	return( match )

    def scanChildClass( self, hFile, line ) :
	"Does the line contain a child class definition?"
	match = self.childClass.match( line )
	if match :
	    self.classes[ match.group( self.baseGroup ) ]     = match.group( self.childGroup )
	    self.definitions[ match.group( self.baseGroup ) ] = self.getDefinition( hFile, line )
	return( match )

    def getDefinition( self, hFile, line ) :
	"Load in the current class definition"
	classDef = [ line ]
	while 1 :
	    line = hFile.readline()
	    classDef.append( line )
	    match = self.endClass.match( line )
	    if match :
		break
	return( classDef )

    def writeResults( self, out = sys.stdout ) :
	"Write the results of the scan to stdout"
	classes = self.classes.keys()
	classes.sort()
	for className in classes :
	    if not self.classes[ className ] :
		out.write( self.classLine( className ) + "\n" )
		self.dumpDef( className, out )
		self.writeChildren( className, out )
	    elif not self.classes.has_key( self.classes[ className ] ) :
		out.write( self.classLine( className + \
					   " (from unknown parent " + \
					   self.classes[ className ] + ")" + \
					   "\n" ) )
		self.dumpDef( className, out )
		self.writeChildren( className, out )

    def writeChildren( self, className, out = sys.stdout, indent = 0 ) :
	"Write out the children of a given class"
	classes = self.classes.keys()
	classes.sort()
	for possibleChild in classes :
	    if self.classes[ possibleChild ] == className :
		out.write( self.classLine( self.indentStr * ( indent + 1 ) + \
					   possibleChild ) + "\n" )
		self.dumpDef( possibleChild, out )
		self.writeChildren( possibleChild, out, indent + 1 )

    def dumpDef( self, className, out = sys.stdout ) :
	"Write out a class definition"
	if self.writeGuideSource :
	    map( lambda s, o = out : o.write( s ), self.definitions[ className ] )

    def classLine( self, line ) :
	"Write out a class name line, taking into accout any NG stuff"
	if self.writeGuideSource :
	    line = "!Short:" + line
	return( line )

if __name__ == "__main__" :
    if sys.argv[ 1: ] :
	sys.stdout.write( str( ClassyScan( sys.argv[ 1: ] ).scan() ) )
    else :
	sys.stdout.write( str( ClassyScan().scan() ) )


