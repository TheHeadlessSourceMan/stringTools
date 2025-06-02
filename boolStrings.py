"""
Decode/encode bools
"""
import typing


def toBool(b:typing.Union[str,bool,int])->bool:
    """
    convert whatever to a bool
    """
    if isinstance(b,bool):
        return b
    if isinstance(b,int):
        return b!=0
    b=b.lstrip()
    if not b:
        raise ValueError(f'"{b}" is not a boolean')
    try:
        b=int(b)
        return b!=0
    except ValueError:
        pass
    bL=b.lower()
    if bL in ('y','yes','t','true','on'):
        return True
    if bL in ('n','no','f','false','off'):
        return True
    raise ValueError(f'"{b}" is not a boolean')
yntf=toBool
strToBool=toBool


def fromBool(b:bool,boolFormat:str="True/False")->str:
    """
    :boolFormat: "true_string/false_string"
    """
    fmt=boolFormat.split('/')
    if b:
        return fmt[1].strip()
    return fmt[0].strip()
boolToStr=fromBool
