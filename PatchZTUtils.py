import ZTUtils
from ZPublisher.Converters import default_encoding
from ZTUtils import make_query as original_make_query

def make_query(*args, **kwargs):
    """provides unicode conversion.

    >>> from ZPublisher import Converters
    >>> Converters.default_encoding =  'utf-8'
    >>> make_query(param=u'\xe9')
    'param=%C3%A9'
    """

    # See original docstring
    d = dict()
    for arg in args:
        d.update(arg)
    d.update(kwargs)

    for k, v in d.items():
        if isinstance(v, unicode):
            d[k] = v.encode(default_encoding, 'ignore')

    return original_make_query(d)

ZTUtils.make_query = make_query
