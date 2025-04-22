"""
Extract filenames mentioned in command line
"""
import typing
from pathlib import Path


def commandlineToFiles(
    cmdline:str,
    includeMissing:bool=False,
    mustHaveExtension:bool=True,
    extensions:typing.Union[None,str,typing.Iterable[str]]=None,
    relativeTo:typing.Union[str,Path]='.'
    )->typing.Iterable[Path]:
    """
    Extract filenames mentioned in command line

    TODO: handle quoted parameters
    """
    if extensions is None:
        extensions=[]
    else:
        if isinstance(extensions,str):
            extensions=[extensions]
        fixedExtensions=[]
        for extension in extensions:
            if not extension:
                continue
            if extension[0]!='.':
                extension='.'+extension
            fixedExtensions.append(extension.lower())
        extensions=fixedExtensions
    if not relativeTo:
        relativeTo=Path('.')
    elif not isinstance(relativeTo,Path):
        relativeTo=Path(relativeTo)
    for param in cmdline.split():
        if not param:
            continue
        elif param[0]=='-':
            parts=param.split('=',1)
            if len(parts)>1:
                param=parts[-1]
            else:
                parts=param.split(':',1)
                if len(parts)>1:
                    param=parts[-1]
                else:
                    continue
        try:
            # NOTE: if a path is absolute, pathlib discards preceeding path
            filename=relativeTo/param
        except Exception:
            continue
        if mustHaveExtension and not filename.suffix:
            continue
        if extensions and filename.suffix.lower() not in extensions:
            continue
        if includeMissing or filename.exists():
            yield filename
commandLineToFiles=commandlineToFiles
cmdlineToFiles=commandlineToFiles
cmdLineToFiles=commandlineToFiles
