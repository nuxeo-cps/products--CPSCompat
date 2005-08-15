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

Add ZODB 3.5's ordered before commit hook into ZODB 3.2

$Id$
"""

import bisect

try:
    from ZODB.Transaction import Transaction
    # ZODB 3.2
    # No before commit hook support at all.

    def __init__(self, id=None):
        self._old__init__(id=id)
        self._before_commit = []
        self._before_commit_index = 0
    Transaction._old__init__ = Transaction.__init__
    Transaction.__init__ = __init__

    def _init(self):
        self._old_init()
        self._before_commit = []
        self._before_commit_index = 0
    Transaction._old_init = Transaction._init
    Transaction._init = _init

    def commit(self, subtransaction=None):
        if not subtransaction:
            self._callBeforeCommitHooks()
        self._old_commit(subtransaction)
    Transaction._old_commit = Transaction.commit
    Transaction.commit = commit

except ImportError, e:
    if str(e) != 'No module named Transaction': raise

    # ZODB >= 3.4
    from transaction import Transaction

    def __init__(self, synchronizers=None, manager=None):
        self._old__init__(synchronizers, manager)
        self._before_commit_index = 0
    Transaction._old__init__ = Transaction.__init__
    Transaction.__init__ = __init__

#
# Patch for ordering support
#

def getBeforeCommitHooks(self):
    # Don't return the hook order and index values because of
    # backward compatibility, and because they're internal details.
    return iter([x[2:] for x in self._before_commit])
Transaction.getBeforeCommitHooks = getBeforeCommitHooks

def addBeforeCommitHook(self, hook, args=(), kws=None, order=0):
    if not isinstance(order, int):
        raise ValueError("An integer value is required "
                         "for the order argument")
    if kws is None:
        kws = {}
    bisect.insort(self._before_commit, (order, self._before_commit_index,
                                        hook, tuple(args), kws))
    self._before_commit_index += 1
Transaction.addBeforeCommitHook = addBeforeCommitHook

def beforeCommitHook(self, hook, *args, **kws):
    from ZODB.utils import deprecated37
    
    deprecated37("Use addBeforeCommitHook instead of beforeCommitHook.")
    # Default order is zero.
    self.addBeforeCommitHook(hook, args, kws, order=0)
Transaction.beforeCommitHook = beforeCommitHook

def _callBeforeCommitHooks(self):
    # Call all hooks registered, allowing further registrations
    # during processing.
    while self._before_commit:
        order, index, hook, args, kws = self._before_commit.pop(0)
        hook(*args, **kws)
    self._before_commit_index = 0
Transaction._callBeforeCommitHooks = _callBeforeCommitHooks
