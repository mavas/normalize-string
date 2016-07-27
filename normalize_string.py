def normalize_string(s):
    """Normalizes a string representing a file path, in a particular way.

    All single dot components of the path are removed ("foo/./bar" ->
    "foo/bar").  All double dots components of the path are removed, along with
    their parent directory ("foo/bar/../baz" -> "foo/baz").  Also this:
    "foo//bar" -> "foo/bar".
    """
    # Do some preformatting. Split the paths into components. After this, there
    # are no more slashes in the data; the double slashes are replaced with
    # elements consisting of an empty string.
    r = s.split('/')
    if r[0] == '':
        b = True
    else:
        b = False

    # Remove the elements consisting of a single dot, and the elements which
    # used to represent the double slash.
    r = filter(lambda x: x != '.', r)
    r = filter(lambda x: x != '', r)

    # We need to take care of the logic of the double dots - removing both the
    # original double dot entry, and the entry before it. To do this, we
    # replace both with a single dot, and then later run the filter sweep on
    # the data again.
    i = 0; l = len(r)
    while i < l:
        # If the current element is the double dot, replace the prior element,
        # and this one, with a single dot.
        if r[i] == '..':
            r[i] = r[i-1] = '.'
        i += 1

    # Run a final cleaning sweep on the single dots.
    r = filter(lambda x: x != '.', r)

    # Join the rest of the data with the path separator.
    return '/'.join(r)


if __name__ == '__main__':
    assert normalize_string("foo/./bar") == "foo/bar"
    assert normalize_string("foo/bar/../baz") == "foo/baz"
    assert normalize_string("foo//bar") == "foo/bar"
