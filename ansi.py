"""
Quick-and-dirty tools for managing ANSI colors,
including converting colored terminal text to HTML
"""
import typing
import re
from enum import Enum


ANSI_CLEAR_SCREEN="{}[2J{}[;H".format(chr(27),chr(27))
class ANSI_COLORS(Enum):
    """
    ANSI terminal color codes
    https://en.wikipedia.org/wiki/ANSI_escape_code#Colors
    """
    ANSI_WHITE=       "\033[1;37m"
    ANSI_YELLOW=      "\033[1;33m"
    ANSI_GREEN=       "\033[1;32m"
    ANSI_BLUE=        "\033[1;34m"
    ANSI_CYAN=        "\033[1;36m"
    ANSI_RED=         "\033[1;31m"
    ANSI_MAGENTA=     "\033[1;35m"
    ANSI_BLACK=       "\033[1;30m" # aka, dark gray
    ANSI_DARK_WHITE=  "\033[0;37m" # aka, light gray
    ANSI_DARK_YELLOW= "\033[0;33m"
    ANSI_DARK_GREEN=  "\033[0;32m"
    ANSI_DARK_BLUE=   "\033[0;34m"
    ANSI_DARK_CYAN=   "\033[0;36m"
    ANSI_DARK_RED=    "\033[0;31m"
    ANSI_DARK_MAGENTA="\033[0;35m"
    ANSI_DARK_BLACK=  "\033[0;30m" # aka, actual black
    ANSI_OFF=         "\033[0;0m"

ansi2CSS={
    30:'color:black',
    31:'color:red',
    32:'color:green',
    33:'color:yellow',
    34:'color:blue',
    35:'color:purple',
    36:'color:cyan',
    37:'color:white',
    40:'background-color:black',
    41:'background-color:red',
    42:'background-color:green',
    43:'background-color:yellow',
    44:'background-color:blue',
    45:'background-color:purple',
    46:'background-color:cyan',
    47:'background-color:white'}

ansiEscapeCodeFinderRe=re.compile(r'\x1b\[(.*?)m')
def ansiColorToHtml(ansiColoredString:str)->str:
    """
    take a string with ansi color codes and return an html string

    NOTE: this html is JUST THE COLORS
    not any curses stuff, fixed-width font, or newline handling
    """
    # make this a list so it gets shared with the child function
    spancount:typing.List[int]=[0]
    currentFG:typing.List[typing.Optional[str]]=[None]
    currentBG:typing.List[typing.Optional[str]]=[None]
    lastWasFG:typing.List[bool]=[False]
    def replaceAnsi(match)->str:
        """
        replace an ansi color escape code with a span
        """
        ret=[]
        #print(f'Detected ANSI codes {match.group(1)}')
        for code in match.group(1).split(';'):
            code=int(code)
            #print(f'Detected ANSI code {code}')
            if code==0:
                if spancount[0]>0:
                    ret.append('</span>'*spancount[0])
                    spancount[0]=0
                currentFG[0]=None
                currentBG[0]=None
                lastWasFG[0]=False
                continue
            try:
                style=ansi2CSS[code]
            except IndexError as e:
                raise IndexError(f'unknown ANSI escape code {code}') from e
            span=f'<span style="{style}">'
            here=len(ret)
            ret.append(span) # assume the basics, then modify as needed
            isFG=(style[0]=='c')
            if isFG:
                if currentFG[0] is not None:
                    # if there is a current foreground color,
                    # we need to close it first!
                    if lastWasFG[0]:
                        # current span is the foreground color span,
                        # so close it
                        ret.insert(here,'</span>')
                    elif currentBG[0] is not None:
                        # there is a background inside the foreground,
                        # so we have to close it, then reopen it after
                        ret.insert(here,'</span></span>')
                        ret.append(currentBG[0])
                else:
                    spancount[0]+=1
                lastWasFG[0]=True
                currentFG[0]=span
            else:
                if currentBG[0] is not None:
                    # if there is a current background color,
                    # we need to close it first!
                    if currentBG[0]:
                        # current span is the backgruond color span,
                        # so close it
                        ret.insert(here,'</span>')
                    elif currentFG[0] is not None:
                        # there is a foreground inside the background,
                        # so we have to close it, then reopen it after
                        ret.insert(here,'</span></span>')
                        ret.append(currentFG[0])
                else:
                    spancount[0]+=1
                lastWasFG[0]=False
                currentBG[0]=span
        return ''.join(ret)
    result=re.sub(ansiEscapeCodeFinderRe,replaceAnsi,ansiColoredString)
    return result
