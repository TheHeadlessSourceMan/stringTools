r"""
Handle quoted/encoded strings eg
    "Momma says \"hello\"\n"
"""
import sys
import re


QUOTE_REGEX_STR=r"""r?("{3}|"|')(?P<contents>(?:[^\1\\]|\\.)*)\1"""
QUOTE_REGEX=re.compile('.?'+QUOTE_REGEX_STR)


def test():
    """
    unit test for proper handling of quote strings
    """
    tests=[
        'x"abc"y',
        "x'abc'y",
        'xr"""abc"""y',
        'x"ab\\"c"y',
        "x'ab\\'c'y",
        ]
    for t in tests:
        print(t,QUOTE_REGEX.match(t).group("contents"))


if __name__=='__main__':
    for i,a in enumerate(sys.argv):
        print("%d) %s"%(i,a))
