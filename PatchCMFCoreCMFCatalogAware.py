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
""" CMF > 1.5.4 [38390]

Defines now 2 methods, _getCatalogTool() and _getWorkflowTool(), that
are used to find the catalog and workflow tool. It's now possible to
override these methods using inheritence for a given content type to
specify another catalog or workflow tool the content type can use

$Id$
"""

from zLOG import LOG, PROBLEM

from Acquisition import aq_base
from Products.CMFCore.utils import getToolByName
from Products.CMFCore.CMFCatalogAware import CMFCatalogAware

if True:

    def _getCatalogTool(self):
        return getToolByName(self, 'portal_catalog', None)
    CMFCatalogAware._getCatalogTool = _getCatalogTool

    def _getWorkflowTool(self):
        return getToolByName(self, 'portal_workflow', None)
    CMFCatalogAware._getWorkflowTool = _getWorkflowTool

    def indexObject(self):
        """
            Index the object in the portal catalog.
        """
        catalog = self._getCatalogTool()
        if catalog is not None:
            catalog.indexObject(self)
    CMFCatalogAware.indexObject = indexObject

    def unindexObject(self):
        """
            Unindex the object from the portal catalog.
        """
        catalog = self._getCatalogTool()
        if catalog is not None:
            catalog.unindexObject(self)
    CMFCatalogAware.unindexObject = unindexObject

    def reindexObject(self, idxs=[]):
        """
            Reindex the object in the portal catalog.
            If idxs is present, only those indexes are reindexed.
            The metadata is always updated.

            Also update the modification date of the object,
            unless specific indexes were requested.
        """
        if idxs == []:
            # Update the modification date.
            if hasattr(aq_base(self), 'notifyModified'):
                self.notifyModified()
        catalog = self._getCatalogTool()
        if catalog is not None:
            catalog.reindexObject(self, idxs=idxs)
    CMFCatalogAware.reindexObject = reindexObject

    def reindexObjectSecurity(self, skip_self=False):
        """Reindex security-related indexes on the object.

        Recurses in the children to reindex them too.

        If skip_self is True, only the children will be reindexed. This
        is a useful optimization if the object itself has just been
        fully reindexed, as there's no need to reindex its security twice.
        """
        catalog = self._getCatalogTool()
        if catalog is None:
            return
        path = '/'.join(self.getPhysicalPath())

        # XXX if _getCatalogTool() is overriden we will have to change
        # this method for the sub-objects.
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

    def notifyWorkflowCreated(self):
        """
            Notify the workflow that self was just created.
        """
        wftool = self._getWorkflowTool()
        if wftool is not None:
            wftool.notifyCreated(self)
    CMFCatalogAware.notifyWorkflowCreated = notifyWorkflowCreated

    def manage_workflowsTab(self, REQUEST, manage_tabs_message=None):
        """
            Tab displaying the current workflows for the content object.
        """
        ob = self
        wftool = self._getWorkflowTool()
        # XXX None ?
        if wftool is not None:
            wf_ids = wftool.getChainFor(ob)
            states = {}
            chain = []
            for wf_id in wf_ids:
                wf = wftool.getWorkflowById(wf_id)
                if wf is not None:
                    # XXX a standard API would be nice
                    if hasattr(wf, 'getReviewStateOf'):
                        # Default Workflow
                        state = wf.getReviewStateOf(ob)
                    elif hasattr(wf, '_getWorkflowStateOf'):
                        # DCWorkflow
                        state = wf._getWorkflowStateOf(ob, id_only=1)
                    else:
                        state = '(Unknown)'
                    states[wf_id] = state
                    chain.append(wf_id)
        return self._manage_workflowsTab(
            REQUEST,
            chain=chain,
            states=states,
            management_view='Workflows',
            manage_tabs_message=manage_tabs_message)
    CMFCatalogAware.manage_workflowsTab = manage_workflowsTab
