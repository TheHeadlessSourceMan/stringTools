import typing
import re
from stringTools import ansiColorToHtml

Txt2HtmlCanConvert = typing.Union[str,typing.TextIO,typing.BinaryIO]

class Txt2Html:
    """
    A robust string-to-html class that can do:
        * 1-to-1 text display (not needing <pre> tag)
        * urls to <a> tags
        * ansi (eg windows) console colors
        * vt100 (eg linux) console colors
        * arbitrary user-defined pattern-to-html conversions
            eg, turn a git hash into a link
            addConversion(r'(([0-9a-zA-Z]{7})|([0-9a-zA-Z]{40}))',r'<a href="https://github.com/[user]/[project]/commit/\1">\1</a>')
    """

    EMAIL_REGEX = re.compile('([a-z0-9_.]+[@][a-z0-9_]+([.][a-z0-9_]+)+)',re.DOTALL|re.IGNORECASE)

    # TODO: I think I have a better version of this somewhere, but this should work for now
    URL_REGEX = re.compile('([a-z0-9_]+[:]//[^\s]+)',re.DOTALL|re.IGNORECASE)

    def __init__(self,
        userConversion:typing.Union[
            None,
            typing.Tuple[typing.Union[str,typing.Pattern],str],
            typing.Iterable[typing.Tuple[typing.Union[str,typing.Pattern],str]]
            ]=None,
        detectUrls=True,detectAnsi=True,detectVt100=False,detectEmail=True,fixedWidth=False):
        """ """
        self.fixedWidth=True
        self.detectUrls=detectUrls
        self.detectEmail=detectEmail
        self.detectVt100=detectVt100
        self.detectAnsi=detectAnsi
        self.fixedWidth=fixedWidth
        self._userConversions:typing.List[typing.Tuple[typing.Pattern,str]]=[]
        if userConversion is not None:
            self.addConversions(userConversion)

    def addConversion(self,
        userConversion:typing.Union[
            typing.Tuple[typing.Union[str,typing.Pattern],str],
            typing.Iterable[typing.Tuple[typing.Union[str,typing.Pattern],str]]
            ]
        )->None:
        """
        Add one or more user conversion
        """
        if isinstance(userConversion,tuple):
            userConversion=[userConversion] # type: ignore
        for pattern,replacement in userConversion:
            if isinstance(pattern,str):
                pattern=re.compile(pattern,re.DOTALL|re.IGNORECASE)
            self._userConversions.append((pattern,replacement))
    addConversions=addConversion

    def _doUserConversions(self,s:str)->str:
        """
        perform all user conversions
        """
        for pattern,replacement in self._userConversions:
            s=pattern.sub(replacement,s)
        return s
    
    def _doAnsiConversion(self,s:str)->str:
        """
        perform all ansi (eg windows console) conversions
        """
        ret=ansiColorToHtml(s)
        if s!=ret:
            self.fixedWidth=True
        return ret
    
    def _doVt100Conversion(self,s:str)->str:
        """
        perform all vt100 (eg linux console) conversions
        """
        from pygments import highlight
        from pygments.lexers import get_lexer_by_name
        from pygments.formatters import HtmlFormatter
        # use pygments for everything else
        lexer=get_lexer_by_name('console')
        formatter=HtmlFormatter()
        s=highlight(s,lexer,formatter)
        raise NotImplementedError("This doesn't seem to work correctly")
        return s

    def _doUrlConversion(self,s:str)->str:
        """
        perform all url conversions
        """
        return self.URL_REGEX.sub(r'<a href="\1">\1</a>',s)
    
    def _doEmailConversion(self,s:str)->str:
        """
        perform all email address conversions
        """
        return self.EMAIL_REGEX.sub(r'<a href="mailto:\1">\1</a>',s)
    
    def convert(self,data:Txt2HtmlCanConvert)->str:
        """
        perform all selected conversions
        """
        if isinstance(data,str):
            s=data
        else:
            d=data.read()
            if isinstance(d,str):
                s=d
            else:
                s=d.decode('utf-8',errors='ignore')
        # now convert
        if self.detectAnsi:
            s=self._doAnsiConversion(s)
        if self.detectVt100:
            s=self._doVt100Conversion(s)
        if self.detectUrls:
            s=self._doUrlConversion(s)
        if self.detectEmail:
            s=self._doEmailConversion(s)
        s=self._doUserConversions(s)
        if self.fixedWidth:
            s=f'<span style="font-family:ui-monospace,monospace; background-color:black">{s}</span>'
        return s
    def __call__(self,data:Txt2HtmlCanConvert)->str:
        return self.convert(data)
    
def txt2Html(
    data:Txt2HtmlCanConvert,
    userConversion:typing.Union[
        typing.Tuple[typing.Union[str,typing.Pattern],str],
        typing.Iterable[typing.Tuple[typing.Union[str,typing.Pattern],str]]
        ]=(),
    detectUrls=True,detectAnsi=True,detectVt100=False,detectEmail=True,fixedWidth=False):
    """ """
    return Txt2Html(userConversion,detectUrls,detectAnsi,detectVt100,detectEmail,fixedWidth)(data)

def test():
    def t(s,u=None):
        print(s)
        s=txt2Html(s,userConversion=u,fixedWidth=True)
        print('\t',s)
        print()
    t("hello world")
    t("hello http://toshistation.com")
    t("Hello gradma@gmail.com")
    t("Hello 1234567 github",(r'(([0-9a-zA-Z]{7})|([0-9a-zA-Z]{40}))',r'<a href="https://github.com/[user]/[project]/commit/\1">\1</a>'))

test()