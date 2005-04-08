CPSCompat
=========

This product is a forward-compatibility module for Zope and CMF. It
changes Zope and CMF code by monkey patching to make available features
that are checked in Zope or CMF sources, but not yet used in production
everywhere.

It has to work in the presence of various versions of Zope and CMF.

Other products that want to monkey-patch Zope or CMF need to make sure
they import CPSCompat first.

Features
--------

- Fix creator computation or upgrade.
  (http://zope.org/Collectors/CMF/300)

- Prevent skin data loss during transaction.
  (http://www.zope.org/Collectors/CMF/198)

- Add ZODB 3.4 beforeCommitHook in transaction.

License
-------

The code in this product is derived from Zope and CMF, and is thus under
the ZPL 2.1 license.
