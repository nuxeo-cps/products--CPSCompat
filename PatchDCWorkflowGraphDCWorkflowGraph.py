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
"""PatchDCWorkflowGraphDCWorkflowGraph

Patch needed to get the "Graph" tab in a CPS worklow using DCWorkflowGraph

$Id$
"""

import os
from Products.PageTemplates.PageTemplateFile import PageTemplateFile
from Products.DCWorkflowGraph.DCWorkflowGraph import getGraph
from Products.CPSWorkflow.workflow import WorkflowDefinition

path = os.path.join(INSTANCE_HOME,
                    'Products',
                    'DCWorkflowGraph',
                    'www',
                    'manage_workflowGraph')
manage_workflowGraph = PageTemplateFile(path, globals())
manage_workflowGraph.__name__ = 'manage_workflowGraph'
manage_workflowGraph._need__name__ = 0

WorkflowDefinition.getGraph=getGraph
WorkflowDefinition.manage_workflowGraph=manage_workflowGraph
WorkflowDefinition.manage_options=tuple(WorkflowDefinition.manage_options)+(
    {'label': 'Graph', 'action': 'manage_workflowGraph'},)
