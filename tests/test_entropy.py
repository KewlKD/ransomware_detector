from analysis.entropy import shannon_entropy, string_entropy


def test_low_entropy():
    data = b"AAAAAAAAAAAA"
    assert shannon_entropy(data) < 1.0


def test_high_entropy():
    data = b"ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890"
    assert shannon_entropy(data) > 4.0


def test_string_entropy():
    assert string_entropy("hello") > 0