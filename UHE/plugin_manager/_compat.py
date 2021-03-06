"""
    Look here for more information:
    https://github.com/mitsuhiko/flask/blob/master/flask/_compat.py
"""
import sys

PY2 = sys.version_info[0] == 2

if not PY2:  # pragma: no cover
    text_type = str
    string_types = (str,)
    integer_types = (int, )
    intern_method = sys.intern

    iterkeys = lambda d: iter(d.keys())
    itervalues = lambda d: iter(d.values())
    iteritems = lambda d: iter(d.items())

else:  # pragma: no cover
    text_type = unicode
    string_types = (str, unicode)
    integer_types = (int, long)
    intern_method = intern

    iterkeys = lambda d: d.iterkeys()
    itervalues = lambda d: d.itervalues()
    iteritems = lambda d: d.iteritems()