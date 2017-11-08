#!/usr/local/bin/python

# xbppScan - Simple Xbase++ class scanner.
#
# This is a simple script to run thru a set of Xbase++ sources and locate
# any class definitions. The method used is pretty brain dead and could be a
# lot more elegant. Also, the output format is pretty simple too.
#
# Note that for this script to work you also need csyScan.py in your python
# LIB path.
#
# Dave Pearson <davep@hagbard.demon.co.uk>
#
# Revision History
# ================
# $Log: xbppscan.py,v $
# Revision 1.1  1998/03/20 11:30:07  davep
# Initial revision
#

from csyScan import *

class XbppScan( ClassyScan ) :
    "Scan Xbase++ source code and look for class definitions"

    def __init__( self, fileSpec = glob.glob( "*.prg" ) ) :
	"Constructor"

	ClassyScan.__init__( self, fileSpec )

	self.baseGroup  = 2
	self.childGroup = 4

	# Given that the code maybe using mixed Class(y) and Xbase++
	# syntax, we build the regular expressions to cater for both
	# flavours of syntax.

	self.baseClass  = re.compile( r"^\s*(Create\s+)*Class" + \
				      "\s+([^\s]+)\s*$", \
					     re.IGNORECASE )
	self.childClass = re.compile( r"^\s*(Create\s+)*Class" + \
				      "\s+([^\s]+)\s+" + \
				      "(Inherit|From)" + \
				      "\s+([^\s]+)\s*$", \
				      re.IGNORECASE )

if __name__ == "__main__" :
    if sys.argv[ 1: ] :
	sys.stdout.write( str( XbppScan( sys.argv[ 1: ] ).scan() ) )
    else :
	sys.stdout.write( str( XbppScan().scan() ) )
