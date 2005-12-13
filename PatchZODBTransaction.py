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
"""PatchZODBTransaction

Add ZODB 3.5's new addBeforeCommitHook API

$Id$
"""

from transaction import Transaction

#
# API updated : ZODB >= 3.5
#

def addBeforeCommitHook(self, hook, args=(), kws=None):
    if kws is None:
        kws = {}
    self._before_commit.append((hook, tuple(args), kws))
Transaction.addBeforeCommitHook = addBeforeCommitHook


