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
"""PatchDCWorkflowDCWorkflow

_checkTransitionGuard() supports **kw arguments and propagates them to
the guard.check() method. isActionSupported() uses now this facility
as well and propagates **kw to the guard.check() method

CMF > 1.5.1

$Id$
"""

from AccessControl import Unauthorized

from Products.CMFCore.WorkflowCore import WorkflowException

from Products.DCWorkflow.Transitions import TRIGGER_USER_ACTION
from Products.DCWorkflow.DCWorkflow import DCWorkflowDefinition

if True:

    def isActionSupported(self, ob, action, **kw):
        '''
        Returns a true value if the given action name
        is possible in the current state.
        '''
        sdef = self._getWorkflowStateOf(ob)
        if sdef is None:
            return 0
        if action in sdef.transitions:
            tdef = self.transitions.get(action, None)
            if (tdef is not None and
                tdef.trigger_type == TRIGGER_USER_ACTION and
                self._checkTransitionGuard(tdef, ob, **kw)):
                return 1
        return 0

    def doActionFor(self, ob, action, comment='', **kw):
        '''
        Allows the user to request a workflow action.  This method
        must perform its own security checks.
        '''
        kw['comment'] = comment
        sdef = self._getWorkflowStateOf(ob)
        if sdef is None:
            raise WorkflowException, 'Object is in an undefined state'
        if action not in sdef.transitions:
            raise Unauthorized(action)
        tdef = self.transitions.get(action, None)
        if tdef is None or tdef.trigger_type != TRIGGER_USER_ACTION:
            raise WorkflowException, (
                'Transition %s is not triggered by a user action' % action)
        if not self._checkTransitionGuard(tdef, ob, **kw):
            raise Unauthorized(action)
        self._changeStateOf(ob, tdef, kw)

    def _checkTransitionGuard(self, t, ob, **kw):
        guard = t.guard
        if guard is None:
            return 1
        if guard.check(getSecurityManager(), self, ob, **kw):
            return 1
        return 0


DCWorkflowDefinition.isActionSupported = isActionSupported
DCWorkflowDefinition.doActionFor = doActionFor
DCWorkflowDefinition._checkTransitionGuard = _checkTransitionGuard
