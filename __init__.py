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

import sys

from zLOG import LOG, INFO

import PatchOFSApplication
import PatchCMFCoreFSPythonScript
import PatchPublisherConflictErrors
import PatchZODBTransaction

from OFS.ObjectManager import ObjectManager

from Globals import DTMLFile

# DCWorkflowGraph is not always present
try:
    from Products import DCWorkflowGraph
except ImportError, e:
    if str(e) != 'cannot import name DCWorkflowGraph':
        raise
else:
    import PatchDCWorkflowGraphDCWorkflowGraph

try:
    from Products import ExternalEditor
    # Monkey patch manage_main so that the urls are encoded properly
    ObjectManager.manage_main = DTMLFile('manage_main', globals())
except ImportError:
    if sys.exc_info()[2].tb_next is not None: raise

LOG('CPSCompat', INFO, "Patching for Zope/CMF forward compatibility")
