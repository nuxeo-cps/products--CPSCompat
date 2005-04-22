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

Add ZODB 3.4's before commit hook into ZODB 3.2

$Id$
"""

try:
    from ZODB.Transaction import Transaction
    # ZODB 3.2
    has_before_commit_hook = hasattr(Transaction, 'beforeCommitHook')
except ImportError, e:
    if str(e) != 'No module named Transaction': raise
    # ZODB 3.4
    has_before_commit_hook = True


if not has_before_commit_hook:

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

    def beforeCommitHook(self, hook, *args, **kws):
        self._before_commit.append((hook, args, kws))
    Transaction.beforeCommitHook = beforeCommitHook

    def _callBeforeCommitHooks(self):
        # Call all hooks registered, allowing further registrations
        # during processing.
        while self._before_commit:
            hook, args, kws = self._before_commit.pop(0)
            hook(*args, **kws)
    Transaction._callBeforeCommitHooks = _callBeforeCommitHooks

    def commit(self, subtransaction=None):
        if not subtransaction:
            self._callBeforeCommitHooks()
        self._old_commit(subtransaction)
    Transaction._old_commit = Transaction.commit
    Transaction.commit = commit
