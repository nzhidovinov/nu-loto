import loto


def test_unique_numbers():
    numbers = loto.unique_numbers(10, 1, 10)
    assert len(numbers) == 10
    assert len(numbers) == len(set(numbers))
    assert min(numbers) == 1
    assert max(numbers) == 10


def test_keg():
    keg = loto.Keg(10)
    assert keg.value == 10
    assert keg.is_crossed is False
    keg.cross_out()
    assert keg.is_crossed is True
    assert keg == loto.Keg(10)
    assert keg != loto.Keg(1)
