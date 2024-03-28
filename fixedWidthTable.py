"""
Tools for parsing and printing text fixed-with tables, eg
    Name    Age   Occupation
    ----    ---   ----------
    Cindy   21    Nurse
    Doogie  14    Doctor
"""
import typing
import re
import pandas as pd
splitWithWhitespace=re.compile(r'''([^\s]+)[\s]+''')


def _parseFixedWidthTable(data:typing.Union[str,typing.Iterable[str]]):
    """
    Helper to split table into ([header],[[row_val]])
    """
    if isinstance(data,str):
        data=data.replace('\r','').split('\n')
    header:typing.List[str]=[]
    headerIndices=[]
    lines=[]
    for line in data:
        if not header:
            for m in splitWithWhitespace.finditer(line):
                headerIndices.append((m.start(0),m.end(0)))
                header.append(m.group(1))
        else:
            strp=line.lstrip()
            if not strp:
                continue
            if strp.startswith('---'):
                continue
            cols=[]
            maxl=len(line)-1
            for start,stop in headerIndices:
                cols.append(line[min(start,maxl):min(stop,maxl)].strip())
            lines.append(cols)
    return (header,lines)


def parseFixedWidthTable(
    data:typing.Union[str,typing.Iterable[str]]
    )->typing.List[typing.Dict[str,str]]:
    """
    parse a fixed width table into a list of dicts (json compatible)

    see also: parseFixedWidthTablePandas()
    """
    header,lines=_parseFixedWidthTable(data)
    ret=[]
    for line in lines:
        dct={}
        for k,v in zip(header,line):
            dct[k]=v
        ret.append(dct)
    return ret


def parseFixedWidthTablePandas(
    data:typing.Union[str,typing.Iterable[str]]
    )->typing.List[typing.Dict[str,str]]:
    """
    parse a fixed width table into a list of dicts (json compatible)

    see also: parseFixedWidthTablePandas()
    """
    header,lines=_parseFixedWidthTable(data)
    vals=[]
    ret={}
    for h in header:
        valList:typing.List[str]=[]
        ret[h]=valList
        vals.append(valList)
    for line in lines:
        for lst,v in zip(vals,line):
            lst.append(v)
    return pd.DataFrame(ret)
