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
"""Patch CMFSetup.utils to allow export of old list properties.

Available in CMF > 1.5.4.
"""

from Products.CMFSetup.utils import ExportConfiguratorBase

if True: # Keep indentation

    def _extractProperty(self, obj, prop_map):

        prop_id = prop_map['id']
        prop = obj.getProperty(prop_id)

        if isinstance(prop, tuple):
            prop_value = ''
            prop_elements = prop
        elif isinstance(prop, list):
            # Backward compat for old instances that stored
            # properties as list.
            prop_value = ''
            prop_elements = tuple(prop)
        else:
            prop_value = prop
            prop_elements = ()

        if 'd' in prop_map.get('mode', 'wd') and not prop_id == 'title':
            type = prop_map.get('type', 'string')
            select_variable = prop_map.get('select_variable', None)
        else:
            type = None
            select_variable = None

        return { 'id': prop_id,
                 'value': prop_value,
                 'elements': prop_elements,
                 'type': type,
                 'select_variable': select_variable }

    ExportConfiguratorBase._extractProperty = _extractProperty
