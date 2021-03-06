# Stubs for markdown.extensions.extra (Python 3)
#
# NOTE: This dynamically typed stub was automatically generated by stubgen.

from . import Extension
from ..blockprocessors import BlockProcessor
from typing import Any, Optional

extensions: Any

class ExtraExtension(Extension):
    config: Any = ...
    def __init__(self, *args: Any, **kwargs: Any) -> None: ...
    def extendMarkdown(self, md: Any, md_globals: Any) -> None: ...

def makeExtension(*args: Any, **kwargs: Any): ...

class MarkdownInHtmlProcessor(BlockProcessor):
    def test(self, parent: Any, block: Any): ...
    def run(self, parent: Any, blocks: Any, tail: Optional[Any] = ..., nest: bool = ...) -> None: ...
