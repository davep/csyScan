#!/usr/local/bin/python

# csyNG - Write a simple NG source file documenting a Class(y) class
#         hierarchy.
#
# Dave Pearson <davep@davep.org>
#
# Revision History
# ================
# $Log: csyng.py,v $
# Revision 1.2  1998/02/08 16:16:19  davep
# Slight change to use the new interface to ClassyScan().
#
# Revision 1.1  1998/02/04 13:03:03  davep
# Initial revision
#

import sys
from csyScan import ClassyScan

if sys.argv[ 1: ] :
    scanner = ClassyScan( sys.argv[ 1: ] )
else :
    scanner = ClassyScan()

scanner.writeGuideSource = 1
sys.stdout.write( str( scanner.scan() ) )
