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
"""PatchCMFCoreSkinnable

Fix skin data loss during transaction.
(http://www.zope.org/Collectors/CMF/198)

Related to PatchCMFCorePortalObect

WARNING this patch is not compatible with Speedpack !

Correct __of__ to not catch ConflictError.

$Id$
"""

from zLOG import LOG, INFO, DEBUG
from thread import get_ident
from Acquisition import aq_base
from Acquisition import ImplicitAcquisitionWrapper
from AccessControl import ClassSecurityInfo
from Globals import InitializeClass
from ZODB.POSException import ConflictError

from Products.CMFCore.Skinnable import SkinnableObjectManager


if True: # Fix ConflictError in __of__

    security = ClassSecurityInfo()

    def __of__(self, parent):
        '''
        Sneakily sets up the portal skin then returns the wrapper
        that Acquisition.Implicit.__of__() would return.
        '''
        w_self = ImplicitAcquisitionWrapper(self, parent)
        try:
            w_self.setupCurrentSkin()
        except ConflictError:
            raise
        except:
            # This shouldn't happen, even if the requested skin
            # does not exist.
            import sys
            from zLOG import LOG, ERROR
            LOG('CMFCore', ERROR, 'Unable to setupCurrentSkin()',
                error=sys.exc_info())
        return w_self

    SkinnableObjectManager.__of__ = __of__


    SkinnableObjectManager.security = security
    InitializeClass(SkinnableObjectManager)



needs_new_skindata = not hasattr(SkinnableObjectManager, 'clearCurrentSkin')

if needs_new_skindata:

    from Products.CMFCore.Skinnable import superGetAttr

    _marker = []  # Create a new marker object.
    SKINDATA = {} # mapping thread-id -> (skinobj, ignore, resolve)

    class SkinDataCleanup:
        """Cleanup at the end of the request."""
        def __init__(self, tid):
            self.tid = tid
        def __del__(self):
            tid = self.tid
            if SKINDATA.has_key(tid):
                del SKINDATA[tid]


    security = ClassSecurityInfo()


    def ___getattr__(self, name):
        '''
        Looks for the name in an object with wrappers that only reach
        up to the root skins folder.

        This should be fast, flexible, and predictable.
        '''
        if not name.startswith('_') and not name.startswith('aq_'):
            sd = SKINDATA.get(get_ident())
            if sd is not None:
                ob, ignore, resolve = sd
                if not ignore.has_key(name):
                    if resolve.has_key(name):
                        return resolve[name]
                    subob = getattr(ob, name, _marker)
                    if subob is not _marker:
                        # Return it in context of self, forgetting
                        # its location and acting as if it were located
                        # in self.
                        retval = aq_base(subob)
                        resolve[name] = retval
                        return retval
                    else:
                        ignore[name] = 1
        if superGetAttr is None:
            raise AttributeError, name
        return superGetAttr(self, name)

    SkinnableObjectManager.__getattr__ = ___getattr__


    def changeSkin(self, skinname):
        '''Change the current skin.

        Can be called manually, allowing the user to change
        skins in the middle of a request.
        '''
        skinobj = self.getSkin(skinname)
        if skinobj is not None:
            tid = get_ident()
            SKINDATA[tid] = (skinobj, {}, {})
            REQUEST = getattr(self, 'REQUEST', None)
            if REQUEST is not None:
                REQUEST._hold(SkinDataCleanup(tid))

    SkinnableObjectManager.changeSkin = changeSkin


    security.declarePublic('clearCurrentSkin')
    def clearCurrentSkin(self):
        """Clear the current skin."""
        tid = get_ident()
        if SKINDATA.has_key(tid):
            del SKINDATA[tid]

    SkinnableObjectManager.clearCurrentSkin = clearCurrentSkin


    def setupCurrentSkin(self, REQUEST=None):
        '''
        Sets up skindata so that __getattr__ can find it.

        Can NOT be called manually to change skins in the middle of a
        request! Use changeSkin for that.
        '''
        if REQUEST is None:
            REQUEST = getattr(self, 'REQUEST', None)
        if REQUEST is None:
            # self is not fully wrapped at the moment.  Don't
            # change anything.
            return
        if SKINDATA.has_key(get_ident()):
            # Already set up for this request.
            return
        skinname = self.getSkinNameFromRequest(REQUEST)
        self.changeSkin(skinname)

    SkinnableObjectManager.setupCurrentSkin = setupCurrentSkin


    def _checkId(self, id, allow_dup=0):
        '''
        Override of ObjectManager._checkId().

        Allows the user to create objects with IDs that match the ID of
        a skin object.
        '''
        superCheckId = SkinnableObjectManager.inheritedAttribute('_checkId')
        if not allow_dup:
            # Temporarily disable skindata.
            # Note that this depends heavily on Zope's current thread
            # behavior.
            tid = get_ident()
            sd = SKINDATA.get(tid)
            if sd is not None:
                del SKINDATA[tid]
            try:
                base = getattr(self,  'aq_base', self)
                if not hasattr(base, id):
                    # Cause _checkId to not check for duplication.
                    return superCheckId(self, id, allow_dup=1)
            finally:
                if sd is not None:
                    SKINDATA[tid] = sd
        return superCheckId(self, id, allow_dup)

    SkinnableObjectManager._checkId = _checkId


    SkinnableObjectManager.security = security
    InitializeClass(SkinnableObjectManager)
