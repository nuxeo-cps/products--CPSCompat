=========
CPSCompat
=========

:Authors: - Florent Guillaume <fg@nuxeo.com>
          - Julien Anguenot <ja@nuxeo.com>
          - Marc-Aur�le Darche <madarche@nuxeo.com>

This product is a forward-compatibility module for Zope and CMF. It
changes Zope and CMF code by monkey patching to make available features
that are checked in Zope or CMF sources, but not yet used in production
everywhere.

It has to work in the presence of various versions of Zope and CMF.

Other products that want to monkey-patch Zope or CMF need to make sure
they import CPSCompat first.


Features
========

- External Editor fix : creation of "CPS Flexible Type Information"
  failed if the javascript was disabled

- Add ZODB 3.7 after commit hook support

- Add modified version of the "postonly" Hotfix_20070319 for the CPSUserFolder
  product

- Add a Graph tab in workflows for DCWorkflowGraph.


License
=======

The code in this product is derived from Zope and CMF, and is thus under
the ZPL 2.1 license.



.. Local Variables:
.. mode: rst
.. End:
.. vim: set filetype=rst:
