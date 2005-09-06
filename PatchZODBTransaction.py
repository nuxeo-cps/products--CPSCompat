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

Add before commit hooks support on ZODB <= 3.2
Add ZODB 3.5's new addBeforeCommitHook API

$Id$
"""

try:
    from ZODB.Transaction import Transaction

    # ZODB 3.2
    # No before commit hook support at all.

    def __init__(self, id=None):
        self._old__init__(id=id)
        self._before_commit = []
    Transaction._old__init__ = Transaction.__init__
    Transaction.__init__ = __init__

    def _init(self):
        self._old_init()
        self._before_commit = []
    Transaction._old_init = Transaction._init
    Transaction._init = _init

    def commit(self, subtransaction=None):
        if not subtransaction:
            self._callBeforeCommitHooks()
        self._old_commit(subtransaction)
    Transaction._old_commit = Transaction.commit
    Transaction.commit = commit

    def _callBeforeCommitHooks(self):
        # Call all hooks registered, allowing further registrations
        # during processing.  Note that calls to addBeforeCommitHook() may
        # add additional hooks while hooks are running, and iterating over a
        # growing list is well-defined in Python.
        for hook, args, kws in self._before_commit:
            hook(*args, **kws)
        self._before_commit = []
    Transaction._callBeforeCommitHooks = _callBeforeCommitHooks

    def getBeforeCommitHooks(self):
        return iter(self._before_commit)
    Transaction.getBeforeCommitHooks = getBeforeCommitHooks

except ImportError, e:

    if str(e) != 'No module named Transaction':
        raise

    # ZODB 3.4
    from transaction import Transaction

#
# API updated : ZODB >= 3.5
#

def addBeforeCommitHook(self, hook, args=(), kws=None):
    if kws is None:
        kws = {}
    self._before_commit.append((hook, tuple(args), kws))
Transaction.addBeforeCommitHook = addBeforeCommitHook


