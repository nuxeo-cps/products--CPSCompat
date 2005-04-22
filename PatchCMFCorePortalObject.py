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
"""PatchCMFCorePortalObject

Fix skin data loss during transaction.
(http://www.zope.org/Collectors/CMF/198)

Related to PatchCMFCoreSkinnable

$Id$
"""

from PatchCMFCoreSkinnable import needs_new_skindata

from Products.CMFCore.Skinnable import SkinnableObjectManager
from Products.CMFCore.PortalObject import PortalObjectBase


if True:

    PortalObjectBase.__of__ = SkinnableObjectManager.__of__


if needs_new_skindata:

    PortalObjectBase.__getattr__ = SkinnableObjectManager.__getattr__
    PortalObjectBase._checkId = SkinnableObjectManager._checkId
