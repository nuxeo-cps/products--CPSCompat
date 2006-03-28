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
"""Patch OFS.Application

Fix : transaction().abort() -> transaction.abort()

revision 41573

Can be remove after Zope-2.9.0. This is a temporay fix for zasync to
avoid having to put in production a Zope-2.9 trunk.

$Id: $
"""

from OFS.Application import *
import logging

logger = logging.getLogger("CPSCompat.PatchOFSApplication")

def install_product(app, product_dir, product_name, meta_types,
                    folder_permissions, raise_exc=0, log_exc=1):

    path_join=os.path.join
    isdir=os.path.isdir
    exists=os.path.exists
    global_dict=globals()
    silly=('__doc__',)

    if 1:  # Preserve indentation for diff :-)
        package_dir=path_join(product_dir, product_name)
        __traceback_info__=product_name
        if not isdir(package_dir): return
        if not exists(path_join(package_dir, '__init__.py')):
            if not exists(path_join(package_dir, '__init__.pyc')):
                if not exists(path_join(package_dir, '__init__.pyo')):
                    return
        try:
            product=__import__("Products.%s" % product_name,
                               global_dict, global_dict, silly)

            # Install items into the misc_ namespace, used by products
            # and the framework itself to store common static resources
            # like icon images.
            misc_=pgetattr(product, 'misc_', {})
            if misc_:
                if isinstance(misc_, dict):
                    misc_=Misc_(product_name, misc_)
                Application.misc_.__dict__[product_name]=misc_

            # Here we create a ProductContext object which contains
            # information about the product and provides an interface
            # for registering things like classes and help topics that
            # should be associated with that product. Products are
            # expected to implement a method named 'initialize' in
            # their __init__.py that takes the ProductContext as an
            # argument.
            productObject=App.Product.initializeProduct(
                product, product_name, package_dir, app)
            context=ProductContext(productObject, app, product)

            # Look for an 'initialize' method in the product. If it does
            # not exist, then this is an old product that has never been
            # updated. In that case, we will analyze the product and
            # build up enough information to do initialization manually.
            initmethod=pgetattr(product, 'initialize', None)
            if initmethod is not None:
                initmethod(context)

            # Support old-style product metadata. Older products may
            # define attributes to name their permissions, meta_types,
            # constructors, etc.
            permissions={}
            new_permissions={}
            if pgetattr(product, '__ac_permissions__', None) is not None:
                warn('__init__.py of %s has a long deprecated '
                     '\'__ac_permissions__\' attribute. '
                     '\'__ac_permissions__\' will be ignored by '
                     'install_product in Zope 2.10. Please use registerClass '
                     'instead.' % product.__name__,
                     DeprecationWarning)
            for p in pgetattr(product, '__ac_permissions__', ()):
                permission, names, default = (
                    tuple(p)+('Manager',))[:3]
                if names:
                    for name in names:
                        permissions[name]=permission
                elif not folder_permissions.has_key(permission):
                    new_permissions[permission]=()

            if pgetattr(product, 'meta_types', None) is not None:
                warn('__init__.py of %s has a long deprecated \'meta_types\' '
                     'attribute. \'meta_types\' will be ignored by '
                     'install_product in Zope 2.10. Please use registerClass '
                     'instead.' % product.__name__,
                     DeprecationWarning)
            for meta_type in pgetattr(product, 'meta_types', ()):
                # Modern product initialization via a ProductContext
                # adds 'product' and 'permission' keys to the meta_type
                # mapping. We have to add these here for old products.
                pname=permissions.get(meta_type['action'], None)
                if pname is not None:
                    meta_type['permission']=pname
                meta_type['product']=productObject.id
                meta_type['visibility'] = 'Global'
                meta_types.append(meta_type)

            if pgetattr(product, 'methods', None) is not None:
                warn('__init__.py of %s has a long deprecated \'methods\' '
                     'attribute. \'methods\' will be ignored by '
                     'install_product in Zope 2.10. Please use registerClass '
                     'instead.' % product.__name__,
                     DeprecationWarning)
            for name,method in pgetattr(
                product, 'methods', {}).items():
                if not hasattr(Folder.Folder, name):
                    setattr(Folder.Folder, name, method)
                    if name[-9:]!='__roles__': # not Just setting roles
                        if (permissions.has_key(name) and
                            not folder_permissions.has_key(
                                permissions[name])):
                            permission=permissions[name]
                            if new_permissions.has_key(permission):
                                new_permissions[permission].append(name)
                            else:
                                new_permissions[permission]=[name]

            if new_permissions:
                new_permissions=new_permissions.items()
                for permission, names in new_permissions:
                    folder_permissions[permission]=names
                new_permissions.sort()
                Folder.Folder.__ac_permissions__=tuple(
                    list(Folder.Folder.__ac_permissions__)+new_permissions)

            if not doInstall():
                transaction.abort()
            else:
                transaction.get().note('Installed product '+product_name)
                transaction.commit()

        except:
            if log_exc:
                logger.error('Couldn\'t install %s (error: %s)' % (product_name, 
                    sys.exc_info()))
            transaction.abort()
            if raise_exc:
                raise

import OFS.Application
OFS.Application.install_product = install_product
