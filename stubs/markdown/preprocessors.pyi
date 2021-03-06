# Stubs for markdown.preprocessors (Python 3)
#
# NOTE: This dynamically typed stub was automatically generated by stubgen.

from . import util
from typing import Any

def build_preprocessors(md_instance: Any, **kwargs: Any): ...

class Preprocessor(util.Processor):
    def run(self, lines: Any) -> None: ...

class NormalizeWhitespace(Preprocessor):
    def run(self, lines: Any): ...

class HtmlBlockPreprocessor(Preprocessor):
    right_tag_patterns: Any = ...
    attrs_pattern: str = ...
    left_tag_pattern: Any = ...
    attrs_re: Any = ...
    left_tag_re: Any = ...
    markdown_in_raw: bool = ...
    def run(self, lines: Any): ...

class ReferencePreprocessor(Preprocessor):
    TITLE: str = ...
    RE: Any = ...
    TITLE_RE: Any = ...
    def run(self, lines: Any): ...
