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
"""Patch Publisher ConflictError logging.

Available starting in Zope 2.9.

$Id$
"""
import sys
from types import StringType, ListType
from Acquisition import aq_acquire
import AccessControl.User
from zLOG import LOG, ERROR, BLATHER
from ZODB.POSException import ConflictError
import ZPublisher

import Zope2.App.startup
from Zope2.App.startup import RequestContainer
from Zope2.App.startup import conflict_errors

def zpublisher_exception_hook(published, REQUEST, t, v, traceback):
    try:
        if isinstance(t, StringType):
            if t.lower() in ('unauthorized', 'redirect'):
                raise
        else:
            if t is SystemExit:
                raise
            if issubclass(t, ConflictError):
                global conflict_errors
                conflict_errors += 1
                method_name = REQUEST.get('PATH_INFO', '')
                LOG('ZODB', BLATHER, "%s at %s: %s"
                    " (%s conflicts since startup at %s)"
                    % (v.__class__.__name__, method_name, v,
                       conflict_errors, Zope2.App.startup.startup_time))
                raise ZPublisher.Retry(t, v, traceback)
            if t is ZPublisher.Retry:
                # An exception that can't be retried anymore
                # Retrieve the original exception
                try: v.reraise()
                except: t, v, traceback = sys.exc_info()
                # Then fall through to display the error to the user

        try:
            log = aq_acquire(published, '__error_log__', containment=1)
        except AttributeError:
            error_log_url = ''
        else:
            error_log_url = log.raising((t, v, traceback))

        if (getattr(REQUEST.get('RESPONSE', None), '_error_format', '')
            !='text/html'):
            raise t, v, traceback

        app = Zope2.App.startup.app
        if (published is None or published is app or
            type(published) is ListType):
            # At least get the top-level object
            published=app.__bobo_traverse__(REQUEST).__of__(
                RequestContainer(REQUEST))

        published=getattr(published, 'im_self', published)
        while 1:
            f=getattr(published, 'raise_standardErrorMessage', None)
            if f is None:
                published=getattr(published, 'aq_parent', None)
                if published is None:
                    raise t, v, traceback
            else:
                break

        client=published
        while 1:
            if getattr(client, 'standard_error_message', None) is not None:
                break
            client=getattr(client, 'aq_parent', None)
            if client is None:
                raise t, v, traceback

        if REQUEST.get('AUTHENTICATED_USER', None) is None:
            REQUEST['AUTHENTICATED_USER']=AccessControl.User.nobody

        try:
            f(client, REQUEST, t, v, traceback, error_log_url=error_log_url)
        except TypeError:
            # Pre 2.6 call signature
            f(client, REQUEST, t, v, traceback)

    finally:
        traceback=None

Zope2.App.startup.zpublisher_exception_hook = zpublisher_exception_hook

# This monkey-patched is done before Zope's startup() so we
# don't have to tweak get_module_info's modules.
