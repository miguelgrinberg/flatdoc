"""mod5
!INCLUDE foo
"""


def foo():
    """foo
    !INCLUDE .bar.
    """
    pass


def bar():
    """bar"""
    pass
