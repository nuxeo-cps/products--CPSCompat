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
"""CPSCompat

$Id$
"""

import logging
import sys

import PatchZODBTransaction
import PatchZTUtils

from OFS.ObjectManager import ObjectManager
from App.Management import Navigation
from Globals import DTMLFile

try:
    from Products import ExternalEditor
    # Monkey patch manage_main so that the urls are encoded properly
    ObjectManager.manage_main = DTMLFile('manage_main', globals())
except ImportError:
    if sys.exc_info()[2].tb_next is not None: raise

# #2404: Sets the whole ZMI in UTF-8
Navigation.manage_page_header = DTMLFile('manage_page_header', globals())

logging.getLogger('CPSCompat').debug(
    "Patching for Zope/CMF forward compatibility")
