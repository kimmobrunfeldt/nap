import sys

_PY33 = sys.version_info >= (3, 3)

if not _PY33:
    from backports.functools_lru_cache import lru_cache
else:
    from functools import lru_cache

_PY3 = sys.version_info >= (3, 0)

# For Python 3 compatibility
if _PY3:
    from urllib.parse import urljoin
else:
    from urlparse import urljoin