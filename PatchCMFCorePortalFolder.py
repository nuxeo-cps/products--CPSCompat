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
"""Patch CMFCore PortalFolder.

Allow root doted prefixed object name overrides

In CMF > 1.5.3

$Id$
"""

from Acquisition import aq_parent, aq_inner
from AccessControl import getSecurityManager

from Products.CMFCore.exceptions import BadRequest
from Products.CMFCore.permissions import ManagePortal
from Products.CMFCore.PortalFolder import PortalFolderBase
from Products.CMFCore.PortalFolder import PortalFolder

if True: # keep indentation

    def _checkId(self, id, allow_dup=0):
        PortalFolderBase.inheritedAttribute('_checkId')(self, id, allow_dup)

        if allow_dup:
            return

        # FIXME: needed to allow index_html for join code
        if id == 'index_html':
            return

        # Another exception: Must allow "syndication_information" to enable
        # Syndication...
        if id == 'syndication_information':
            return

        # This code prevents people other than the portal manager from
        # overriding skinned names and tools.
        if not getSecurityManager().checkPermission(ManagePortal, self):
            ob = self
            while ob is not None and not getattr(ob, '_isPortalRoot', False):
                ob = aq_parent( aq_inner(ob) )
            if ob is not None:
                # If the portal root has a non-contentish object by this name,
                # don't allow an override.
                if (hasattr(ob, id) and
                    id not in ob.contentIds() and
                    # Allow root doted prefixed object name overrides
                    not id.startswith('.')):
                    raise BadRequest('The id "%s" is reserved.' % id)
            # Don't allow ids used by Method Aliases.
            ti = self.getTypeInfo()
            if ti and ti.queryMethodID(id, context=self):
                raise BadRequest('The id "%s" is reserved.' % id)
        # Otherwise we're ok.
        
    PortalFolder._checkId = _checkId
