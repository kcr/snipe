# Stubs for ply.lex (Python 3)
#
# NOTE: This dynamically typed stub was automatically generated by stubgen.

from typing import Any, Optional

__tabversion__: str
StringTypes: Any

class LexError(Exception):
    args: Any = ...
    text: Any = ...
    def __init__(self, message: Any, s: Any) -> None: ...

class LexToken: ...

class PlyLogger:
    f: Any = ...
    def __init__(self, f: Any) -> None: ...
    def critical(self, msg: Any, *args: Any, **kwargs: Any) -> None: ...
    def warning(self, msg: Any, *args: Any, **kwargs: Any) -> None: ...
    def error(self, msg: Any, *args: Any, **kwargs: Any) -> None: ...
    info: Any = ...
    debug: Any = ...

class NullLogger:
    def __getattribute__(self, name: Any): ...
    def __call__(self, *args: Any, **kwargs: Any): ...

class Lexer:
    lexre: Any = ...
    lexretext: Any = ...
    lexstatere: Any = ...
    lexstateretext: Any = ...
    lexstaterenames: Any = ...
    lexstate: str = ...
    lexstatestack: Any = ...
    lexstateinfo: Any = ...
    lexstateignore: Any = ...
    lexstateerrorf: Any = ...
    lexstateeoff: Any = ...
    lexreflags: int = ...
    lexdata: Any = ...
    lexpos: int = ...
    lexlen: int = ...
    lexerrorf: Any = ...
    lexeoff: Any = ...
    lextokens: Any = ...
    lexignore: str = ...
    lexliterals: str = ...
    lexmodule: Any = ...
    lineno: int = ...
    lexoptimize: bool = ...
    def __init__(self) -> None: ...
    def clone(self, object: Optional[Any] = ...): ...
    def writetab(self, lextab: Any, outputdir: str = ...) -> None: ...
    lextokens_all: Any = ...
    def readtab(self, tabfile: Any, fdict: Any) -> None: ...
    def input(self, s: Any) -> None: ...
    def begin(self, state: Any) -> None: ...
    def push_state(self, state: Any) -> None: ...
    def pop_state(self) -> None: ...
    def current_state(self): ...
    def skip(self, n: Any) -> None: ...
    lexmatch: Any = ...
    def token(self): ...
    def __iter__(self): ...
    def next(self): ...
    __next__: Any = ...

def get_caller_module_dict(levels: Any): ...

class LexerReflect:
    ldict: Any = ...
    error_func: Any = ...
    tokens: Any = ...
    reflags: Any = ...
    stateinfo: Any = ...
    modules: Any = ...
    error: bool = ...
    log: Any = ...
    def __init__(self, ldict: Any, log: Optional[Any] = ..., reflags: int = ...) -> None: ...
    def get_all(self) -> None: ...
    def validate_all(self): ...
    def get_tokens(self) -> None: ...
    def validate_tokens(self) -> None: ...
    literals: Any = ...
    def get_literals(self) -> None: ...
    def validate_literals(self) -> None: ...
    states: Any = ...
    def get_states(self) -> None: ...
    toknames: Any = ...
    funcsym: Any = ...
    strsym: Any = ...
    ignore: Any = ...
    errorf: Any = ...
    eoff: Any = ...
    def get_rules(self): ...
    def validate_rules(self) -> None: ...
    def validate_module(self, module: Any) -> None: ...

def lex(module: Optional[Any] = ..., object: Optional[Any] = ..., debug: bool = ..., optimize: bool = ..., lextab: str = ..., reflags: Any = ..., nowarn: bool = ..., outputdir: Optional[Any] = ..., debuglog: Optional[Any] = ..., errorlog: Optional[Any] = ...): ...
def runmain(lexer: Optional[Any] = ..., data: Optional[Any] = ...) -> None: ...
def TOKEN(r: Any): ...
Token = TOKEN
