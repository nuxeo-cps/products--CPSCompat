import ZTUtils
from ZPublisher.Converters import default_encoding as encoding
from ZTUtils import make_query as original_make_query

def make_query(*args, **kwargs):
    """provides unicode conversion.

    >>> from ZPublisher import Converters
    >>> Converters.default_encoding =  'utf-8'

    %3A is the URL escape fr colon
    >>> make_query(param=u'\xe9')
    'param%3Autf-8%3Austring=%C3%A9'
    >>> make_query({'param:utf-8:ustring' : u'\xe9'})
    'param%3Autf-8%3Austring=%C3%A9'
    """

    # See original docstring
    d = dict()
    for arg in args:
        d.update(arg)
    d.update(kwargs)

    uni = dict()
    # unicode string will migrate from d to uni (avoid side effects)
    for k, v in d.items():
        if isinstance(v, unicode):
            p = k.split(':', 1)[0]
            newk = '%s:%s:ustring' % (p, encoding)
            uni[newk] = v.encode(encoding, 'ignore')
            del d[k]

    return original_make_query(d, uni)

ZTUtils.make_query = make_query
