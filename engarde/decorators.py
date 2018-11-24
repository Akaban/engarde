# Hack module to retrieve easily decorator version of checks
# Need Python 3.7+

import engarde.checks as ck

def __getattr__(attr):
    return getattr(ck, attr).as_decorator
