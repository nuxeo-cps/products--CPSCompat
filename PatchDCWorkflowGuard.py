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
"""PatchDCWorkflowGuard

check() accept **kw that are propagated to StateChangeInfo() constructor

CMF > 1.5.1

$Id$
"""

from Acquisition import aq_base

from Products.CMFCore.utils import _checkPermission

from Products.DCWorkflow.Expression import StateChangeInfo
from Products.DCWorkflow.Expression import createExprContext

from Products.DCWorkflow.Guard import Guard

if True:

    def check(self, sm, wf_def, ob, **kw):
        """Checks conditions in this guard.
        """
        u_roles = None
        if wf_def.manager_bypass:
            # Possibly bypass.
            u_roles = sm.getUser().getRolesInContext(ob)
            if 'Manager' in u_roles:
                return 1
        if self.permissions:
            for p in self.permissions:
                if _checkPermission(p, ob):
                    break
            else:
                return 0
        if self.roles:
            # Require at least one of the given roles.
            if u_roles is None:
                u_roles = sm.getUser().getRolesInContext(ob)
            for role in self.roles:
                if role in u_roles:
                    break
            else:
                return 0
        if self.groups:
            # Require at least one of the specified groups.
            u = sm.getUser()
            b = aq_base( u )
            if hasattr( b, 'getGroupsInContext' ):
                u_groups = u.getGroupsInContext( ob )
            elif hasattr( b, 'getGroups' ):
                u_groups = u.getGroups()
            else:
                u_groups = ()
            for group in self.groups:
                if group in u_groups:
                    break
            else:
                return 0
        expr = self.expr
        if expr is not None:
            econtext = createExprContext(
                StateChangeInfo(ob, wf_def, kwargs=kw))
            res = expr(econtext)
            if not res:
                return 0
        return 1

Guard.check = check
