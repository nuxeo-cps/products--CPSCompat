##############################################################################
#
# Copyright (c) 2006 Zope Corporation and Contributors. All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
""" Fix for CMFCore.FSPythonScript

Fixed in CMF 1.6 branch : revision 41636:

CMFCore.FSPythonScript: FSPythonScripts forgot to add __file__ to
the script globals. This broke warnings.warn() when a stacklevel
argument pointing into the script was passed (2).
  
$Id: PatchZODBTransaction.py 31353 2006-01-06 00:05:16Z janguenot $
"""

import new

from AccessControl import getSecurityManager

from Products.CMFCore.FSPythonScript import FSPythonScript
from Products.CMFCore.FSPythonScript import FSPythonScriptTracebackSupplement

if True:
    def _exec(self, bound_names, args, kw):
        """Call a Python Script

        Calling a Python Script is an actual function invocation.
        """
        # do caching
        keyset = None
        if self.ZCacheable_isCachingEnabled():
            # Prepare a cache key.
            keyset = kw.copy()
            asgns = self.getBindingAssignments()
            name_context = asgns.getAssignedName('name_context', None)
            if name_context:
                keyset[name_context] = self.aq_parent.getPhysicalPath()
            name_subpath = asgns.getAssignedName('name_subpath', None)
            if name_subpath:
                keyset[name_subpath] = self._getTraverseSubpath()
            # Note: perhaps we should cache based on name_ns also.
            keyset['*'] = args
            result = self.ZCacheable_get(keywords=keyset, default=_marker)
            if result is not _marker:
                # Got a cached value.
                return result

        # Prepare the function.
        f = self._v_f
        if f is None:
            # The script has errors.
            __traceback_supplement__ = (
                FSPythonScriptTracebackSupplement, self, 0)
            raise RuntimeError, '%s has errors.' % self._filepath

        # Updating func_globals directly is not thread safe here.
        # In normal PythonScripts, every thread has its own
        # copy of the function.  But in FSPythonScripts
        # there is only one copy.  So here's another way.
        new_globals = f.func_globals.copy()
        new_globals['__traceback_supplement__'] = (
            FSPythonScriptTracebackSupplement, self)
        new_globals['__file__'] = self._filepath
        if bound_names:
            new_globals.update(bound_names)
        if f.func_defaults:
            f = new.function(f.func_code, new_globals, f.func_name,
                             f.func_defaults)
        else:
            f = new.function(f.func_code, new_globals, f.func_name)

        # Execute the function in a new security context.
        security=getSecurityManager()
        security.addContext(self)
        try:
            result = f(*args, **kw)
            if keyset is not None:
                # Store the result in the cache.
                self.ZCacheable_set(result, keywords=keyset)
            return result
        finally:
            security.removeContext(self)

    FSPythonScript._exec = _exec
