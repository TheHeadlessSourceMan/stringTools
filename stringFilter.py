"""
Quickly and easily filter a list of strings based on a match string or pattern.
"""
import typing


MatchLike=typing.Union[str,typing.Pattern[str],
    typing.Iterable[typing.Union[str,typing.Pattern[str]]]]
MatchStringAs=typing.Literal["exact","contains","glob","regex"]

T=typing.TypeVar("T")


def objectsWithMember[T](
    memberName:str,
    src:typing.Iterable[T],
    defaultString:str='',
    match:typing.Optional[MatchLike]=None,
    matchStringAs:MatchStringAs="exact",
    ignorecase:bool=False,
    )->typing.Iterable[T]:
    """
    Quickly and easily filter a list of objects based on
    a match string or pattern of one of their members.

    That is, given a list of objects, reuturn only those where
    obj.memberName matches the given pattern or string.
    """
    for _,v in tupleStringFilter(
        [(getattr(m,memberName,defaultString),m) for m in src],
        match=match,
        matchStringAs=matchStringAs,
        ignorecase=ignorecase):
        #
        yield v


def dictsWithMember[T](
    memberName:str,
    src:typing.Iterable[typing.Dict[str,T]],
    defaultString:str='',
    match:typing.Optional[MatchLike]=None,
    matchStringAs:MatchStringAs="exact",
    ignorecase:bool=False,
    )->typing.Iterable[typing.Dict[str,T]]:
    """
    Quickly and easily filter a list of dicts based on
    a match string or pattern of one of their members.

    Do not confuse with dictStringFilter.
    dictStringFilter is for {name:value}
    dictsWithMember is for [{memberName:name}]
    """
    for _,v in tupleStringFilter(
        [(m.get(memberName,defaultString),m) for m in src],
        match=match,
        matchStringAs=matchStringAs,
        ignorecase=ignorecase):
        #
        yield v


def dictStringFilter[T](
    src:typing.Dict[str,T],
    match:typing.Optional[MatchLike]=None,
    matchStringAs:MatchStringAs="exact",
    ignorecase:bool=False,
    )->typing.Dict[str,T]:
    """
    Quickly and easily filter a {string:value} dict
    a match string or pattern.

    Do not confuse with dictsWithMember.
    dictStringFilter is for {name:value, ...}
    dictsWithMember is for [{memberName:name}, ...]
    """
    return dict(tupleStringFilter(
        src.items(),
        match=match,
        matchStringAs=matchStringAs,
        ignorecase=ignorecase))


def tupleStringFilter[T](
    src:typing.Iterable[typing.Tuple[str,T]],
    match:typing.Optional[MatchLike]=None,
    matchStringAs:MatchStringAs="exact",
    ignorecase:bool=False,
    )->typing.Iterable[typing.Tuple[str,T]]:
    """
    Quickly and easily filter a list of [(string,value)] tuples
    based on a match string or pattern.

    NOTE: for typing, only the rh type (T) of the tuple is specified,
    since the lh type is always str.
    """
    if match is None:
        return src
    if isinstance(match,str) and matchStringAs=="regex":
        import re
        match=re.compile(match,re.IGNORECASE if ignorecase else 0)
    elif hasattr(match,'__iter__'):
        import re
        match=[
            m if isinstance(m,typing.Pattern)
            else re.compile(m,re.IGNORECASE if ignorecase else 0)
            for m in match]
    for k,v in src:
        if isinstance(match,str):
            if matchStringAs=="exact":
                if ignorecase:
                    if k.lower()==match.lower():
                        yield k,v
                else:
                    if k==match:
                        yield k,v
            elif matchStringAs=="contains":
                if ignorecase:
                    if match.lower() in k.lower():
                        yield k,v
                else:
                    if match in k:
                        yield k,v
            elif matchStringAs=="glob":
                import fnmatch
                if fnmatch.fnmatch(k,match):
                    yield k,v
        elif isinstance(match,typing.Pattern):
            if match.match(k):
                yield k,v
        elif hasattr(match,"__iter__"):
            for match1 in match:
                if isinstance(match1,str):
                    if matchStringAs=="exact":
                        if ignorecase:
                            if match1.lower()==k.lower():
                                yield k,v
                                break
                        else:
                            if match1==k:
                                yield k,v
                                break
                    elif matchStringAs=="contains":
                        if ignorecase:
                            if match1.lower() in k.lower():
                                yield k,v
                                break
                        else:
                            if match1 in k:
                                yield k,v
                                break
                elif isinstance(match1,typing.Pattern):
                    if match1.match(k):
                        yield k,v
                        break


def stringFilter(
    src:typing.Union[str,typing.Iterable[str]],
    match:typing.Optional[MatchLike]=None,
    matchStringAs:MatchStringAs="exact",
    ignorecase:bool=False,
    )->typing.Iterable[str]:
    """
    Quickly and easily filter a list of strings based on
    a match string or pattern.
    """
    if isinstance(src,str):
        src=(src,)
    if match is None:
        return src
    if isinstance(match,str) and matchStringAs=="regex":
        import re
        match=re.compile(match,re.IGNORECASE if ignorecase else 0)
    elif hasattr(match,'__iter__'):
        import re
        match=[
            m if isinstance(m,typing.Pattern)
            else re.compile(m,re.IGNORECASE if ignorecase else 0)
            for m in match]
    for s in src:
        if isinstance(match,str):
            if matchStringAs=="exact":
                if ignorecase:
                    if s.lower()==match.lower():
                        yield s
                else:
                    if s==match:
                        yield s
            elif matchStringAs=="contains":
                if ignorecase:
                    if match.lower() in s.lower():
                        yield s
                else:
                    if match in s:
                        yield s
            elif matchStringAs=="glob":
                import fnmatch
                if fnmatch.fnmatch(s,match):
                    yield s
        elif isinstance(match,typing.Pattern):
            if match.match(s):
                yield s
        elif hasattr(match,"__iter__"):
            for match1 in match:
                if isinstance(match1,str):
                    if matchStringAs=="exact":
                        if ignorecase:
                            if match1.lower()==s.lower():
                                yield s
                                break
                        else:
                            if match1==s:
                                yield s
                                break
                    elif matchStringAs=="contains":
                        if ignorecase:
                            if match1.lower() in s.lower():
                                yield s
                                break
                        else:
                            if match1 in s:
                                yield s
                                break
                elif isinstance(match1,typing.Pattern):
                    if match1.match(s):
                        yield s
                        break
