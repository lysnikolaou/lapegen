# lepegen
Pegen with labeled exceptions - A small experiment

This is a small experiment, where we try out various things on how to implement labeled
exceptions in the pegen proejct. We are also trying to better understand labeled exception
semantics, by writing Python code to mimic the behavior the CPython PEG parser would have,
if it was supporting labeled exceptions.

For a discussion about this, see [this](https://github.com/we-like-parsers/cpython/issues/123) issue on the project's main repo.

For more info on the PEG parser, see [PEP 617](https://www.python.org/dev/peps/pep-0617/)
