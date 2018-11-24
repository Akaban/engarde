# Hack module to retrieve easily decorator version of checks
# Need Python 3.7+

import engarde.checks as ck
from engarde import generic

def __getattr__(attr):
    """Proxy for getting decorator version of check
    """
    return generic.as_decorator(getattr(ck, attr))
