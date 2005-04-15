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
"""PatchCMFCorePortalFolder

CMFCore.PortalFolder: Cataloging portal folders was prevented by
overriding the typical indexing calls, but one of them was
forgotten, so they still got cataloged.
http://www.zope.org/Collectors/CMF/309

$Id$
"""

from Products.CMFCore.PortalFolder import PortalFolder

def reindexObjectSecurity(self):
    pass

PortalFolder.reindexObjectSecurity = reindexObjectSecurity
