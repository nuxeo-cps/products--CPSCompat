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
"""PatchCMFDefaultDublinCore

Fix creator computation or upgrade. (http://zope.org/Collectors/CMF/300)

$Id$
"""

from Products.CMFDefault.DublinCore import DefaultDublinCoreImpl

is_cmf_1_5 = hasattr(DefaultDublinCoreImpl, 'listCreators')

if is_cmf_1_5:

    # From CMF 1.5.0+
    def listCreators(self):
        """ List Dublin Core Creator elements - resource authors.
        """
        if not hasattr(aq_base(self), 'creators'):
            # for content created with CMF versions before 1.5
            owner_tuple = self.getOwnerTuple()
            if owner_tuple:
                self.creators = (owner_tuple[1],)
            else:
                self.creators = ()
        return self.creators
    DefaultDublinCoreImpl.listCreators = listCreators

else:

    # From CMF 1.4.8+
    def Creator(self):
        "Dublin Core element - resource creator"
        owner_tuple = self.getOwnerTuple()
        if owner_tuple:
            return owner_tuple[1]
        return 'No owner'
    DefaultDublinCoreImpl.Creator = Creator
