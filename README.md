# pire_py

This is a cython-based python binding of [PIRE](https://github.com/yandex/pire).

What is not wrapped:

- It is impossible yet to subclass `Feature`s and `Scanner`s in python and pass the
  extension back to C++;
- Most low-level operations with `Fsm`;
- `mmap`- and `Action`-related methods and functions;
- Run for pair of scanners;
- `Feature` and `Encoding` classes.

Interface of the binding is similar to the original one. Differences:

- All C++-space global template functions are wrapped as python instance methods.
- `Fsm::operator * ()` is wrapped as `Fsm.Iterated()`.
- All scanners' states are represented as classes similar to `Pire::RunHelper`.
- `Encoding`, `Feature` and `Option` abstractions are replaced with single
  `Options` abstraction, which is used to tweak Lexer behavior. `Options` can
  be either parsed from string such as "aiyu" or composed of predefined
  constants such as `I` and `UTF8`.
- Instead of `lexer.AddFeature(Capture(42))` you use `lexer.AddCapturing(42)`.
- Unsuccessful glue operation raises `OverflowError` instead of returning empty
  scanner.
