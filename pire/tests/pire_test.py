import pickle

import pytest

import pire_py as pire


SCANNER_CLASSES = [
    pire.Scanner,
    pire.ScannerNoMask,
    pire.NonrelocScanner,
    pire.NonrelocScannerNoMask,
]


def check_scanner(scanner, accepts=(), rejects=()):
    for line in accepts:
        assert scanner.Matches(line), '"%s"' % line
    for line in rejects:
        assert not scanner.Matches(line), '"%s"' % line


def check_equivalence(scanner1, scanner2, examples):
    for line in examples:
        assert scanner1.Matches(line) == scanner2.Matches(line), '"%s"' % line


@pytest.fixture(params=SCANNER_CLASSES)
def scanner_class(request):
    return request.param


@pytest.fixture()
def parse_scanner(scanner_class):
    def scanner_factory(pattern, options=""):
        lexer = pire.Lexer(pattern)
        for opt in options:
            if opt == "i":
                lexer.AddFeature(pire.CaseInsensitive())
            elif opt == "a":
                lexer.AddFeature(pire.AndNotSupport())
            else:
                raise ValueError("Unknown option {}".format(opt))
        fsm = lexer.Parse()
        return scanner_class(fsm)
    return scanner_factory


@pytest.fixture()
def example_scanner(parse_scanner):
    return parse_scanner("s(om)*e")


def check_scanner_is_like_example_scanner(scanner):
    check_scanner(scanner, accepts=["se", "somome"], rejects=["", "s"])


class TestFsm(object):
    def test_fsm_is_default_constructible(self):
        f = pire.Fsm()
        assert 1 == f.Size()

    def test_fsm_can_be_made_false(self):
        f = pire.Fsm.MakeFalse()
        assert 1 == f.Size()

    def test_default_fsm_compiles_to_default_scanner(self):
        scanner = pire.Fsm().Compile()
        assert pire.Scanner == type(scanner)

    def test_fsm_compiles_to_scanner_of_choice(self, scanner_class):
        assert scanner_class == type(pire.Fsm().Compile(scanner_class))

    def test_fsm_is_copy_constructible(self):
        fsm = pire.Fsm().Append("ab")
        fsm_copy = pire.Fsm(fsm)
        assert fsm_copy is not fsm
        check_equivalence(
            fsm.Compile(),
            fsm_copy.Compile(),
            ["", "a", "ab", "ab-", "-"]
        )

        fsm.Append("c")
        assert not fsm_copy.Compile().Matches("abc")

    def test_fsm_supports_appending_several_strings(self, scanner_class):
        fsm = pire.Fsm().Append("-")
        fsm.AppendStrings(["abc", "de"])
        check_scanner(
            scanner_class(fsm),
            accepts=["-abc", "-de"],
            rejects=["-", "abc", ""],
        )

    def test_fsm_supports_fluent_inplace_operations(self, scanner_class, parse_scanner):
        a = pire.Fsm().Append("a").AppendDot()

        b = pire.Fsm()
        b.Append("b")

        d = pire.Fsm().Append("d")
        d *= 3

        c = pire.Lexer("c").Parse()

        fsm = a.Iterate()
        fsm += b.AppendAnything()
        fsm |= d
        fsm &= c.PrependAnything().Complement()

        expected_scanner = parse_scanner("((a.)*(b.*)|(d{3}))&~(.*c)", "a")

        check_equivalence(
            expected_scanner,
            scanner_class(fsm), [
                "ddd", "dddc", "a-b--c", "a-a-b--",
                "bdddc", "bddd", "", "b", "bc", "c",
            ]
        )

    def test_fsm_supports_nonmodifying_operations(self, scanner_class, parse_scanner):
        a, b, c, d, e = [pire.Lexer(char).Parse() for char in "abcde"]

        expression = ((a + b.Iterated()) | c.Surrounded() | (2 * (d * 2))) & ~e
        expected_scanner = parse_scanner("((ab*)|(.*c.*)|(d{4}))&~e", "a")

        check_equivalence(
            expected_scanner,
            scanner_class(expression), [
                "a", "abbbb", "c", "--c-",
                "dddd", "--", "e", "-ee-", "",
            ]
        )


class TestLexer(object):
    def test_lexer_default_constructible(self):
        lexer = pire.Lexer()
        assert pire.Fsm == type(lexer.Parse())

    def test_lexer_cannot_be_constructed_with_wrong_argument(self):
        pytest.raises(TypeError, pire.Lexer, 42)

    def test_lexer_parses_valid_regexp_right(self, parse_scanner):
        check_scanner(
            parse_scanner(""),
            accepts=[""],
            rejects=["some"],
        )
        check_scanner(
            parse_scanner("(2.*)&([0-9]*_1+)", "a"),
            accepts=["2123_1111", "2_1"],
            rejects=["123_1111", "2123_1111$", "^_1"],
        )
        check_scanner(
            parse_scanner("a|b|c"),
            accepts=["a", "b", "c"],
            rejects=["", "ab", "ac", "bc", "aa", "bb", "cc"],
        )

    def test_lexer_raises_on_parsing_invalid_regexp(self):
        pytest.raises(Exception, pire.Lexer("[ab").Parse)

    def test_empty_feature_cannot_be_added(self):
        pytest.raises(ValueError, pire.Lexer().AddFeature, pire.Feature())

    def test_features_cannot_be_reused(self):
        lexer1 = pire.Lexer()
        lexer2 = pire.Lexer()
        feature = pire.CaseInsensitive()
        lexer1.AddFeature(feature)
        pytest.raises(ValueError, lexer2.AddFeature, feature)


class TestScanner(object):
    def test_scanner_inherits_from_base_scanner(self, scanner_class):
        assert issubclass(scanner_class, pire.BaseScanner)

    def test_scanner_is_default_constructible(self, scanner_class):
        scanner = scanner_class()
        assert scanner.Empty()
        assert 1 == scanner.Size()
        check_scanner(scanner, rejects=["", "some"])

    def test_scanner_raises_when_matching_not_string_but_stays_valid(self, example_scanner):
        for invalid_input in [None, False, True, 0, 42]:
            pytest.raises(Exception, example_scanner.Matches, invalid_input)
        check_scanner_is_like_example_scanner(example_scanner)

    def test_scanner_is_picklable(self, example_scanner):
        packed = pickle.dumps(example_scanner)
        unpacked = pickle.loads(packed)
        check_scanner_is_like_example_scanner(unpacked)

    def test_scanner_is_saveable_and_loadable(self, example_scanner):
        packed = example_scanner.Save()
        unpacked = example_scanner.__class__.Load(packed)
        check_scanner_is_like_example_scanner(unpacked)
