"""mod1
!INCLUDE Class
!INCLUDE func
!INCLUDE .submod.submod1
"""


class Class(object):
    """Class
    !INCLUDE method1
    """
    def method1(self):
        """method1
        !INCLUDE .method2
        """
        pass

    def method2(self):
        """method2
        !INCLUDE ...mod2
        """
        pass

    def method3(self):
        """method3"""


def func():
    """func
    !INCLUDE .Class.method3
    """
    pass
