# The idea is a system that, when given a name, matches the best
# possible item
# 
# Consider, they said "do the best thing"
# and our options are ["someOtherThing","doTheBest","doTheBestThing","do_the_best_thing"]
# the goal is to choose the most appropriate.
#
# Supports:
#   word separators like "-","_"," "
#   camelCase
#   stop words (eg "do the thing" can resolve to "doThing")
#   zero padded numbers "do thing 01" => "doThing1"
#   textual numbers "do thing one" => "doThing1" or "do thing 1" => "doThingOne"
#   always tries to eat the largest possible match "do the best thing", given ["doTheBest","doTheBestThing"] => "doTheBestThing"
#   prefers caps that match, but will accept those that don't
#   also supports variable stacks, so for programming uses it is easy to manage context
import re
import typing

class NameMatch:
    """
    Indicates a name has matched, with a given
    reliablility rank.
    """
    def __init__(self,match:str,rank:float):
        self.match:str=match
        self.rank:float=rank
        self.tapeEndIdx:int=0 # where the match ends in the tape
    
    def __cmp__(self,other:'NameMatch')->float:
        """
        You can compare name matches by rank for sorting and whatnot
        """
        return self.rank-other.rank
    def __lt__(self,other:'NameMatch')->bool:
        """
        You can compare name matches by rank for sorting and whatnot
        """
        return self.rank<other.rank

    def __str__(self):
        return self.match

    def __repr__(self):
        return f'(rank={self.rank}) {self.match}'

numbers=['zero','one','two','three','four','five','six','seven','eight','nine','ten']
numeridecode_re=re.compile(r"""(?P<textual>"""+('|'.join(numbers))+r""")|(?:0*(?P<numerical>[1-9][0-9]*))""",re.IGNORECASE)
def numeridecode(s:str)->str:
    """
    decode numbers in a string to common digits
    numbers can be:
        single digit in text (case insensitve)
            eg "Seven"
        zero-padded number
            eg "007"
        in this case, bot examples return "7"
    """
    def subfn(m:typing.Match)->str:
        if m.group('textual'):
            return str(numbers.index(m.group('textual').lower()))
        return m.group('numerical')
    return numeridecode_re.sub(subfn,s)

def stopwordsremove(s:str)->str:
    """
    TODO: this could be better by using
        1) my variable name class
        2) NLTK stopwords smarts
    This should still be adequate for most things as-is, though
    """
    stopwords=['and','or','to','of','from','the','a','an','in','for']
    ret=[]
    for w in s.split():
        if w.lower() not in stopwords:
            ret.append(w)
    return ' '.join(ret)

class ForgivingName:
    """
    A text name that we can determine alternate meanings
    """

    breakingChars=(' ','-','_')

    def __init__(self,name):
        self.name=name
        self._squishy_precalc=None

    @property
    def _squishy(self)->str:
        """
        Returns a squishier string with
            1) numbers converted numeridecode()
            2) stop words removed with stopwordsremove()
        """
        if self._squishy_precalc is None:
            self._squishy_precalc=stopwordsremove(numeridecode(self.name))
        return self._squishy_precalc

    def match(self,tape:str,idx:int=0)->typing.Optional[NameMatch]:
        """
        get a match or None

        TODO: the match end index is not implemented
        """
        # first try the simple case
        if tape.startswith(self.name):
            return NameMatch(self.name,len(self.name))
        # utility function we can call to check multiple things
        def match_util(name:str,tape:str,idx:int=0)->float:
            tapeIdx:int=idx
            nameIdx:int=0
            rank:float=0
            while tapeIdx<len(tape) and nameIdx<len(name):
                if tape[tapeIdx]==name[nameIdx]:
                    # case sensitive matches are worth a full point
                    rank+=1
                    tapeIdx+=1
                    nameIdx+=1
                elif tape[tapeIdx].lower()==name[nameIdx].lower():
                    # case-insensitive matches are worth half a point
                    rank+=0.5
                    tapeIdx+=1
                    nameIdx+=1
                elif tape[tapeIdx] in self.breakingChars or name[nameIdx]in self.breakingChars:
                    # breaking characters are different
                    # so don't add to the rank, but skip over them and keep going
                    if tape[tapeIdx] in self.breakingChars and name[nameIdx]in self.breakingChars:
                        # mismatched breaking chars are still breaking chars, so worth a little something
                        rank+=0.5
                    else:
                        rank-=0.5
                    while tape[tapeIdx] in self.breakingChars:
                        tapeIdx+=1
                    while name[nameIdx] in self.breakingChars:
                        nameIdx+=1
                else:
                    # character simply did not match!
                    return 0
            # reached the end
            if nameIdx<len(name):
                # still unmached characters in the name!
                return 0
            # add a little nudge for being closer to the same size
            if rank!=0:
                rank-=abs((tapeIdx-idx)-nameIdx)/100.0
            return rank
        # try for a straight-up match
        rank:float=match_util(self.name,tape,idx)
        if rank!=0:
            return NameMatch(self.name,rank)
        # see if decoding any numbers and removing stopwords in the text helps
        desiredChars=max(len(self.name),len(self._squishy))+10
        subtape=tape[idx:min(len(tape)-idx,desiredChars)]
        subtape=stopwordsremove(numeridecode(subtape))
        rank=match_util(self._squishy,subtape)
        if rank!=0:
            return NameMatch(self.name,rank)
        return None


class ForgivingNamesContext:
    """
    A stack frame for a name context.
    (Having more than one is handy for variable name contexts)
    """

    def __init__(self):
        self._ctx:typing.Dict[str,ForgivingName]={}

    def clear(self):
        """
        Clear out all names in context
        """
        self._ctx={}

    def add(self,name:str)->None:
        """
        Add a name to the current context
        """
        self._ctx[name]=ForgivingName(name)

    def remove(self,name:str):
        """
        Remove a name from the current context
        """
        del self._ctx[name]

    def matches(self,tape:str,idx:int=0,sorted:bool=True
        )->typing.List[NameMatch]:
        """
        All of the matches possible in the tape, with a rank

        Unless otherwise turned off, will return in sorted order,
        with the most likely candidate first in the list.
        """
        ret=[]
        for forgiving in self._ctx.values():
            m=forgiving.match(tape,idx)
            if m is not None:
                ret.append(m)
        if ret and sorted:
            ret.sort(reverse=True)
        return ret

    def bestMatch(self,tape:str,idx:int=0)->typing.Optional[NameMatch]:
        """
        Single best match for a given name
        (can still be None, if nothing matched)

        This is probably more efficient than matches[0]
        """
        m=self.matches(tape,idx)
        if not m:
            return None
        return m[0]


class ForgivingNames:
    """
    The idea is a system that, when given a name, matches the best
    possible item

    Consider, they said "do the best thing"
    and our options are ["someOtherThing","doTheBest","doTheBestThing","do_the_best_thing"]
    the goal is to choose which is the most appropriate.

    Supports:
        * word separators like "-","_"," "
        * camelCase
        * stop words (eg "do the thing" can resolve to "doThing")
        * zero padded numbers "do thing 01" => "doThing1"
        * textual numbers "do thing one" => "doThing1" or "do thing 1" => "doThingOne"
        * always tries to eat the largest possible match
            "do the best thing", given ["doTheBest","doTheBestThing"] => "doTheBestThing"
        * prefers caps that match, but will accept those that don't
        * also supports variable stacks, so for programming uses it is easy to manage context scope
    """

    def __init__(self):
        self.stackPenaltyFactor=0.10 # parent in the stack is this much less likely to match
        self.contextStack:typing.List[ForgivingNamesContext]=[ForgivingNamesContext()]

    @property
    def globals(self)->ForgivingNamesContext:
        """
        global values, aka the very top Context
        """
        return self.contextStack[0]

    @property
    def current(self)->ForgivingNamesContext:
        """
        current values, aka the very latest Context
        """
        return self.contextStack[-1]

    def add(self,name:str)->None:
        """
        Add a name to the current context
        """
        self.contextStack[-1].add(name)

    def remove(self,name:str):
        """
        Remove a name from the current context
        """
        self.contextStack[-1].remove(name)

    def clear(self):
        """
        Clear out everything and start over
        """
        self.contextStack=[ForgivingNamesContext()]

    def pop(self)->ForgivingNamesContext:
        """
        Take the current context off the stack
        """
        if len(self.contextStack)<2:
            # never remove the global context b/c this is probably an accident
            return self.contextStack[0]
        return self.contextStack.pop()
    def push(self,ctx:typing.Optional[ForgivingNamesContext]=None)->ForgivingNamesContext:
        """
        Add a new context as the current context of the stack

        If you don't pass one in, it creates one and returns it.
        (Whichever way you like to do it is fine.)
        """
        if ctx is None:
            ctx=ForgivingNamesContext()
        self.contextStack.append(ctx)
        return ctx

    def matches(self,
        tape:str,idx:int=0,sorted:bool=True
        )->typing.List[NameMatch]:
        """
        All of the matches possible in the tape, with a rank

        Unless otherwise turned off, will return in sorted order,
        with the most likely candidate first in the list.
        """
        ret=[]
        stackLevels=len(self.contextStack)
        for level,ctx in enumerate(self.contextStack):
            factor=stackLevels-level-1
            for m in ctx.matches(tape,idx,False):
                m.rank*=1-(self.stackPenaltyFactor*factor)
                ret.append(m)
        if sorted:
            ret.sort(reverse=True)
        return ret

    def bestMatch(self,tape:str,idx:int=0)->typing.Optional[NameMatch]:
        """
        Single best match for a given name
        (can still be None, if nothing matched)
    
        This is probably more efficient than matches[0]
        """
        best=None
        stackLevels=len(self.contextStack)
        for level,ctx in enumerate(self.contextStack):
            factor=stackLevels-level-1
            bestForLevel=None
            for m in ctx.matches(tape,idx,False):
                if not bestForLevel or m.rank>bestForLevel.rank:
                    bestForLevel=m
            if bestForLevel:
                bestForLevel.rank*=1-(self.stackPenaltyFactor*factor)
                if not best or bestForLevel.rank>=best:
                    best=bestForLevel
        return best


def cmdline(args:typing.Iterable[str])->int:
    """
    Run the command line

    :param args: command line arguments (WITHOUT the filename)
    """
    didSomething=False
    printhelp=False
    fnames=ForgivingNames()
    for arg in args:
        if arg.startswith('-'):
            av=arg.split('=',1)
            av[0]=av[0].lower()
            if av[0] in ('-h','--help'):
                printhelp=True
            elif av[0]=='--add':
                fnames.add(av[1])
            elif av[0]=='--push':
                fnames.push()
            elif av[0]=='--pop':
                fnames.pop()
            elif av[0] in ('--matches'):
                for m in fnames.matches(av[1]):
                    print(repr(m))
                didSomething=True
            elif av[0] in ('--bestmatch','--find'):
                result=fnames.bestMatch(av[1])
                print(repr(result))
                didSomething=True
            else:
                printhelp=True
        else:
            printhelp=True
    if printhelp or not didSomething:
        print('USEAGE:')
        print('  forgivingNames [options]')
        print('OPTIONS:')
        print('  -h ................................. this help')
        print('  --add=name ......................... add a new name to the list of matchable names')
        print('  --push ............................. push a new name context onto the stack')
        print('  --pop .............................. pop a name context off the stack')
        print('  --find=name  ....................... find a name in the current list of values')
        print('  --matches=name  .................... find all names that match')
        return 1
    return 0


if __name__=='__main__':
    import sys
    cmdline(sys.argv[1:])