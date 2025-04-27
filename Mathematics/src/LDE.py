def hop_and_skip(a, b):
    """
    Computes the Bézout identity: gcd(a, b) = x * a + y * b
    using a traceable version of the Euclidean algorithm.
    """
    u, v = a, b
    u_hops, u_skips = 1, 0
    v_hops, v_skips = 0, 1

    while v != 0:
        q = u // v
        r = u % v
        r_hops = u_hops - q * v_hops
        r_skips = u_skips - q * v_skips

        u, v = v, r
        u_hops, v_hops = v_hops, r_hops
        u_skips, v_skips = v_skips, r_skips

    print(f"{u} = {u_hops}*{a} + {u_skips}*{b}")

def solve_LDE(a, b, c):
    """
    Solves the equation ax + by = c for integer x, y.
    Returns one solution (x, y) if it exists, otherwise None.
    """
    u, v = a, b
    u_hops, u_skips = 1, 0
    v_hops, v_skips = 0, 1

    while v != 0:
        q = u // v
        r = u % v
        r_hops = u_hops - q * v_hops
        r_skips = u_skips - q * v_skips

        u, v = v, r
        u_hops, v_hops = v_hops, r_hops
        u_skips, v_skips = v_skips, r_skips

    g = u  # gcd(a, b)

    if c % g == 0:
        d = c // g
        x = d * u_hops
        y = d * u_skips
        print(f"{a}x + {b}y = {c} has solutions if and only if:")
        print(f"x = {x} + {b // g}n, y = {y} - {a // g}n for n in ℤ.")
        return x, y
    else:
        print(f"No solutions exist for {a}x + {b}y = {c} because gcd({a}, {b}) = {g} does not divide {c}.")
    return None


print(solve_LDE(1337, 137, 1))