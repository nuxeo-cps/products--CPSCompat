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
"""Patch CMFCore CMFCatalogAware.

- In CMF < 1.5.2, reindexObjectSecurity does not reindex viewLanguage
  objects corrrectly. See also PatchCMFCoreCatalogTool.py

$Id:$
"""

from zLOG import LOG, PROBLEM
from Acquisition import aq_base
from Products.CMFCore.utils import getToolByName
from Products.CMFCore.CMFCatalogAware import CMFCatalogAware

if True: # keep indentation

    def reindexObjectSecurity(self, skip_self=False):
        """Reindex security-related indexes on the object.

        Recurses in the children to reindex them too.

        If skip_self is True, only the children will be reindexed. This
        is a useful optimization if the object itself has just been
        fully reindexed, as there's no need to reindex its security twice.
        """
        catalog = getToolByName(self, 'portal_catalog', None)
        if catalog is None:
            return
        path = '/'.join(self.getPhysicalPath())
        for brain in catalog.unrestrictedSearchResults(path=path):
            brain_path = brain.getPath()
            if brain_path == path and skip_self:
                continue
            # Get the object
            if hasattr(aq_base(brain), '_unrestrictedGetObject'):
                ob = brain._unrestrictedGetObject()
            else:
                # BBB: Zope 2.7
                ob = self.unrestrictedTraverse(brain_path, None)
            if ob is None:
                # BBB: Ignore old references to deleted objects.
                # Can happen only in Zope 2.7, or when using
                # catalog-getObject-raises off in Zope 2.8
                LOG('reindexObjectSecurity', PROBLEM,
                    "Cannot get %s from catalog" % brain_path)
                continue
            # Recatalog with the same catalog uid.
            s = getattr(ob, '_p_changed', 0)
            catalog.reindexObject(ob, idxs=self._cmf_security_indexes,
                                  update_metadata=0, uid=brain_path)
            if s is None: ob._p_deactivate()

    CMFCatalogAware.reindexObjectSecurity = reindexObjectSecurity
