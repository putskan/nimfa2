
"""
#########################
Utils (``utils.utils``)
#########################
"""

class MFError(Exception):

    """
    Generic Python exception derived object raised by nimfa2 library.
    
    This is general purpose exception class, derived from Python common base
    class for all non-exit exceptions. It is programmatically raised in nimfa2
    library functions when:
        
        #. linear algebra related condition prevents further correct execution
        of a function;
        #. user input parameters are ambiguous or not in correct format.
    """

    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return repr(self.msg)
