##############################################################################
#
# Copyright (c) 2005 Zope Corporation and Contributors. All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
"""CPSCompat

$Id$
"""

from zLOG import LOG, INFO

import PatchOFSApplication
import PatchPublisherConflictErrors
import PatchZODBTransaction

# DCWorkflowGraph is not always present
try:
    from Products import DCWorkflowGraph
except ImportError, e:
    if str(e) != 'cannot import name DCWorkflowGraph':
        raise
else:
    import PatchDCWorkflowGraphDCWorkflowGraph

LOG('CPSCompat', INFO, "Patching for Zope/CMF forward compatibility")
