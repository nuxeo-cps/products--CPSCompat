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
"""Patch CMFSetup.utils for code available in CMF > 1.5.4.

 - Allow export of old list properties.

 - Correct import of empty attributes when an encoding is specified.
"""

from Products.CMFSetup.utils import ExportConfiguratorBase
from Products.CMFSetup.utils import ImportConfiguratorBase


if True: # Keep indentation

    def _extractNode(self, node):

        nodes_map = self._getImportMapping()
        if node.nodeName not in nodes_map:
            nodes_map = self._getSharedImportMapping()
            if node.nodeName not in nodes_map:
                raise ValueError('Unknown node: %s' % node.nodeName)
        node_map = nodes_map[node.nodeName]
        info = {}

        for name, val in node.attributes.items():
            key = node_map[name].get( KEY, str(name) )
            if self._encoding is not None:
                val = val.encode(self._encoding)
            info[key] = val

        for child in node.childNodes:
            name = child.nodeName

            if name == '#comment':
                continue

            if not name == '#text':
                key = node_map[name].get(KEY, str(name) )
                info[key] = info.setdefault( key, () ) + (
                                                    self._extractNode(child),)

            elif '#text' in node_map:
                key = node_map['#text'].get(KEY, 'value')
                val = child.nodeValue.lstrip()
                if self._encoding is not None:
                    val = val.encode(self._encoding)
                info[key] = info.setdefault(key, '') + val

        for k, v in node_map.items():
            key = v.get(KEY, k)

            if DEFAULT in v and not key in info:
                if isinstance( v[DEFAULT], basestring ):
                    info[key] = v[DEFAULT] % info
                else:
                    info[key] = v[DEFAULT]

            elif CONVERTER in v and key in info:
                info[key] = v[CONVERTER]( info[key] )

            if key is None:
                info = info[key]

        return info

    ImportConfiguratorBase._extractNode = _extractNode


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
