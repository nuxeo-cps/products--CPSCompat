#############################################################################
#
# Copyright (c) 2007 Zope Corporation and Contributors. All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE
#
##############################################################################

"""Modified version of the Hotfix_20070319 for the CPSUserFolder product.

Protect security methods against GET requests.

Remove this fix when CPS followed method are protected in Zope

$Id$
"""
from AccessControl.requestmethod import postonly

# Zope not protected on Zope 2.9.7
from AccessControl.Owned import Owned
Owned.manage_takeOwnership = postonly(Owned.manage_takeOwnership)
Owned.manage_changeOwnershipType = postonly(Owned.manage_changeOwnershipType)
