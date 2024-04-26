def solution(inp):
    """Exercise from 22_49

    :Examples:

    >>> solution([[18, 20], [45, 2], [61, 12], [37, 6], [21, 21], [78, 9]])
    ['Open', 'Open', 'Senior', 'Open', 'Open', 'Senior']

    >>> solution([(45, 12), (55, 21), (19, -2), (104, 20)])
    ['Open', 'Senior', 'Open', 'Senior']

    >>> solution([(16, 23), (73, 1), (56, 20), (1, -1)])
    ['Open', 'Open', 'Senior', 'Open']

    """
    senior = (age >= 55 and handicap > 7 for age, handicap in inp)
    labels = ['Senior' if is_senior else 'Open' for is_senior in senior]
    return labels


def solution_flo(inp):
    return ['Senior' if age >= 55 and handicap > 7 else 'Open' for age, handicap in inp]


if __name__ == '__main__':
    import doctest
    doctest.testmod(verbose=True)

