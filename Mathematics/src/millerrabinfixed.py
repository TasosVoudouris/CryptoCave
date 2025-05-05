def miller_rabin_test_fixed(n, a_list):
    if n % 2 == 0:
        return 'Composite'
    
    r, s = 0, n - 1
    while s % 2 == 0:
        s //= 2
        r += 1
    assert (2**r * s == n - 1)

    for a in a_list:
        x = pow(a, s, n)
        if x in (1, n - 1):
            continue
        for _ in range(r):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return 'Composite'
    return 'Probably prime'