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

import os
from Products import CMFCore
version_file = os.path.join(os.path.dirname(CMFCore.__file__), "version.txt")
version = open(version_file).read().strip()

# XXX: need some test here too...
LOG('CPSCompat', INFO, "Patching for ZODB 3.4 compatibility")
import PatchZODBTransaction

if version == "CMF-1.5.0":
    import PatchCMFCoreSkinnable
    import PatchCMFCorePortalObject
    import PatchCMFCorePortalFolder
    import PatchCMFCoreCMFCatalogAware

    import PatchCMFDefaultDublinCore

    LOG('CPSCompat', INFO, "Patching for Zope/CMF compatibility")

else:
    LOG('CPSCompat', INFO, "Already using (hopefuly) CMF 1.5.1, not patching anything")
