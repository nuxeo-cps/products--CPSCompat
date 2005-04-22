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
"""PatchCMFCoreCMFCatalogAware

reindexObjectSecutiry() optimizations : CMF > 1.5.1

$Id$
"""

from Products.CMFCore.utils import getToolByName
from Products.CMFCore.CMFCatalogAware import CMFCatalogAware

def reindexObjectSecurity(self, skip_self=False):
    """
        Reindex security-related indexes on the object
        (and its descendants).
    """
    catalog = getToolByName(self, 'portal_catalog', None)
    if catalog is not None:
        path = '/'.join(self.getPhysicalPath())
        for brain in catalog.unrestrictedSearchResults(path=path):
            brain_path = brain.getPath()
            # self is treated at the end of the method
            # Optimization in case of an indexable container
            if brain_path == path:
                continue
            ob = self.unrestrictedTraverse(brain_path, None)
            if ob is None:
                # Ignore old references to deleted objects.
                continue
            s = getattr(ob, '_p_changed', 0)
            catalog.reindexObject(ob, idxs=['allowedRolesAndUsers'],
                                  update_metadata=0)
            if s is None: ob._p_deactivate()
        # Reindex the object itself in here if not explicitly
        # asked to not to
        if not skip_self:
            catalog.reindexObject(self, idxs=['allowedRolesAndUsers'],
                                  update_metadata=0)

CMFCatalogAware.reindexObjectSecurity = reindexObjectSecurity
