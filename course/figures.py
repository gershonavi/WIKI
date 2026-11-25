"""Draw the figures for the course exercises: python3 course/figures.py  ->  course/img/*.svg

One figure per exercise (key 'LL-E', e.g. '07-3'; lesson 17 tasks '17-1'..'17-7')
and one per worked example (key 'LL-eK', e.g. '04-e6').
Labels are kept in English/math so they render the same everywhere; the Hebrew caption is in the lesson.
"""
import os, math, cmath
from math import gcd, log, sqrt, pi, comb
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'img')
os.makedirs(OUT, exist_ok=True)
plt.rcParams.update({'svg.fonttype': 'none', 'font.size': 10, 'axes.spines.top': False,
                     'axes.spines.right': False, 'figure.figsize': (6.4, 3.4)})
C1, C2, C3, C4, GR = '#1f77b4', '#d62728', '#2ca02c', '#ff7f0e', '#9a9a9a'
FIGS = {}


def fig(key):
    def deco(f):
        FIGS[key] = f
        return f
    return deco


def save(key):
    plt.tight_layout()
    plt.savefig(os.path.join(OUT, key + '.svg'))
    if os.environ.get('PREVIEW'):
        plt.savefig(os.path.join(os.environ['PREVIEW'], key + '.png'), dpi=60)
    plt.close('all')


# ---------- number-theory helpers ----------
N = 2_000_000
_s = bytearray([1]) * (N + 1); _s[0] = _s[1] = 0
for _i in range(2, int(N ** .5) + 1):
    if _s[_i]:
        _s[_i * _i::_i] = bytearray(len(_s[_i * _i::_i]))
PR = [i for i in range(N + 1) if _s[i]]
isp = lambda n: n <= N and bool(_s[n]) if n >= 0 else False


def factor(n):
    f, d = {}, 2
    while d * d <= n:
        while n % d == 0:
            f[d] = f.get(d, 0) + 1; n //= d
        d += 1
    if n > 1:
        f[n] = f.get(n, 0) + 1
    return f


def divisors(n):
    return [d for d in range(1, n + 1) if n % d == 0]


def mu(n):
    f = factor(n)
    return 0 if any(e > 1 for e in f.values()) else (-1) ** len(f)


def phi(n):
    r = n
    for p in factor(n):
        r = r // p * (p - 1)
    return r


def legendre(a, p):
    r = pow(a % p, (p - 1) // 2, p)
    return 0 if r == 0 else (1 if r == 1 else -1)


def circle_nodes(ax, n, labels=None, r=1.0, color='k', size=60, start=90):
    ang = [math.radians(start - 360 * k / n) for k in range(n)]
    pts = [(r * math.cos(a), r * math.sin(a)) for a in ang]
    ax.add_patch(plt.Circle((0, 0), r, fill=False, color='#dddddd'))
    for k, (x, y) in enumerate(pts):
        ax.scatter([x], [y], s=size, color=color, zorder=3)
        ax.annotate(str(labels[k] if labels else k), (x * 1.16, y * 1.16), ha='center', va='center', fontsize=9)
    ax.set_aspect('equal'); ax.axis('off')
    return pts


def arrow(ax, a, b, color=C2, rad=0.15):
    ax.annotate('', xy=b, xytext=a, arrowprops=dict(arrowstyle='->', color=color, lw=1.3,
                                                    connectionstyle=f'arc3,rad={rad}', shrinkA=6, shrinkB=6))


def power_cycle(ax, g, m, title):
    pts = circle_nodes(ax, m, labels=list(range(m)))
    x, seen = 1, []
    for _ in range(m):
        y = x * g % m
        arrow(ax, pts[x], pts[y])
        seen.append(x); x = y
        if x == 1:
            break
    for k in seen:
        ax.scatter(*pts[k], s=90, color=C2, zorder=4)
    ax.set_title(title)


# ================= lesson 1 =================
@fig('01-1')
def _():
    ax = plt.gca()
    xs = range(-112, -90)
    ax.axhline(0, color='k', lw=.8)
    for x in xs:
        ax.plot([x, x], [-.08, .08], color='k', lw=.6)
        if x % 7 == 0:
            ax.scatter([x], [0], s=60, color=C1, zorder=3); ax.annotate(str(x), (x, -.3), ha='center')
    ax.scatter([-100], [0], s=80, color=C2, zorder=4); ax.annotate('-100', (-100, .3), ha='center', color=C2)
    ax.annotate('', xy=(-100, .12), xytext=(-105, .12), arrowprops=dict(arrowstyle='->', color=C3, lw=2))
    ax.text(-102.5, .45, 'r = 5', ha='center', color=C3)
    ax.text(-112, .8, '-100 = 7·(-15) + 5,   0 ≤ r < 7', fontsize=11)
    ax.set_ylim(-.7, 1.1); ax.set_yticks([]); ax.spines['left'].set_visible(False)
    ax.set_xlabel('multiples of 7 (blue): the remainder is the step from the multiple just below')
    save('01-1')


@fig('01-2')
def _():
    ax = plt.gca()
    for a in range(1, 31):
        for b in range(1, 31):
            if b % a == 0:
                ax.scatter(a, b, s=40, color=C1)
            if (b * b) % (a * a) == 0:
                ax.scatter(a, b, s=110, facecolors='none', edgecolors=C2)
    ax.set_xlabel('a'); ax.set_ylabel('b'); ax.set_aspect('equal')
    ax.set_title('dots: a | b      circles: a² | b²   (they coincide)')
    save('01-2')


@fig('01-3')
def _():
    fig_, ax = plt.subplots(figsize=(6.6, 2.6))
    ns = list(range(1, 17))
    rows = [('÷2', 2), ('÷3', 3), ('÷4', 4)]
    for r, (lab, d) in enumerate(rows):
        for n in ns:
            ax.add_patch(plt.Rectangle((n - .45, 2 - r - .4), .9, .8, color=C1 if n % d == 0 else '#eeeeee'))
        ax.text(.1, 2 - r, lab, va='center', ha='right')
    for s in (1, 5, 9):
        ax.add_patch(plt.Rectangle((s - .5, -.55), 4, 3.1, fill=False, edgecolor=C2, lw=1.5))
    ax.set_xlim(-.6, 16.6); ax.set_ylim(-.7, 2.7); ax.set_yticks([]); ax.set_xticks(ns)
    ax.set_title('every window of 4 consecutive numbers has a multiple of 4, another even number, and a multiple of 3')
    ax.title.set_fontsize(8.5); ax.spines['left'].set_visible(False)
    save('01-3')


@fig('01-4')
def _():
    ns = np.arange(0, 9)
    ax = plt.gca()
    v = [4 ** int(n) + 5 for n in ns]
    ax.bar(ns, [x / 3 for x in v], color=C1)
    for n, x in zip(ns, v):
        ax.text(n, x / 3 * 1.15, f'{x}=3·{x//3}', ha='center', fontsize=7, rotation=90)
    ax.set_yscale('log'); ax.set_xticks(ns); ax.set_xlabel('n'); ax.set_ylabel('(4^n + 5) / 3')
    ax.set_title('always an integer: 4 ≡ 1 (mod 3) ⇒ 4^n + 5 ≡ 1 + 5 ≡ 0')
    save('01-4')

@fig('01-5')
def _():
    ax = plt.gca()
    ns = [n for n in range(-8, 9) if n != -1]
    vals = [(n * n + 1) / (n + 1) for n in ns]
    ok = [(n * n + 1) % (n + 1) == 0 for n in ns]
    ax.axhline(0, color=GR, lw=.6)
    ax.scatter(ns, vals, c=[C2 if o else C1 for o in ok], s=[80 if o else 25 for o in ok], zorder=3)
    xs = np.linspace(-8, 8, 600); xs = xs[np.abs(xs + 1) > .15]
    ax.plot(xs, (xs ** 2 + 1) / (xs + 1), color=GR, lw=.8)
    for n, v, o in zip(ns, vals, ok):
        if o:
            ax.annotate(f'n={n}', (n, v), xytext=(5, 5), textcoords='offset points', color=C2)
    ax.set_ylim(-12, 10); ax.set_xlabel('n'); ax.set_ylabel('(n²+1)/(n+1)')
    ax.set_title('integer only when (n+1) | 2  (red points)')
    save('01-5')


@fig('01-6')
def _():
    d = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    sign = [(-1) ** (len(d) - 1 - i) for i in range(len(d))]
    ax = plt.gca()
    ax.bar(range(9), d, color=C1, alpha=.5, label='digit (sum = 45)')
    ax.bar(range(9), [a * s for a, s in zip(d, sign)], color=C2, alpha=.8, width=.45, label='signed digit (sum = 5)')
    ax.axhline(0, color='k', lw=.6)
    ax.set_xticks(range(9)); ax.set_xticklabels([str(x) for x in d]); ax.legend(fontsize=8)
    ax.set_title('123456789:  45 ≡ 0 (mod 9),  5 ≢ 0 (mod 11)')
    save('01-6')


# ================= lesson 2 =================
def euclid_tiles(ax, a, b, title):
    x0, y0, w, h = 0, 0, a, b
    cols = [C1, C3, C4, C2, '#8c564b', '#9467bd']
    k = 0
    while w and h:
        if w >= h:
            q = w // h
            for i in range(q):
                ax.add_patch(plt.Rectangle((x0 + i * h, y0), h, h, ec='k', fc=cols[k % 6], alpha=.55))
            if h > a / 30:
                ax.text(x0 + h / 2, y0 + h / 2, str(h), ha='center', va='center', fontsize=8)
            x0 += q * h; w -= q * h
        else:
            q = h // w
            for i in range(q):
                ax.add_patch(plt.Rectangle((x0, y0 + i * w), w, w, ec='k', fc=cols[k % 6], alpha=.55))
            if w > a / 30:
                ax.text(x0 + w / 2, y0 + w / 2, str(w), ha='center', va='center', fontsize=8)
            y0 += q * w; h -= q * w
        k += 1
    ax.set_xlim(0, a); ax.set_ylim(0, b); ax.set_aspect('equal'); ax.set_title(title)


@fig('02-1')
def _():
    euclid_tiles(plt.gca(), 252, 198, 'Euclid = cutting squares: 252×198 → 54 → 36 → 18 (the gcd)')
    save('02-1')


@fig('02-2')
def _():
    M = 30
    G = np.array([[gcd(a, b) for a in range(1, M + 1)] for b in range(1, M + 1)])
    ax = plt.gca()
    im = ax.imshow(np.log(G), origin='lower', extent=(.5, M + .5, .5, M + .5), cmap='Blues')
    ax.plot(range(1, M), range(2, M + 1), color=C2, lw=1.5, label='b = a+1 : gcd = 1')
    ax.plot(range(1, M - 1, 2), range(3, M + 1, 2), color=C4, lw=1.5, label='b = a+2, a odd : gcd = 1')
    ax.set_xlabel('a'); ax.set_ylabel('b'); ax.legend(fontsize=7, loc='upper left'); ax.set_title('gcd(a, b) (darker = larger)')
    save('02-2')


@fig('02-3')
def _():
    euclid_tiles(plt.gca(), 89, 55, 'Fibonacci 89×55: every step removes one square, down to 1')
    save('02-3')


@fig('02-4')
def _():
    fig_, axs = plt.subplots(1, 2, figsize=(6.6, 3.3))
    for ax, c in zip(axs, (21, 20)):
        X, Y = np.meshgrid(range(-6, 9), range(-4, 6))
        ax.scatter(X, Y, s=6, color=GR)
        xs = np.linspace(-6, 8, 100)
        ax.plot(xs, (c - 6 * xs) / 15, color=C1)
        hits = [(x, y) for x in range(-6, 9) for y in range(-4, 6) if 6 * x + 15 * y == c]
        if hits:
            ax.scatter(*zip(*hits), s=60, color=C2, zorder=3)
        ax.set_ylim(-4, 5); ax.set_title(f'6x + 15y = {c}: ' + ('lattice points every (5,-2)' if hits else 'no lattice point'))
        ax.title.set_fontsize(9)
    save('02-4')


@fig('02-5')
def _():
    ax = plt.gca()
    pts = [(a, b) for a in range(1, 40) for b in range(1, 40) if gcd(a, b) == 1 and a != b]
    col = [C2 if gcd(a + b, abs(a - b)) == 2 else C1 for a, b in pts]
    ax.scatter(*zip(*pts), c=col, s=8)
    ax.set_xlabel('a'); ax.set_ylabel('b'); ax.set_aspect('equal')
    ax.set_title('coprime (a,b): gcd(a+b, a−b) = 1 (blue) or 2 (red: both odd)')
    save('02-5')


@fig('02-6')
def _():
    big, small, B, S = 11, 7, 0, 0
    hist = [(0, 0)]
    while B != 1:
        if S == 0:
            S = small
        elif B == big:
            B = 0
        else:
            t = min(S, big - B); S -= t; B += t
        hist.append((S, B))
        if len(hist) > 60:
            break
    ax = plt.gca()
    ax.step(range(len(hist)), [h[1] for h in hist], where='post', color=C1, label='11-litre jug')
    ax.step(range(len(hist)), [h[0] for h in hist], where='post', color=C4, label='7-litre jug')
    ax.scatter([len(hist) - 1], [1], s=80, color=C2, zorder=3)
    ax.annotate('1 litre', (len(hist) - 1, 1), xytext=(-40, 15), textcoords='offset points', color=C2)
    ax.set_xlabel('step (fill 7 / pour into 11 / empty 11)'); ax.set_ylabel('litres'); ax.legend(fontsize=8)
    ax.set_title('7·8 − 11·5 = 1')
    save('02-6')


# ================= lesson 3 =================
def factor_tree(ax, n, x0, title):
    def rec(m, x, y, w):
        ax.text(x, y, str(m), ha='center', va='center', fontsize=9,
                bbox=dict(boxstyle='round', fc='#fde0dd' if isp(m) else 'white', ec=C2 if isp(m) else 'k'))
        if isp(m) or m == 1:
            return
        p = min(factor(m))
        for xx, mm in ((x - w, p), (x + w, m // p)):
            ax.plot([x, xx], [y - .12, y - .88], color=GR, lw=.8)
            rec(mm, xx, y - 1, w * .6)
    rec(n, x0, 0, 1.0)
    ax.text(x0, .6, title, ha='center', fontsize=9)


@fig('03-1')
def _():
    ax = plt.gca(); plt.gcf().set_size_inches(6.6, 3.2)
    factor_tree(ax, 1001, 0, '1001 = 7·11·13')
    factor_tree(ax, 2026, 3.2, '2026 = 2·1013')
    factor_tree(ax, 9999, 6.4, '9999 = 3²·11·101')
    ax.set_xlim(-1.5, 8); ax.set_ylim(-3.6, .9); ax.axis('off')
    save('03-1')


@fig('03-2')
def _():
    ax = plt.gca()
    for i in range(7):
        for j in range(7):
            ax.scatter(i, j, s=40, color=C1)
            if i < 6: ax.plot([i, i + 1], [j, j], color='#cccccc', lw=.7, zorder=0)
            if j < 6: ax.plot([i, i], [j, j + 1], color='#cccccc', lw=.7, zorder=0)
    ax.set_xlabel('power of 2 (0..6)'); ax.set_ylabel('power of 5 (0..6)'); ax.set_aspect('equal')
    ax.set_title('divisors of 10⁶ = 2⁶·5⁶: a 7×7 grid → 49 divisors')
    save('03-2')


@fig('03-3')
def _():
    ax = plt.gca()
    for n in range(1, 121):
        r, c = (n - 1) // 6, (n - 1) % 6
        ax.add_patch(plt.Rectangle((c, -r), .95, .95, fc='#fde0dd' if isp(n) else 'white', ec='#cccccc'))
        ax.text(c + .47, -r + .47, str(n), ha='center', va='center', fontsize=6.5, color=C2 if isp(n) else 'k')
    ax.set_xlim(0, 6); ax.set_ylim(-20, 1); ax.set_aspect('equal'); ax.axis('off')
    ax.set_title('rows of 6: after 2 and 3, primes appear only in columns 6k+1 and 6k+5')
    plt.gcf().set_size_inches(3.6, 7.2)
    save('03-3')


@fig('03-4')
def _():
    xs = range(3, 3000)
    a = b = 0; A, B = [], []
    for x in xs:
        if isp(x):
            if x % 4 == 1: a += 1
            else: b += 1
        A.append(a); B.append(b)
    ax = plt.gca()
    ax.plot(xs, B, color=C2, label='primes ≡ 3 (mod 4)'); ax.plot(xs, A, color=C1, label='primes ≡ 1 (mod 4)')
    ax.set_xlabel('x'); ax.set_ylabel('count up to x'); ax.legend()
    ax.set_title('both classes keep growing (both are infinite)')
    save('03-4')


@fig('03-5')
def _():
    ax = plt.gca()
    xs = range(80, 115)
    ax.bar(xs, [1] * len(xs), color=[C2 if isp(x) else '#dddddd' for x in xs])
    ax.add_patch(plt.Rectangle((89.5, 0), 7, 1.15, fill=False, ec=C1, lw=2))
    ax.text(93, 1.2, '90..96: seven composites', ha='center', color=C1)
    ax.set_yticks([]); ax.set_xlabel('n (red = prime)'); ax.set_ylim(0, 1.45)
    save('03-5')


@fig('03-6')
def _():
    ax = plt.gca()
    ns = range(2, 32)
    cols = []
    for n in ns:
        M = 2 ** n - 1
        pr = all(M % p for p in range(2, int(M ** .5) + 1)) if n < 32 else False
        cols.append(C2 if pr else (C4 if isp(n) else '#cccccc'))
    ax.bar(ns, [1] * len(ns), color=cols)
    ax.set_yticks([]); ax.set_xlabel('n')
    ax.set_title('2ⁿ−1: red = prime, orange = n prime but 2ⁿ−1 composite, grey = n composite')
    ax.title.set_fontsize(9)
    save('03-6')


# ================= lesson 4 =================
@fig('04-1')
def _():
    fig_, ax = plt.subplots(figsize=(4.2, 4.2))
    power_cycle(ax, 2, 13, 'powers of 2 mod 13: period 12')
    save('04-1')


@fig('04-2')
def _():
    fig_, axs = plt.subplots(1, 2, figsize=(6.6, 3.0))
    axs[0].bar(range(16), [n * n % 4 for n in range(16)], color=C1)
    axs[0].set_title('n² mod 4 ∈ {0, 1}'); axs[0].set_xlabel('n')
    T = np.array([[(a + b) % 4 for a in (0, 1)] for b in (0, 1)])
    axs[1].imshow(T, cmap='Blues', vmin=0, vmax=3)
    for i in range(2):
        for j in range(2):
            axs[1].text(j, i, str(T[i, j]), ha='center', va='center', fontsize=14)
    axs[1].set_xticks([0, 1]); axs[1].set_yticks([0, 1]); axs[1].set_title('x²+y² mod 4: never 3')
    save('04-2')


@fig('04-3')
def _():
    ax = plt.gca()
    xs = range(91)
    ys = [35 * x % 91 for x in xs]
    ax.scatter(xs, ys, s=10, color=C1)
    sol = [x for x in xs if 35 * x % 91 == 14]
    ax.scatter(sol, [14] * len(sol), s=60, color=C2, zorder=3)
    ax.axhline(14, color=C2, lw=.6, ls='--')
    ax.set_xlabel('x'); ax.set_ylabel('35x mod 91'); ax.set_title('35x takes only multiples of 7; value 14 hit 7 times (step 13)')
    save('04-3')


@fig('04-4')
def _():
    ax = plt.gca()
    xs = range(0, 430)
    ax.scatter([x for x in xs if x % 60 == 1], [1] * 8, s=50, color=C1, label='≡ 1 (mod 60)')
    ax.scatter([x for x in xs if x % 7 == 0], [0] * 62, s=8, color=C3, label='multiples of 7')
    ax.axvline(301, color=C2, lw=1); ax.text(305, .5, '301', color=C2)
    ax.set_yticks([]); ax.set_ylim(-.6, 1.6); ax.legend(loc='upper left', fontsize=8); ax.set_xlabel('n')
    save('04-4')


@fig('04-5')
def _():
    ax = plt.gca()
    xs = range(105)
    ys = [x * x % 105 for x in xs]
    ax.scatter(xs, ys, s=8, color=C1)
    sol = [x for x in xs if x * x % 105 == 1]
    ax.scatter(sol, [1] * len(sol), s=60, color=C2, zorder=3)
    for x in sol:
        ax.annotate(str(x), (x, 1), xytext=(0, 8), textcoords='offset points', ha='center', fontsize=7, color=C2)
    ax.set_xlabel('x'); ax.set_ylabel('x² mod 105'); ax.set_title('x² ≡ 1 (mod 105): 2·2·2 = 8 solutions')
    save('04-5')


@fig('04-6')
def _():
    fig_, ax = plt.subplots(figsize=(6.6, 2.8))
    for n in range(2, 15):
        for k, m in enumerate((n - 1, n, n + 1)):
            col = C4 if m % 3 == 0 else (C1 if m % 2 == 0 else '#eeeeee')
            ax.add_patch(plt.Rectangle((n - .45, 2 - k - .45), .9, .9, fc=col))
            ax.text(n, 2 - k, str(m), ha='center', va='center', fontsize=8)
    ax.set_xlim(1.4, 14.6); ax.set_ylim(-.6, 2.6); ax.set_yticks([0, 1, 2]); ax.set_yticklabels(['n+1', 'n', 'n−1'])
    ax.set_xlabel('n'); ax.set_title('n³−n = (n−1)n(n+1): each column has an even number (blue) and a multiple of 3 (orange)', fontsize=8.5)
    save('04-6')

@fig('05-1')
def _():
    fig_, axs = plt.subplots(1, 2, figsize=(6.6, 3.4))
    power_cycle(axs[0], 5, 7, '5^k mod 7: period 6')
    power_cycle(axs[1], 2, 7, '2^k mod 7: period 3')
    save('05-1')


@fig('05-2')
def _():
    ax = plt.gca()
    ns = np.arange(1, 2101)
    ax.scatter(ns, [phi(int(n)) for n in ns], s=1, color=C1)
    ax.plot([1, 2100], [0, 2099], color=GR, lw=.6, label='n − 1 (primes)')
    for n in (97, 1000, 2026):
        ax.scatter([n], [phi(n)], s=60, color=C2, zorder=3)
        ax.annotate(f'φ({n}) = {phi(n)}', (n, phi(n)), xytext=(5, 6), textcoords='offset points', color=C2)
    ax.set_xlabel('n'); ax.legend(fontsize=8)
    save('05-2')


@fig('05-3')
def _():
    p = 11
    T = np.array([[pow(a, k, p) for a in range(1, p)] for k in range(1, p)])
    ax = plt.gca()
    ax.imshow(T, cmap='viridis', origin='lower', extent=(.5, p - .5, .5, p - .5))
    ax.axhline(p - 1, color=C2, lw=2)
    ax.set_xlabel('a'); ax.set_ylabel('exponent k'); ax.set_title('a^k mod 11: the row k = 10 is all 1 (Fermat)')
    save('05-3')


@fig('05-4')
def _():
    ps = [2, 3, 5, 7, 13]
    fig_, axs = plt.subplots(1, 5, figsize=(7.2, 1.9))
    for ax, p in zip(axs, ps):
        ax.scatter(range(p), [pow(n, 13, p) for n in range(p)], s=14, color=C2)
        ax.plot([0, p - 1], [0, p - 1], color=GR, lw=.6)
        ax.set_title(f'n¹³ mod {p}', fontsize=8); ax.set_xticks([]); ax.set_yticks([])
    fig_.suptitle('n¹³ ≡ n for p = 2, 3, 5, 7, 13 (all have p−1 | 12) ⇒ 2730 | n¹³ − n', fontsize=9)
    save('05-4')

@fig('05-5')
def _():
    p = 13
    fig_, ax = plt.subplots(figsize=(4.4, 4.4))
    pts = circle_nodes(ax, p - 1, labels=list(range(1, p)))
    for a in range(1, p):
        b = pow(a, -1, p)
        if a < b:
            ax.plot([pts[a - 1][0], pts[b - 1][0]], [pts[a - 1][1], pts[b - 1][1]], color=C1)
    for a in (1, p - 1):
        ax.scatter(*pts[a - 1], s=120, color=C2, zorder=4)
    ax.set_title("Wilson mod 13: a pairs with a⁻¹; only 1 and 12 are alone")
    save('05-5')


@fig('05-6')
def _():
    fig_, axs = plt.subplots(1, 2, figsize=(6.8, 2.8))
    for ax, (m, e) in zip(axs, ((561, 560), (341, 340))):
        xs = [a for a in range(1, m) if gcd(a, m) == 1]
        ys = [pow(a, e, m) for a in xs]
        ax.scatter(xs, ys, s=4, c=[C3 if y == 1 else C2 for y in ys])
        ax.set_title(f'a^{e} mod {m}: ' + (f'always 1' if all(y == 1 for y in ys) else f'{sum(y==1 for y in ys)} of {len(ys)} give 1'), fontsize=9)
        ax.set_xlabel('a coprime to ' + str(m))
    save('05-6')

@fig('06-1')
def _():
    ax = plt.gca()
    ns = range(1, 50)
    d = [len(divisors(n)) for n in ns]
    ax.bar(ns, d, color=[C2 if x == 6 else '#bbbbbb' for x in d])
    ax.axhline(6, color=C2, lw=.6, ls='--')
    ax.set_xlabel('n'); ax.set_ylabel('d(n)'); ax.set_title('d(n) = 6: n = p⁵ or p²q  (red)')
    save('06-1')


@fig('06-2')
def _():
    ax = plt.gca()
    M = 10000
    sig = [0] * (M + 1)
    for d_ in range(1, M + 1):
        for m in range(d_, M + 1, d_):
            sig[m] += d_
    ns = np.arange(1, M + 1)
    ax.scatter(ns, [sig[n] / n for n in ns], s=.5, color=C1)
    ax.axhline(2, color=C2, lw=.8)
    for n in (6, 28, 496, 8128):
        ax.scatter([n], [2], s=50, color=C2, zorder=3); ax.annotate(str(n), (n, 2), xytext=(0, 8), textcoords='offset points', ha='center', color=C2)
    ax.set_xscale('log'); ax.set_xlabel('n'); ax.set_ylabel('σ(n)/n'); ax.set_title('perfect numbers sit exactly on σ(n)/n = 2')
    save('06-2')


@fig('06-3')
def _():
    ns = np.arange(1, 31)
    fig_, axs = plt.subplots(3, 1, figsize=(6.4, 4.2), sharex=True)
    axs[0].bar(ns, [mu(int(n)) for n in ns], color=C1); axs[0].set_ylabel('μ(n)')
    axs[1].bar(ns, [len(divisors(int(n))) for n in ns], color=C4); axs[1].set_ylabel('d(n)')
    conv = [sum(mu(d_) * len(divisors(int(n) // d_)) for d_ in divisors(int(n))) for n in ns]
    axs[2].bar(ns, conv, color=C2); axs[2].set_ylabel('(μ*d)(n)'); axs[2].set_ylim(0, 1.5)
    axs[2].set_xlabel('n'); axs[0].set_title('μ * d = μ * 1 * 1 = 1')
    save('06-3')


@fig('06-4')
def _():
    ax = plt.gca()
    ns = np.arange(1, 61)
    ax.bar(ns, [sum(abs(mu(d_)) for d_ in divisors(int(n))) for n in ns], color=C1, label='Σ|μ(d)|')
    ax.plot(ns, [2 ** len(factor(int(n))) for n in ns], 'o', color=C2, ms=4, label='2^ω(n)')
    ax.set_xlabel('n'); ax.legend(); ax.set_title('the two functions agree')
    save('06-4')


@fig('06-5')
def _():
    fig_, ax = plt.subplots(figsize=(5.2, 3.6))
    pos = {1: (0, 0), 2: (-1, 1), 3: (1, 1), 4: (-2, 2), 6: (0, 2), 12: (-1, 3)}
    sig = lambda n: sum(divisors(n))
    for a in pos:
        for b in pos:
            if b % a == 0 and b != a and isp(b // a):
                ax.plot(*zip(pos[a], pos[b]), color='#cccccc', zorder=0)
    for n, (x, y) in pos.items():
        v = mu(n) * sig(n)
        ax.scatter(x, y, s=500, color=C2 if v > 0 else (C1 if v < 0 else '#eeeeee'), zorder=2)
        ax.text(x, y, str(n), ha='center', va='center', fontsize=10)
        ax.text(x + .28, y - .05, f'μσ={v}', fontsize=8)
    ax.axis('off'); ax.set_title('divisors of 12:  1 − 3 − 4 + 12 = 6 = (1−3)(1−4)')
    save('06-5')


@fig('06-6')
def _():
    fig_, axs = plt.subplots(1, 2, figsize=(6.8, 3.3))
    ax = axs[0]
    for a in range(12):
        z = cmath.exp(2j * pi * a / 12)
        prim = gcd(a, 12) == 1
        ax.scatter(z.real, z.imag, s=70 if prim else 25, color=C2 if prim else GR, zorder=3)
        ax.annotate(str(a), (z.real * 1.18, z.imag * 1.18), ha='center', va='center', fontsize=8)
    ax.add_patch(plt.Circle((0, 0), 1, fill=False, color='#dddddd')); ax.set_aspect('equal'); ax.axis('off')
    ax.set_title('12th roots of unity\n(red = primitive: a = 1,5,7,11)', fontsize=9)
    c = lambda n: round(sum(cmath.exp(2j * pi * a * n / 12) for a in (1, 5, 7, 11)).real)
    ns = range(1, 25)
    axs[1].bar(ns, [c(n) for n in ns], color=C1); axs[1].axhline(0, color='k', lw=.5)
    axs[1].set_xlabel('n'); axs[1].set_title('c₁₂(n): integer values, period 12', fontsize=9)
    save('06-6')


# ================= lesson 7 =================
@fig('07-1')
def _():
    fig_, ax = plt.subplots(figsize=(4.2, 4.2))
    power_cycle(ax, 2, 13, '2 generates all 12 non-zero residues mod 13')
    save('07-1')


@fig('07-2')
def _():
    ps = [p for p in PR if 5 <= p < 250]
    rows = [('(−1/p)', lambda p: legendre(-1, p)), ('(2/p)', lambda p: legendre(2, p)), ('(3/p)', lambda p: legendre(3, p))]
    T = np.array([[f(p) for p in ps] for _, f in rows])
    ax = plt.gca(); plt.gcf().set_size_inches(6.8, 2.6)
    ax.imshow(T, cmap='coolwarm_r', aspect='auto', vmin=-1, vmax=1)
    ax.set_yticks(range(3)); ax.set_yticklabels([r[0] for r in rows])
    ax.set_xticks(range(0, len(ps), 6)); ax.set_xticklabels([ps[i] for i in range(0, len(ps), 6)], fontsize=7)
    k = ps.index(97); ax.axvline(k, color='k', lw=1.5)
    ax.set_title('blue = +1, red = −1 for primes p; black line: p = 97 (all three are +1)')
    save('07-2')


@fig('07-3')
def _():
    p = 1009
    sq = sorted({x * x % p for x in range(1, p)})
    ax = plt.gca(); plt.gcf().set_size_inches(6.6, 2.2)
    ax.scatter(sq, [0] * len(sq), s=3, color=C1, marker='|')
    ax.scatter([150], [0], s=120, color=C2, marker='v', zorder=3); ax.text(150, .25, '150', color=C2, ha='center')
    ax.set_yticks([]); ax.set_ylim(-.5, .6); ax.set_xlabel('the 504 quadratic residues mod 1009 (150 is one of them)')
    save('07-3')


@fig('07-4')
def _():
    ax = plt.gca()
    ns = range(1, 13)
    vals = [n * n + 1 for n in ns]
    for n, v in zip(ns, vals):
        fs = factor(v)
        ok = all(p == 2 or p % 4 == 1 for p in fs)
        ax.bar(n, v, color=C3 if ok else C2)
        ax.text(n, v + 3, '·'.join(str(p) for p in sorted(fs)), ha='center', fontsize=7, rotation=90)
    ax.set_xlabel('m'); ax.set_ylabel('m² + 1'); ax.set_ylim(0, 190)
    ax.set_title('odd prime factors of m²+1 are always ≡ 1 (mod 4)')
    save('07-4')


@fig('07-5')
def _():
    p = 19
    ax = plt.gca()
    xs = range(p)
    ax.scatter(xs, [x * x % p for x in xs], color=C1)
    for x in (9, 10):
        ax.scatter([x], [5], s=90, color=C2, zorder=3)
    ax.axhline(5, color=C2, ls='--', lw=.6)
    ax.set_xlabel('x'); ax.set_ylabel('x² mod 19'); ax.set_title('5^((19+1)/4) = 5⁵ ≡ 9, and 9² = 81 ≡ 5;  also −9 = 10')
    save('07-5')


@fig('07-6')
def _():
    chain = [(1001, 9907), (898, 1001), (449, 1001), (103, 449), (37, 103), (29, 37), (8, 29), (2, 29)]
    ax = plt.gca()
    ax.plot(range(len(chain)), [b for _, b in chain], 'o-', color=C1, label='bottom (n)')
    ax.plot(range(len(chain)), [a for a, _ in chain], 's-', color=C4, label='top (a)')
    for i, (a, b) in enumerate(chain):
        ax.annotate(f'({a}/{b})', (i, b), xytext=(4, 6), textcoords='offset points', fontsize=7)
    ax.set_yscale('log'); ax.set_xlabel('step'); ax.legend(fontsize=8)
    ax.set_title('Jacobi reciprocity shrinks the numbers like Euclid — no factoring needed')
    save('07-6')


# ================= lesson 8 =================
@fig('08-1')
def _():
    fig_, axs = plt.subplots(1, 4, figsize=(7.2, 2.4))
    for ax, (a, b, c), col in zip(axs, [(15, 8, 17), (15, 20, 25), (15, 36, 39), (15, 112, 113)], [C1, C3, C4, C2]):
        ax.add_patch(plt.Polygon([(0, 0), (b, 0), (0, a)], alpha=.35, color=col))
        ax.text(b / 2, -.08 * max(a, b), str(b), ha='center', fontsize=8); ax.text(-.04 * max(a, b), a / 2, '15', ha='right', fontsize=8)
        ax.text(b / 2, a / 2, str(c), fontsize=8)
        ax.set_xlim(-.2 * b, b * 1.05); ax.set_ylim(-.15 * max(a, b), max(a, b) * .9); ax.set_aspect('equal'); ax.axis('off')
    fig_.suptitle('leg 15: (z−y)(z+y) = 225 = 1·225 = 3·75 = 5·45 = 9·25', fontsize=9)
    save('08-1')

@fig('08-2')
def _():
    fig_, axs = plt.subplots(1, 2, figsize=(6.6, 3.2))
    T = np.array([[(x * x + y * y) % 3 for x in range(3)] for y in range(3)])
    axs[0].imshow(T, cmap='Blues', vmin=0, vmax=2)
    for i in range(3):
        for j in range(3):
            axs[0].text(j, i, str(T[i, j]), ha='center', va='center', fontsize=13)
    axs[0].set_xlabel('x mod 3'); axs[0].set_ylabel('y mod 3'); axs[0].set_title('x²+y² mod 3: 0 only at (0,0)', fontsize=9)
    t = np.linspace(0, 2 * pi, 300)
    r = sqrt(3)
    axs[1].plot(r * np.cos(t), r * np.sin(t), color=C1)
    X, Y = np.meshgrid(np.arange(-2, 2.01, .25), np.arange(-2, 2.01, .25))
    axs[1].scatter(X, Y, s=3, color=GR)
    axs[1].set_aspect('equal'); axs[1].set_title('x²+y² = 3 has no rational point', fontsize=9)
    save('08-2')


@fig('08-3')
def _():
    ax = plt.gca(); plt.gcf().set_size_inches(4.4, 4.4)
    R = sqrt(221)
    t = np.linspace(0, 2 * pi, 400)
    ax.plot(R * np.cos(t), R * np.sin(t), color=C1)
    pts = [(x, y) for x in range(-15, 16) for y in range(-15, 16) if x * x + y * y == 221]
    ax.scatter(*zip(*pts), color=C2, s=30, zorder=3)
    for (x, y) in [(10, 11), (5, 14)]:
        ax.annotate(f'({x},{y})', (x, y), xytext=(4, 4), textcoords='offset points', fontsize=8)
    ax.set_aspect('equal'); ax.grid(alpha=.3); ax.set_title('x² + y² = 221: 16 lattice points (2 essentially different)', fontsize=9)
    save('08-3')


@fig('08-4')
def _():
    ax = plt.gca()
    def bad(n):
        while n % 4 == 0:
            n //= 4
        return n % 8 == 7
    ns = range(1, 141)
    ax.bar(ns, [1] * 140, color=[C2 if bad(n) else '#dddddd' for n in ns], width=1)
    for n in (60, 71, 112, 135):
        ax.text(n, 1.05, str(n), ha='center', fontsize=8, color=C2)
    ax.set_yticks([]); ax.set_ylim(0, 1.3); ax.set_xlabel('n (red: 4^a(8b+7), not a sum of three squares)')
    save('08-4')


@fig('08-5')
def _():
    ax = plt.gca()
    xs = np.linspace(1, 30, 400)
    ax.plot(xs, np.sqrt((xs ** 2 - 1) / 3), color=C1, label='x² − 3y² = 1')
    ax.plot(-xs, np.sqrt((xs ** 2 - 1) / 3), color=C1)
    pts = [(2, 1), (7, 4), (26, 15)]
    ax.scatter(*zip(*pts), color=C2, zorder=3, s=40)
    for p in pts:
        ax.annotate(str(p), p, xytext=(5, -10), textcoords='offset points', fontsize=8)
    X, Y = np.meshgrid(range(0, 31), range(0, 18))
    ax.scatter(X, Y, s=2, color=GR)
    ax.set_xlim(0, 30); ax.set_ylim(0, 17); ax.set_title('(2+√3)^k: (2,1) → (7,4) → (26,15)')
    save('08-5')


@fig('08-6')
def _():
    ax = plt.gca()
    xs = np.linspace(0, 20, 400)
    ax.plot(xs, np.sqrt((xs ** 2 + 1) / 3), color=C2, label='x² − 3y² = −1 (no lattice points)')
    ax.plot(xs[xs >= 1], np.sqrt((xs[xs >= 1] ** 2 - 1) / 3), color=C1, label='x² − 3y² = 1')
    X, Y = np.meshgrid(range(0, 21), range(0, 13))
    ax.scatter(X, Y, s=3, color=GR)
    ax.legend(fontsize=8); ax.set_title('mod 3: x² ≡ −1 ≡ 2 is impossible')
    save('08-6')


# ================= lesson 9 =================
@fig('09-1')
def _():
    ax = plt.gca(); plt.gcf().set_size_inches(4.6, 4.2)
    x = 10
    for a in range(1, 11):
        for b in range(1, 11):
            if a * b <= x:
                ax.scatter(a, b, color=C1, s=30)
    t = np.linspace(1, 10, 200); ax.plot(t, x / t, color=C2)
    for a in range(1, 11):
        ax.text(a, -.2, str(x // a), ha='center', fontsize=8, color=C3)
    ax.set_xlim(0, 10.5); ax.set_ylim(-.6, 10.5); ax.set_aspect('equal')
    ax.set_title('27 lattice points under ab = 10\ncolumns: ⌊10/a⌋, rows: d(n)', fontsize=9)
    save('09-1')


@fig('09-2')
def _():
    M = 100000
    om = [0] * (M + 1)
    for p in PR:
        if p > M: break
        for m in range(p, M + 1, p):
            om[m] += 1
    ns = np.arange(2, M + 1)
    ax = plt.gca()
    idx = np.random.default_rng(1).choice(len(ns), 4000, replace=False)
    ax.scatter(ns[idx], [om[n] for n in ns[idx]], s=2, color=C1, alpha=.4)
    avg = np.cumsum([om[n] for n in ns]) / (ns - 1)
    ax.plot(ns, avg, color=C2, label='average of ω up to x')
    ax.plot(ns, np.log(np.log(ns)) + 1.03, color=C4, ls='--', label='log log x + 1.03')
    ax.set_xscale('log'); ax.legend(fontsize=8); ax.set_xlabel('n'); ax.set_ylabel('ω(n)')
    save('09-2')


@fig('09-3')
def _():
    M = 5000
    ph = list(range(M + 1))
    for p in PR:
        if p > M: break
        for m in range(p, M + 1, p):
            ph[m] -= ph[m] // p
    xs = np.arange(1, M + 1)
    S = np.cumsum([ph[n] / n for n in xs])
    ax = plt.gca()
    ax.plot(xs, S - 6 / pi ** 2 * xs, color=C1, label='Σ φ(n)/n − (6/π²)x')
    ax.plot(xs, np.log(xs), color=GR, ls='--', label='± log x')
    ax.plot(xs, -np.log(xs), color=GR, ls='--')
    ax.legend(fontsize=8); ax.set_xlabel('x'); ax.set_title('the error stays within O(log x)')
    save('09-3')


@fig('09-4')
def _():
    def g(n):
        best = 1
        def rec(rem, start, cur):
            nonlocal best
            best = max(best, cur)
            for q in range(start, rem + 1):
                if isp(q):
                    pk = q
                    while pk <= rem:
                        rec(rem - pk, q + 1, cur * pk); pk *= q
        rec(n, 2, 1)
        return best
    ns = range(1, 41)
    gs = [g(n) for n in ns]
    ax = plt.gca()
    ax.step(ns, np.log(gs), where='post', color=C1, label='log g(n)')
    ax.plot(ns, [sqrt(n * log(n)) if n > 1 else 0 for n in ns], color=C2, ls='--', label='√(n log n)')
    for n in (7, 12):
        ax.scatter([n], [log(gs[n - 1])], color=C4, zorder=3); ax.annotate(f'g({n})={gs[n-1]}', (n, log(gs[n - 1])), xytext=(4, -12), textcoords='offset points', fontsize=8)
    ax.legend(fontsize=8); ax.set_xlabel('n')
    save('09-4')


@fig('09-5')
def _():
    u = np.linspace(0, 6, 601)
    rho = np.ones_like(u)
    h = u[1] - u[0]
    for i, x in enumerate(u):
        if x > 1:
            j = int(round((x - 1) / h))
            rho[i] = rho[i - 1] - h * rho[j] / x
    ax = plt.gca()
    ax.plot(u, rho, color=C1)
    ax.scatter([3], [rho[300]], color=C2, zorder=3); ax.annotate(f'ρ(3) ≈ {rho[300]:.3f}', (3, rho[300]), xytext=(8, 10), textcoords='offset points', color=C2)
    ax.set_yscale('log'); ax.set_xlabel('u'); ax.set_ylabel('ρ(u)'); ax.set_title("Dickman: share of n ≤ x with all prime factors ≤ x^(1/u)")
    save('09-5')


# ================= lesson 10 =================
@fig('10-1')
def _():
    fig_, axs = plt.subplots(1, 2, figsize=(6.6, 3.0))
    for ax, p in zip(axs, (3, 5)):
        terms = []
        k = p
        while k <= 1000:
            terms.append(1000 // k); k *= p
        ax.bar(range(1, len(terms) + 1), terms, color=C1)
        for i, t in enumerate(terms):
            ax.text(i + 1, t + 5, str(t), ha='center', fontsize=8)
        ax.set_title(f'⌊1000/{p}^j⌋ : total {sum(terms)}', fontsize=9); ax.set_xlabel('j')
    save('10-1')


@fig('10-2')
def _():
    ax = plt.gca()
    ns = range(1, 70)
    v = []
    for n in ns:
        c, e = comb(2 * n, n), 0
        while c % 2 == 0:
            c //= 2; e += 1
        v.append(e)
    ax.bar(ns, v, color=[C2 if e == 1 else C1 for e in v])
    ax.set_xlabel('n'); ax.set_ylabel('power of 2 in C(2n,n)')
    ax.set_title('= number of 1s in binary n; equals 1 exactly at n = 1,2,4,8,16,32,64')
    save('10-2')


@fig('10-3')
def _():
    ax = plt.gca()
    n = 12
    ps = [p for p in PR if p <= n]
    ex = []
    for p in ps:
        e, k = 0, p
        while k <= n:
            e += n // k; k *= p
        ex.append(e)
    ax.bar([str(p) for p in ps], ex, color=[C2 if p > n / 2 else C1 for p in ps])
    ax.set_xlabel('prime p'); ax.set_ylabel(f'exponent of p in {n}!')
    ax.set_title('12!: 7 and 11 (primes in (6, 12]) appear once → odd exponent → not a square')
    ax.title.set_fontsize(9)
    save('10-3')


@fig('10-4')
def _():
    ax = plt.gca(); plt.gcf().set_size_inches(5.4, 4.0)
    col = {2: '#c6dbef', 3: '#fdd0a2', 5: '#c7e9c0', 7: '#dadaeb'}
    for n in range(1, 51):
        r, c = (n - 1) // 10, (n - 1) % 10
        p = next((q for q in (2, 3, 5, 7) if n % q == 0 and n != q), None)
        ax.add_patch(plt.Rectangle((c, -r), .95, .95, fc=col[p] if p else ('#fde0dd' if isp(n) else 'white'), ec='#bbbbbb'))
        ax.text(c + .47, -r + .47, str(n), ha='center', va='center', fontsize=8, color=C2 if isp(n) else 'k')
    ax.set_xlim(0, 10); ax.set_ylim(-4, 1); ax.set_aspect('equal'); ax.axis('off')
    ax.set_title('sieve to 50: struck by 2, 3, 5, 7 (coloured); 15 primes (red) remain')
    save('10-4')


@fig('10-5')
def _():
    xs = np.arange(2, 20001)
    lam = np.zeros(20001)
    for p in PR:
        if p > 20000: break
        k = p
        while k <= 20000:
            lam[k] = log(p); k *= p
    psi = np.cumsum(lam)[2:]
    ax = plt.gca()
    ax.plot(xs, psi / xs, color=C1, label='ψ(x)/x')
    ax.axhline(log(2), color=C2, ls='--', label='log 2 (lower bound)')
    ax.axhline(2 * log(2), color=C4, ls='--', label='2 log 2 (upper bound)')
    ax.set_xscale('log'); ax.legend(fontsize=8); ax.set_xlabel('x')
    save('10-5')


# ================= lesson 11 =================
@fig('11-1')
def _():
    ns = np.arange(1, 41)
    ax = plt.gca()
    ax.bar(ns - .2, [2 ** len(factor(int(n))) for n in ns], width=.4, color=C1, label='2^ω(n)')
    ax.bar(ns + .2, [len(divisors(int(n) ** 2)) for n in ns], width=.4, color=C4, label='d(n²)')
    ax.set_xlabel('n'); ax.legend(); ax.set_title('Dirichlet series: ζ(s)²/ζ(2s) and ζ(s)³/ζ(2s)')
    save('11-1')


@fig('11-2')
def _():
    M = 20000
    sf = np.array([1 if mu(n) != 0 else 0 for n in range(1, M + 1)])
    xs = np.arange(1, M + 1)
    ax = plt.gca()
    ax.plot(xs, np.cumsum(sf) / xs, color=C1, label='share of square-free n ≤ x')
    ax.axhline(6 / pi ** 2, color=C2, ls='--', label='6/π² ≈ 0.6079')
    ax.set_xscale('log'); ax.legend(); ax.set_xlabel('x')
    save('11-2')


@fig('11-3')
def _():
    ks = np.arange(1, 31)
    ax = plt.gca()
    ax.plot(ks, np.cumsum([(-1) ** (k + 1) / k ** 2 for k in ks]), 'o-', ms=3, color=C1, label='partial sums of η(2)')
    ax.axhline(pi ** 2 / 12, color=C1, ls='--')
    ax.plot(ks, np.cumsum([1 / k ** 6 for k in ks]), 's-', ms=3, color=C4, label='partial sums of ζ(6)')
    ax.axhline(pi ** 6 / 945, color=C4, ls='--')
    ax.legend(); ax.set_xlabel('number of terms'); ax.set_title('η(2) = π²/12,   ζ(6) = π⁶/945')
    save('11-3')


@fig('11-4')
def _():
    fig_, ax = plt.subplots(figsize=(6.4, 3.0))
    sq = [1 / k ** 2 for k in range(1, 9)]
    left = 0
    for k, v in enumerate(sq, 1):
        ax.barh(0, v, left=left, color=C2 if k % 2 else C1, ec='w'); left += v
    ax.text(0.02, .45, 'odd k (red): total π²/8 = 3/4 of ζ(2);  even k (blue): 1/4 of ζ(2)', fontsize=8)
    ax.axvline(pi ** 2 / 6, color='k', ls='--'); ax.text(pi ** 2 / 6, -.55, 'ζ(2)', ha='center')
    ax.set_yticks([]); ax.set_ylim(-.7, .7); ax.set_xlabel('1 + 1/4 + 1/9 + ...')
    save('11-4')


@fig('11-5')
def _():
    Ns = np.arange(1, 400)
    H = np.cumsum(1 / Ns)
    ax = plt.gca()
    ax.plot(Ns, H - np.log(Ns), color=C1, label='H_N − log N')
    ax.axhline(0.5772156649, color=C2, ls='--', label='γ ≈ 0.5772')
    ax.set_xscale('log'); ax.legend(); ax.set_xlabel('N')
    save('11-5')


# ================= lesson 12 =================
@fig('12-1')
def _():
    ns = np.arange(10, 100000)
    ax = plt.gca()
    pn = np.array(PR[9:99999], dtype=float)
    ax.plot(ns, pn / (ns * np.log(ns)), color=C1, label='p_n / (n log n)')
    ax.plot(ns, pn / (ns * (np.log(ns) + np.log(np.log(ns)) - 1)), color=C3, label='p_n / (n(log n + log log n − 1))')
    ax.axhline(1, color='k', lw=.6)
    ax.set_xscale('log'); ax.legend(fontsize=8); ax.set_xlabel('n')
    save('12-1')


@fig('12-2')
def _():
    from mpmath import zetazero
    zs = [float(zetazero(k).imag) for k in range(1, 30)]
    T = np.linspace(5, 100, 800)
    ax = plt.gca()
    ax.step(zs + [100], list(range(1, 30)) + [29], where='post', color=C1, label='N(T) (actual zeros)')
    smooth = T / (2 * pi) * np.log(T / (2 * pi)) - T / (2 * pi) + 7 / 8
    ax.plot(T, smooth, color=C2, label='T/2π log(T/2π) − T/2π + 7/8')
    ax.set_xlabel('T'); ax.legend(fontsize=8); ax.set_title('N(100) = 29; the formula gives 29.00')
    save('12-2')


@fig('12-3')
def _():
    t = np.linspace(-pi, pi, 400)
    ax = plt.gca()
    ax.plot(t, 3 + 4 * np.cos(t) + np.cos(2 * t), color=C1, label='3 + 4cos θ + cos 2θ = 2(1+cos θ)²')
    ax.plot(t, 1 + np.cos(t), color=C4, label='1 + cos θ')
    ax.axhline(0, color='k', lw=.6); ax.legend(fontsize=8); ax.set_xlabel('θ')
    save('12-3')


@fig('12-4')
def _():
    M = 10000
    ms = np.array([mu(n) for n in range(1, M + 1)])
    Mx = np.cumsum(ms)
    xs = np.arange(1, M + 1)
    ax = plt.gca()
    ax.plot(xs, Mx, color=C1, lw=.7, label='M(x) = det A_x')
    ax.plot(xs, np.sqrt(xs), color=C2, ls='--', label='±√x'); ax.plot(xs, -np.sqrt(xs), color=C2, ls='--')
    ax.scatter([6], [Mx[5]], color=C4, zorder=3)
    ax.set_xscale('log'); ax.legend(fontsize=8); ax.set_xlabel('x'); ax.set_title('M(6) = −1')
    save('12-4')


@fig('12-5')
def _():
    x = np.logspace(0, 4, 2000)
    ax = plt.gca()
    ax.plot(x, np.cos(14.134725 * np.log(x)), color=C1)
    for k in range(0, 21):
        ax.axvline(np.exp(2 * pi * k / 14.134725), color='#eeeeee', lw=.8, zorder=0)
    ax.set_xscale('log'); ax.set_xlabel('x (log scale)')
    ax.set_title('wave of the first zero: period 2π/14.13 ≈ 0.4445 in log x (x × 1.56 per cycle)')
    ax.title.set_fontsize(9)
    save('12-5')


# ================= lesson 13 =================
@fig('13-1')
def _():
    T = np.array([[1, 1, 1, 1], [1, -1, 1, -1], [1, -1, -1, 1], [1, 1, -1, -1]])
    ax = plt.gca(); plt.gcf().set_size_inches(4.4, 3.4)
    ax.imshow(T, cmap='coolwarm_r', vmin=-1, vmax=1)
    for i in range(4):
        for j in range(4):
            ax.text(j, i, f'{T[i, j]:+d}', ha='center', va='center')
    ax.set_xticks(range(4)); ax.set_xticklabels(['1', '3', '5', '7'])
    ax.set_yticks(range(4)); ax.set_yticklabels(['χ₀', 'χ₄', '(2/·)', '(−2/·)'])
    ax.set_title('characters mod 8: all values ±1')
    save('13-1')


@fig('13-2')
def _():
    chi = {0: 0, 1: 1, 2: -1, 3: -1, 4: 1}
    ns = np.arange(1, 201)
    ax = plt.gca()
    ax.plot(ns, np.cumsum([chi[n % 5] / n for n in ns]), color=C1, label='partial sums of L(1, (·/5))')
    ax.axhline(2 / sqrt(5) * log((1 + sqrt(5)) / 2), color=C2, ls='--', label='(2/√5) log φ ≈ 0.4304')
    ax.legend(fontsize=8); ax.set_xlabel('number of terms')
    save('13-2')


@fig('13-3')
def _():
    ps = [p for p in PR if 3 < p < 2000 and p % 4 == 3]
    hs = [-sum(a * legendre(a, p) for a in range(1, p)) // p for p in ps]
    ax = plt.gca()
    ax.scatter(ps, hs, s=8, color=C1)
    for p, h in zip(ps, hs):
        if p in (11, 47, 163):
            ax.scatter([p], [h], s=50, color=C2, zorder=3); ax.annotate(f'h(−{p})={h}', (p, h), xytext=(5, 5), textcoords='offset points', fontsize=8, color=C2)
    xs = np.linspace(7, 2000, 200); ax.plot(xs, np.sqrt(xs) / pi, color=GR, ls='--', label='√p / π')
    ax.legend(fontsize=8); ax.set_xlabel('p ≡ 3 (mod 4)'); ax.set_ylabel('class number h(−p)')
    save('13-3')


@fig('13-4')
def _():
    xs, S, s = [], [], 0
    for p in PR:
        if p > 200000: break
        if p > 2:
            s += (1 if p % 4 == 1 else -1) / p
            xs.append(p); S.append(s)
    ax = plt.gca()
    ax.plot(xs, S, color=C1)
    ax.set_xscale('log'); ax.set_xlabel('x'); ax.set_ylabel('Σ χ₄(p)/p')
    ax.set_title('the difference settles down (converges), because L(1, χ₄) = π/4 ≠ 0')
    save('13-4')


@fig('13-5')
def _():
    ns = range(0, 22)
    vals = [n * n + n + 17 for n in ns]
    ax = plt.gca()
    ax.bar(ns, vals, color=[C3 if isp(v) else C2 for v in vals])
    ax.annotate('289 = 17²', (16, 289), xytext=(-60, 20), textcoords='offset points', arrowprops=dict(arrowstyle='->'), color=C2)
    ax.set_xlabel('n'); ax.set_ylabel('n² + n + 17'); ax.set_title('green = prime: n = 0..15 (discriminant −67, h = 1)')
    save('13-5')


# ================= lesson 14 =================
@fig('14-1')
def _():
    ax = plt.gca(); plt.gcf().set_size_inches(6.4, 4.0)
    for n in range(1, 201):
        r, c = (n - 1) // 20, (n - 1) % 20
        keep = n % 2 and n % 3 and n % 7
        ax.add_patch(plt.Rectangle((c, -r), .95, .95, fc='#2ca02c' if keep else '#eeeeee'))
    ax.set_xlim(0, 20); ax.set_ylim(-9, 1); ax.set_aspect('equal'); ax.axis('off')
    ax.set_title('n ≤ 200 not divisible by 2, 3, 7 (green): 58  (expected 200·½·⅔·⁶⁄₇ ≈ 57.1)')
    save('14-1')


@fig('14-2')
def _():
    ps = [p for p in PR if p < 110]
    w = [sum(1 for n in range(p) if (n * n + 1) % p == 0) for p in ps]
    ax = plt.gca()
    ax.bar([str(p) for p in ps], w, color=[C1 if p % 4 == 1 else (C2 if p % 4 == 3 else GR) for p in ps])
    ax.tick_params(axis='x', labelsize=7, rotation=90)
    ax.set_ylabel('w(p) = #roots of n²+1 mod p'); ax.set_title('2 roots when p ≡ 1 (mod 4) (blue), none when p ≡ 3 (red)')
    save('14-2')


@fig('14-3')
def _():
    k = 7
    ts = range(0, k + 1)
    ax = plt.gca()
    ax.plot(ts, [sum((-1) ** j * comb(k, j) for j in range(t + 1)) for t in ts], 'o-', color=C1, label='Σ_{j≤t} (−1)^j C(7, j)')
    ax.axhline(0, color='k', lw=.6)
    ax.set_xlabel('truncation t'); ax.legend(); ax.set_title('even t: ≥ 0 (upper bound);  odd t: ≤ 0 (lower bound)')
    save('14-3')


@fig('14-4')
def _():
    from mpmath import quad, log as mlog
    xs = np.logspace(2, 6, 40)
    tw = np.cumsum([1 if (isp(n) and isp(n + 2)) else 0 for n in range(1, 1_000_001)])
    C2c = 0.6601618158
    pred = [2 * C2c * float(quad(lambda t: 1 / mlog(t) ** 2, [2, x])) for x in xs]
    ax = plt.gca()
    ax.plot(xs, [tw[int(x) - 1] for x in xs], 'o', ms=3, color=C1, label='twin pairs up to x (actual)')
    ax.plot(xs, pred, color=C2, label='2C₂ ∫ dt/log²t')
    ax.set_xscale('log'); ax.set_yscale('log'); ax.legend(fontsize=8); ax.set_xlabel('x')
    save('14-4')


@fig('14-5')
def _():
    xs = np.logspace(3, 6, 30)
    tw = np.cumsum([1 if (isp(n) and isp(n + 2)) else 0 for n in range(1, 1_000_001)])
    C2c = 0.6601618158
    ax = plt.gca()
    ax.plot(xs, [8 * C2c * x / log(x) ** 2 / tw[int(x) - 1] for x in xs], 'o-', ms=3, color=C1, label='Selberg bound / actual')
    ax.plot(xs, [2 * C2c * x / log(x) ** 2 / tw[int(x) - 1] for x in xs], 's-', ms=3, color=C3, label='2C₂x/log²x / actual')
    ax.set_xscale('log'); ax.legend(fontsize=8); ax.set_xlabel('x'); ax.set_title('the sieve bound is about 4 times too big')
    save('14-5')


# ================= lesson 15 =================
@fig('15-1')
def _():
    p = 7
    fig_, ax = plt.subplots(figsize=(4.4, 4.2))
    tot = 0
    for x in range(1, p):
        z = cmath.exp(2j * pi * ((x + pow(x, -1, p)) % p) / p)
        ax.annotate('', xy=(tot + z).real if False else ((tot + z).real, (tot + z).imag), xytext=(tot.real, tot.imag) if tot else (0, 0),
                    arrowprops=dict(arrowstyle='->', color=C1))
        tot += z
    ax.scatter([tot.real], [tot.imag], color=C2, s=60, zorder=3)
    ax.annotate(f'K(1,1;7) ≈ {tot.real:.3f}', (tot.real, tot.imag), xytext=(8, -14), textcoords='offset points', color=C2)
    ax.add_patch(plt.Circle((0, 0), 2 * sqrt(p), fill=False, ls='--', color=GR))
    ax.set_xlim(-5.6, 5.6); ax.set_ylim(-5.6, 5.6); ax.set_aspect('equal'); ax.axhline(0, color='#eeeeee'); ax.axvline(0, color='#eeeeee')
    ax.set_title('walk of the 6 terms; circle radius 2√7 (Weil bound)', fontsize=9)
    save('15-1')


@fig('15-2')
def _():
    rng = np.random.default_rng(3)
    a = rng.normal(size=12) + 1j * rng.normal(size=12)
    al = np.linspace(0, 1, 2000)
    S = np.array([sum(a[n] * np.exp(2j * pi * (n + 1) * t) for n in range(12)) for t in al])
    ax = plt.gca()
    ax.fill_between(al, np.abs(S) ** 2, color=C1, alpha=.4)
    ax.axhline(np.sum(np.abs(a) ** 2), color=C2, ls='--', label=f'Σ|aₙ|² = {np.sum(np.abs(a)**2):.1f} = average height')
    ax.set_xlabel('α'); ax.set_ylabel('|S(α)|²'); ax.legend(fontsize=8); ax.set_title('Parseval: area under |S|² on [0,1] = Σ|aₙ|²')
    save('15-2')


@fig('15-3')
def _():
    fig_, ax = plt.subplots(figsize=(6.6, 2.0))
    left = 0
    for v, c in [(16, C1)] * 4 + [(1, C4)] * 15:
        ax.barh(0, v, left=left, color=c, ec='w'); left += v
    ax.text(32, .5, '4 × 16', ha='center'); ax.text(71.5, .5, '15 × 1', ha='center')
    ax.set_xlim(0, 80); ax.set_yticks([]); ax.set_ylim(-.6, .8); ax.set_xlabel('79 = 4·2⁴ + 15·1⁴ (19 fourth powers; 3⁴ = 81 > 79)')
    save('15-3')


@fig('15-4')
def _():
    M = 400
    ps = [p for p in PR if 2 < p < M]
    cnt = np.zeros(M)
    for i, p in enumerate(ps):
        for q in ps[i:]:
            for r in ps[ps.index(q):]:
                if p + q + r < M:
                    cnt[p + q + r] += 1
    ns = np.arange(M)
    ax = plt.gca()
    ax.scatter(ns[ns % 2 == 1], cnt[ns % 2 == 1], s=4, color=C1, label='N odd')
    ax.scatter(ns[ns % 2 == 0], cnt[ns % 2 == 0], s=4, color=C2, label='N even (always 0)')
    ax.legend(fontsize=8); ax.set_xlabel('N'); ax.set_ylabel('# N = p+q+r, odd primes p ≤ q ≤ r')
    save('15-4')


@fig('15-5')
def _():
    ns = range(4, 1001, 2)
    r = [sum(1 for p in PR if p <= n // 2 and isp(n - p)) for n in ns]
    ax = plt.gca()
    ax.scatter(ns, r, s=4, color=C1)
    ax.scatter([60], [r[(60 - 4) // 2]], s=60, color=C2, zorder=3); ax.annotate('60: 6 ways', (60, 6), xytext=(10, 20), textcoords='offset points', color=C2)
    ax.set_xlabel('even n'); ax.set_ylabel('# n = p + q, p ≤ q'); ax.set_title("Goldbach's comet")
    save('15-5')


# ================= lesson 16 =================
@fig('16-1')
def _():
    fig_, axs = plt.subplots(1, 3, figsize=(6.8, 2.4))
    for ax, (pat, q) in zip(axs, [((0, 2, 4), 3), ((0, 2, 6, 8), 3), ((0, 2, 6, 8), 5)]):
        hit = {h % q for h in pat}
        for r in range(q):
            ax.add_patch(plt.Rectangle((r, 0), .9, .9, fc=C2 if r in hit else C3))
            ax.text(r + .45, .45, str(r), ha='center', va='center', color='w')
        ax.set_xlim(0, q); ax.set_ylim(0, 1); ax.axis('off')
        ax.set_title(f'{pat} mod {q}: ' + ('covers all!' if len(hit) == q else 'a class is free'), fontsize=8)
    save('16-1')


@fig('16-2')
def _():
    hs = [2, 4, 6, 8, 10, 12, 30]
    cnt = [sum(1 for p in PR if p < 1_000_000 and isp(p + h)) for h in hs]
    def corr(h):
        c = 1.0
        for p in factor(h):
            if p > 2: c *= (p - 1) / (p - 2)
        return c
    ax = plt.gca()
    ax.bar([str(h) for h in hs], cnt, color=C1, label='pairs (p, p+h), p < 10⁶')
    ax.plot([str(h) for h in hs], [cnt[0] * corr(h) for h in hs], 'o', color=C2, label='predicted: × Π (p−1)/(p−2), p | h')
    ax.set_xlabel('gap h'); ax.legend(fontsize=8)
    save('16-2')


@fig('16-3')
def _():
    fig_, axs = plt.subplots(1, 2, figsize=(6.6, 2.4))
    for ax, q in zip(axs, (3, 7)):
        vals = [(n * n + n + 1) % q for n in range(q)]
        ax.bar(range(q), [1] * q, color=[C2 if v == 0 else '#dddddd' for v in vals])
        for n, v in enumerate(vals):
            ax.text(n, .5, str(v), ha='center')
        ax.set_yticks([]); ax.set_xticks(range(q)); ax.set_title(f'n²+n+1 mod {q}: w({q}) = {vals.count(0)}', fontsize=9)
    save('16-3')


@fig('16-4')
def _():
    x = np.logspace(2, 12, 200)
    ax = plt.gca()
    ax.plot(x, 2 * np.sqrt(x), color=C1, label='length of [n², (n+1)²] ≈ 2√x')
    ax.plot(x, np.sqrt(x) * np.log(x), color=C2, label='RH guarantees a prime only in √x·log x')
    ax.set_xscale('log'); ax.set_yscale('log'); ax.legend(fontsize=8); ax.set_xlabel('x')
    save('16-4')


@fig('16-5')
def _():
    ax = plt.gca(); plt.gcf().set_size_inches(6.6, 2.4)
    for n in range(1, 31):
        c = {0: '#c6dbef', 1: '#c7e9c0', 2: '#fdd0a2'}[n % 3]
        ax.add_patch(plt.Rectangle((n - .45, 0), .9, .9, fc=c))
        ax.text(n, .45, str(n), ha='center', va='center', fontsize=8, color=C2 if isp(n) else 'k')
    for n in (5, 11, 17, 23):
        ax.add_patch(plt.Rectangle((n - .45, 0), .9, .9, fill=False, ec=C2, lw=2))
    ax.set_xlim(0, 31); ax.set_ylim(-.2, 1.2); ax.axis('off')
    ax.set_title('5, 11, 17, 23: step 6 keeps the class mod 3; step 2 or 4 would hit a multiple of 3', fontsize=9)
    save('16-5')


# ================= lesson 17 =================
@fig('17-1')
def _():
    ax = plt.gca(); plt.gcf().set_size_inches(5.4, 4.0)
    for n in range(1, 101):
        r, c = (n - 1) // 10, (n - 1) % 10
        keep = n % 2 and n % 3
        semi = keep and n > 1 and not isp(n) and len(factor(n)) <= 2 and sum(factor(n).values()) == 2
        ax.add_patch(plt.Rectangle((c, -r), .95, .95, fc=C4 if semi else ('#2ca02c' if keep else '#eeeeee')))
        ax.text(c + .47, -r + .47, str(n), ha='center', va='center', fontsize=6.5)
    ax.set_xlim(0, 10); ax.set_ylim(-9, 1); ax.set_aspect('equal'); ax.axis('off')
    ax.set_title('φ(100, 2) = 33 survivors of 2 and 3; orange: the 9 products pq with 5 ≤ p ≤ q', fontsize=8)
    save('17-1')


@fig('17-2')
def _():
    M = 10000
    Mx = np.cumsum([mu(n) for n in range(1, M + 1)])
    xs = np.arange(1, M + 1)
    ax = plt.gca()
    ax.plot(xs, np.abs(Mx) / np.sqrt(xs), color=C1, lw=.6)
    ax.axhline(1, color=C2, ls='--', label='Mertens conjecture: < 1 (false, but only far away)')
    ax.set_xscale('log'); ax.legend(fontsize=8); ax.set_xlabel('x'); ax.set_ylabel('|M(x)|/√x')
    save('17-2')


@fig('17-3')
def _():
    from mpmath import dirichlet, sqrt as msqrt, mpf
    k = (msqrt(10 - 2 * msqrt(5)) - 2) / (msqrt(5) - 1)
    chi = [0, 1, 1j, -1j, -1]
    chib = [0, 1, -1j, 1j, -1]
    f = lambda s: (1 - 1j * k) / 2 * dirichlet(s, chi) + (1 + 1j * k) / 2 * dirichlet(s, chib)
    t = np.linspace(84.5, 87, 220)
    ax = plt.gca()
    ax.plot(t, [abs(complex(f(complex(0.808517, y)))) for y in t], color=C2, label='|f(0.8085 + it)|')
    ax.plot(t, [abs(complex(f(complex(0.5, y)))) for y in t], color=C1, label='|f(1/2 + it)|')
    ax.axvline(85.699348, color=GR, ls='--', lw=.7)
    ax.set_xlabel('t'); ax.legend(fontsize=8)
    ax.set_title('Davenport–Heilbronn function: a zero at 0.8085 + 85.6993i, off the critical line', fontsize=9)
    save('17-3')

@fig('17-4')
def _():
    from mpmath import siegelz
    t = np.linspace(0, 40, 800)
    ax = plt.gca()
    ax.plot(t, [float(siegelz(x)) for x in t], color=C1)
    ax.axhline(0, color='k', lw=.6)
    for g in (14.1347, 21.0220, 25.0109, 30.4249, 32.9351, 37.5862):
        ax.scatter([g], [0], color=C2, zorder=3)
    ax.set_xlabel('t'); ax.set_ylabel('Z(t)'); ax.set_title('Riemann–Siegel Z: each sign change is a zero (25 < γ₃ < 26)')
    save('17-4')


@fig('17-5')
def _():
    from mpmath import li
    xs = np.logspace(1, 6, 120)
    pi_x = [np.searchsorted(PR, x, side='right') for x in xs]
    ax = plt.gca()
    ax.plot(xs, [p - float(li(x) - li(2)) for p, x in zip(pi_x, xs)], color=C1, label='π(x) − Li(x)')
    ax.plot(xs, [-0.5 * float(li(sqrt(x))) for x in xs], color=C2, ls='--', label='−½ Li(√x)')
    ax.axhline(0, color='k', lw=.6); ax.set_xscale('log'); ax.legend(fontsize=8); ax.set_xlabel('x')
    save('17-5')


@fig('17-6')
def _():
    M = 5000
    sig = [0] * (M + 1)
    for d_ in range(1, M + 1):
        for m in range(d_, M + 1, d_):
            sig[m] += d_
    H = np.cumsum(1 / np.arange(1, M + 1))
    ns = np.arange(2, M + 1)
    ratio = [sig[n] / (H[n - 1] + math.exp(H[n - 1]) * log(H[n - 1])) for n in ns]
    ax = plt.gca()
    ax.scatter(ns, ratio, s=1, color=C1)
    ax.axhline(1, color=C2, ls='--')
    ax.scatter([12], [ratio[10]], color=C2, s=50, zorder=3); ax.annotate('n = 12: 0.989', (12, ratio[10]), xytext=(10, -20), textcoords='offset points', color=C2)
    ax.set_xscale('log'); ax.set_xlabel('n'); ax.set_ylabel('σ(n) / (H_n + e^{H_n} log H_n)'); ax.set_title('Lagarias: RH ⇔ always below 1')
    save('17-6')


@fig('17-7')
def _():
    p, g = 101, 2
    ax = plt.gca()
    ks = range(p - 1)
    ax.scatter(ks, [pow(g, k, p) for k in ks], s=10, color=C1)
    ax.set_xlabel('k'); ax.set_ylabel('2^k mod 101')
    ax.set_title('easy forwards (square-and-multiply), looks random backwards (discrete log)')
    save('17-7')


# =====================================================================
# Figures for the worked examples (keys 'LL-eK')
# =====================================================================
def bar_line(ax, xs, ys, hi=None, color=C1, hicolor=C2):
    ax.bar(xs, ys, color=[hicolor if (hi and hi(x)) else color for x in xs])


def sieve_grid(ax, n, cols, primes_to_strike, title):
    pal = ['#c6dbef', '#fdd0a2', '#c7e9c0', '#dadaeb', '#fcbba1', '#d9f0a3']
    for k in range(1, n + 1):
        r, c = (k - 1) // cols, (k - 1) % cols
        p = next((q for q in primes_to_strike if k % q == 0 and k != q), None)
        fc = pal[primes_to_strike.index(p) % 6] if p else ('#fde0dd' if isp(k) else 'white')
        ax.add_patch(plt.Rectangle((c, -r), .95, .95, fc=fc, ec='#bbbbbb'))
        ax.text(c + .47, -r + .47, str(k), ha='center', va='center', fontsize=7, color=C2 if isp(k) else 'k')
    rows = (n - 1) // cols + 1
    ax.set_xlim(0, cols); ax.set_ylim(-rows + 1, 1); ax.set_aspect('equal'); ax.axis('off'); ax.set_title(title, fontsize=9)


# ---------- lesson 1 ----------
@fig('01-e1')
def _():
    fig_, axs = plt.subplots(2, 1, figsize=(6.6, 2.8))
    for ax, a in zip(axs, (2026, -2026)):
        q = a // 17; lo = 17 * q
        ax.axhline(0, color='k', lw=.6)
        for m in range(q - 2, q + 3):
            ax.scatter([17 * m], [0], color=C1, s=40); ax.annotate(f'17·{m}', (17 * m, 0), xytext=(0, -14), textcoords='offset points', ha='center', fontsize=7)
        ax.scatter([a], [0], color=C2, s=60, zorder=3)
        ax.annotate('', xy=(a, .3), xytext=(lo, .3), arrowprops=dict(arrowstyle='->', color=C3, lw=2))
        ax.text((a + lo) / 2, .5, f'r = {a - lo}', ha='center', color=C3, fontsize=8)
        ax.set_title(f'{a} = 17·({q}) + {a - lo}', fontsize=9); ax.set_ylim(-.8, 1); ax.set_yticks([]); ax.spines['left'].set_visible(False)
    save('01-e1')


@fig('01-e2')
def _():
    ns = range(-25, 26)
    ax = plt.gca()
    ax.bar(ns, [gcd(3 * n + 5, 2 * n + 3) for n in ns], color=C1)
    ax.set_ylim(0, 2); ax.set_xlabel('n'); ax.set_title('gcd(3n+5, 2n+3) = 1 always:  3(2n+3) − 2(3n+5) = −1')
    save('01-e2')


@fig('01-e3')
def _():
    ns = np.arange(-6, 10)
    ax = plt.gca()
    ax.bar(ns, [(n ** 3 - n) // 6 for n in ns], color=C1)
    ax.axhline(0, color='k', lw=.5); ax.set_xlabel('n'); ax.set_ylabel('(n³ − n)/6')
    ax.set_title('(n³ − n)/6 is always an integer (product of 3 consecutive numbers)')
    save('01-e3')


@fig('01-e4')
def _():
    ns = np.arange(0, 10)
    ax = plt.gca()
    ax.bar(ns, [(7 ** int(n) - 1) / 6 for n in ns], color=C1)
    ax.set_yscale('symlog'); ax.set_xlabel('n'); ax.set_ylabel('(7ⁿ − 1)/6')
    ax.set_title('7 ≡ 1 (mod 6) ⇒ 7ⁿ − 1 ≡ 0: (7ⁿ−1)/6 = 1 + 7 + … + 7ⁿ⁻¹')
    save('01-e4')


@fig('01-e5')
def _():
    d = [9, 1, 8, 0, 8, 2]
    sign = [(-1) ** (len(d) - 1 - i) for i in range(len(d))]
    ax = plt.gca()
    ax.bar(range(6), d, color=C1, alpha=.5, label=f'digits: sum {sum(d)}')
    ax.bar(range(6), [a * s for a, s in zip(d, sign)], width=.45, color=C2, label=f'alternating: {sum(a*s for a,s in zip(d,sign))}')
    ax.axhline(0, color='k', lw=.5); ax.set_xticks(range(6)); ax.set_xticklabels(d); ax.legend(fontsize=8)
    ax.set_title('918082: 28 → not ÷3, not ÷9;  alternating sum 22 → ÷11')
    save('01-e5')


# ---------- lesson 2 ----------
@fig('02-e1')
def _():
    euclid_tiles(plt.gca(), 1071, 462, '1071×462 → 147 → 21: gcd = 21')
    save('02-e1')


@fig('02-e2')
def _():
    rows = [(1071, 1, 0), (462, 0, 1), (147, 1, -2), (21, -3, 7), (0, 22, -51)]
    ax = plt.gca()
    ax.plot(range(5), [r[0] for r in rows], 'o-', color=C1, label='remainder r')
    ax.plot(range(5), [r[1] for r in rows], 's--', color=C4, label='x')
    ax.plot(range(5), [r[2] for r in rows], '^--', color=C3, label='y')
    for i, (r, x, y) in enumerate(rows):
        ax.annotate(f'{r} = 1071·({x}) + 462·({y})', (i, r), xytext=(5, 8), textcoords='offset points', fontsize=7)
    ax.set_yscale('symlog'); ax.set_xlabel('row of the table'); ax.legend(fontsize=8)
    ax.set_title('extended Euclid: every row keeps r = 1071x + 462y')
    save('02-e2')


@fig('02-e3')
def _():
    ax = plt.gca()
    xs = np.linspace(0, 15, 100)
    ax.plot(xs, (200 - 14 * xs) / 9, color=C1, label='14x + 9y = 200')
    X, Y = np.meshgrid(range(0, 16), range(0, 24))
    ax.scatter(X, Y, s=3, color=GR)
    ax.scatter([4, 13], [16, 2], s=70, color=C2, zorder=3)
    for p in [(4, 16), (13, 2)]:
        ax.annotate(f'{p[0]} notebooks, {p[1]} pens', p, xytext=(6, 4), textcoords='offset points', fontsize=8)
    ax.set_xlim(0, 15); ax.set_ylim(0, 23); ax.set_xlabel('x (notebooks)'); ax.set_ylabel('y (pens)'); ax.legend(fontsize=8)
    save('02-e3')


# ---------- lesson 3 ----------
@fig('03-e1')
def _():
    ps = [2, 3, 5, 7, 11, 13, 17, 19]
    ax = plt.gca()
    ax.bar(np.arange(8) - .2, [391 % p for p in ps], width=.4, color=C1, label='391 mod p')
    ax.bar(np.arange(8) + .2, [397 % p for p in ps], width=.4, color=C4, label='397 mod p')
    ax.set_xticks(range(8)); ax.set_xticklabels(ps); ax.set_xlabel('primes p ≤ √n'); ax.legend(fontsize=8)
    ax.set_title('391 has remainder 0 at p = 17 (391 = 17·23); 397 never → prime')
    save('03-e1')


@fig('03-e2')
def _():
    sieve_grid(plt.gca(), 50, 10, [2, 3, 5, 7], 'Eratosthenes to 50: strike multiples of 2, 3, 5, 7 → 15 primes (red)')
    save('03-e2')


@fig('03-e3')
def _():
    ps = [2, 3, 5, 7]
    a = [3, 2, 1, 0]; b = [2, 3, 0, 1]
    x = np.arange(4)
    ax = plt.gca()
    ax.bar(x - .2, a, width=.4, color=C1, label='360 = 2³·3²·5')
    ax.bar(x + .2, b, width=.4, color=C4, label='756 = 2²·3³·7')
    ax.plot(x, [min(i, j) for i, j in zip(a, b)], 'v', color=C3, ms=9, label='min → gcd 36')
    ax.plot(x, [max(i, j) for i, j in zip(a, b)], '^', color=C2, ms=9, label='max → lcm 7560')
    ax.set_xticks(x); ax.set_xticklabels(ps); ax.set_ylabel('exponent'); ax.legend(fontsize=8)
    save('03-e3')


@fig('03-e4')
def _():
    ax = plt.gca(); plt.gcf().set_size_inches(4.6, 4.2)
    X, Y = np.meshgrid(range(1, 21), range(1, 21))
    ax.scatter(X, Y, s=6, color=GR)
    t = np.linspace(0, 20, 50); ax.plot(t / sqrt(2), t, color=C2, label='a = √2·b')
    for b, a in [(2, 3), (5, 7), (12, 17)]:
        ax.scatter([b], [a], color=C1, s=30); ax.annotate(f'{a}²−2·{b}² = {a*a-2*b*b}', (b, a), xytext=(5, -4), textcoords='offset points', fontsize=7)
    ax.set_xlabel('b'); ax.set_ylabel('a'); ax.set_aspect('equal'); ax.legend(fontsize=8)
    ax.set_title('the line a = √2 b passes between all lattice points', fontsize=9)
    save('03-e4')


# ---------- lesson 4 ----------
@fig('04-e1')
def _():
    fig_, ax = plt.subplots(figsize=(4.2, 4.2))
    power_cycle(ax, 7, 10, 'last digit of 7^k: 7, 9, 3, 1, …  (period 4)')
    save('04-e1')


@fig('04-e2')
def _():
    ks = range(0, 10)
    ax = plt.gca()
    ax.bar(np.array(ks) - .2, [pow(10, k, 9) for k in ks], width=.4, color=C1, label='10^k mod 9 = 1')
    ax.bar(np.array(ks) + .2, [1 if pow(10, k, 11) == 1 else -1 for k in ks], width=.4, color=C2, label='10^k mod 11 = ±1')
    ax.axhline(0, color='k', lw=.5); ax.set_xlabel('k (place of the digit)'); ax.legend(fontsize=8)
    save('04-e2')


@fig('04-e3')
def _():
    js = range(7)
    vals = [pow(3, 2 ** j, 7) for j in js]
    ax = plt.gca()
    ax.bar([f'3^{2**j}' for j in js], vals, color=[C2 if (100 >> j) & 1 else C1 for j in js])
    ax.set_ylabel('mod 7'); ax.set_title('repeated squaring; red = used for 100 = 64 + 32 + 4 → 4·2·4 ≡ 4')
    save('04-e3')


@fig('04-e4')
def _():
    ax = plt.gca()
    xs = range(43)
    ax.scatter(xs, [17 * x % 43 for x in xs], s=12, color=C1)
    ax.scatter([38], [1], s=80, color=C2, zorder=3); ax.annotate('17·38 = 646 ≡ 1', (38, 1), xytext=(-90, 15), textcoords='offset points', color=C2)
    ax.set_xlabel('x'); ax.set_ylabel('17x mod 43'); ax.set_title('17x runs through every residue once (17 is invertible)')
    save('04-e4')


@fig('04-e5')
def _():
    ax = plt.gca()
    xs = range(30)
    ax.scatter(xs, [12 * x % 30 for x in xs], s=14, color=C1)
    sol = [x for x in xs if 12 * x % 30 == 18]
    ax.scatter(sol, [18] * len(sol), s=70, color=C2, zorder=3); ax.axhline(18, color=C2, ls='--', lw=.6)
    ax.set_xlabel('x'); ax.set_ylabel('12x mod 30'); ax.set_title('12x takes only multiples of gcd = 6; value 18 hit 6 times: x ≡ 4 (mod 5)')
    save('04-e5')


@fig('04-e6')
def _():
    ax = plt.gca(); plt.gcf().set_size_inches(6.8, 3.4)
    for x in range(105):
        c, r = x % 15, x % 7
        ok = x % 3 == 2 and x % 5 == 3
        ax.add_patch(plt.Rectangle((c, r), .95, .95, fc=(C2 if x == 23 else ('#fdd0a2' if ok else 'white')), ec='#dddddd'))
        ax.text(c + .47, r + .47, str(x), ha='center', va='center', fontsize=6, color='w' if x == 23 else 'k')
    ax.set_xlim(0, 15); ax.set_ylim(0, 7); ax.set_xlabel('x mod 15'); ax.set_ylabel('x mod 7')
    ax.set_xticks(np.arange(15) + .5); ax.set_xticklabels(range(15), fontsize=7); ax.set_yticks(np.arange(7) + .5); ax.set_yticklabels(range(7))
    ax.set_title('CRT: each x < 105 has its own cell; orange: x ≡ 2 (3), x ≡ 3 (5); red: also ≡ 2 (7) → 23', fontsize=8.5)
    save('04-e6')


# ---------- lesson 5 ----------
@fig('05-e1')
def _():
    fig_, ax = plt.subplots(figsize=(4.2, 4.2))
    power_cycle(ax, 3, 13, '3^k mod 13: 3, 9, 1 — period 3 (divides 12)')
    save('05-e1')


@fig('05-e2')
def _():
    ax = plt.gca()
    ks = range(0, 91)
    ax.scatter(ks, [pow(2, k, 91) for k in ks], s=10, color=C1)
    ax.scatter([90], [64], s=70, color=C2, zorder=3); ax.annotate('2⁹⁰ ≡ 64 ≠ 1 ⇒ 91 composite', (90, 64), xytext=(-170, 10), textcoords='offset points', color=C2)
    ax.set_xlabel('k'); ax.set_ylabel('2^k mod 91'); ax.set_title('period 12 — and 12 does not divide 90')
    save('05-e2')


@fig('05-e3')
def _():
    ax = plt.gca()
    ks = range(0, 61)
    ax.plot(ks, [pow(3, k, 100) for k in ks], 'o-', ms=3, color=C1)
    ax.axvline(20, color=GR, ls='--'); ax.axvline(40, color=GR, ls='--')
    ax.set_xlabel('k'); ax.set_ylabel('3^k mod 100'); ax.set_title('3^20 ≡ 1 (mod 100): the last two digits repeat every 20')
    save('05-e3')


@fig('05-e4')
def _():
    ax = plt.gca(); plt.gcf().set_size_inches(4.8, 4.4)
    ms = range(143)
    ax.scatter(ms, [pow(m, 7, 143) for m in ms], s=5, color=C1)
    ax.scatter([9], [48], s=70, color=C2, zorder=3); ax.annotate('9 → 48', (9, 48), xytext=(8, 4), textcoords='offset points', color=C2)
    ax.set_xlabel('message m'); ax.set_ylabel('m^7 mod 143'); ax.set_aspect('equal')
    ax.set_title('RSA encryption scrambles 0..142 (a permutation)', fontsize=9)
    save('05-e4')


@fig('05-e5')
def _():
    p = 7
    fig_, ax = plt.subplots(figsize=(4.2, 4.2))
    pts = circle_nodes(ax, p - 1, labels=list(range(1, p)))
    for a in range(1, p):
        b = pow(a, -1, p)
        if a < b:
            ax.plot([pts[a - 1][0], pts[b - 1][0]], [pts[a - 1][1], pts[b - 1][1]], color=C1)
    for a in (1, 6):
        ax.scatter(*pts[a - 1], s=120, color=C2, zorder=4)
    ax.set_title('6! mod 7: (2·4)(3·5) ≡ 1, leaving 1·6 ≡ −1')
    save('05-e5')


@fig('05-e6')
def _():
    ps = [5, 7, 11, 13, 17, 19, 23, 29, 31]
    def vp(n, p):
        e = 0
        while n % p == 0:
            n //= p; e += 1
        return e
    ax = plt.gca()
    ax.bar([str(p) for p in ps], [vp(comb(2 * p - 1, p - 1) - 1, p) for p in ps], color=C1)
    ax.axhline(3, color=C2, ls='--'); ax.set_xlabel('p'); ax.set_ylabel('power of p in C(2p−1,p−1) − 1')
    ax.set_title('Wolstenholme: at least 3 for every p ≥ 5')
    save('05-e6')


# ---------- lesson 6 ----------
@fig('06-e1')
def _():
    ds = divisors(360)
    ax = plt.gca()
    ax.bar(range(len(ds)), ds, color=C1)
    ax.set_xticks(range(len(ds))); ax.set_xticklabels(ds, fontsize=6, rotation=90)
    ax.set_title('the 24 divisors of 360; their sum is 15·13·6 = 1170')
    save('06-e1')


@fig('06-e2')
def _():
    n = 12
    fig_, ax = plt.subplots(figsize=(6.6, 2.2))
    cols = {1: C1, 2: C3, 3: C4, 4: '#9467bd', 6: '#8c564b', 12: C2}
    for k in range(1, n + 1):
        g = gcd(k, n)
        ax.add_patch(plt.Rectangle((k - .45, 0), .9, .9, fc=cols[g]))
        ax.text(k, .45, str(k), ha='center', va='center', color='w')
        ax.text(k, -.25, f'g={g}', ha='center', fontsize=7)
    ax.set_xlim(.4, 12.6); ax.set_ylim(-.5, 1); ax.axis('off')
    ax.set_title('1..12 sorted by gcd(k,12) = g: group g has φ(12/g) members → Σ φ(d) = 12', fontsize=9)
    save('06-e2')


@fig('06-e3')
def _():
    ds = divisors(12)
    fig_, ax = plt.subplots(figsize=(6.6, 1.8))
    left = 0
    for d_, c in zip(ds, [C1, C3, C4, '#9467bd', '#8c564b', C2]):
        ax.barh(0, phi(d_), left=left, color=c, ec='w'); ax.text(left + phi(d_) / 2, 0, f'φ({d_})={phi(d_)}', ha='center', va='center', fontsize=8, color='w')
        left += phi(d_)
    ax.set_xlim(0, 12); ax.set_yticks([]); ax.set_title('φ(1)+φ(2)+φ(3)+φ(4)+φ(6)+φ(12) = 12')
    save('06-e3')


@fig('06-e4')
def _():
    ns = np.arange(1, 13)
    Nn = [sum(mu(d_) * 2 ** (int(n) // d_) for d_ in divisors(int(n))) // int(n) for n in ns]
    ax = plt.gca()
    ax.bar(ns, Nn, color=C1, label='irreducible polynomials of degree n over F₂')
    ax.plot(ns, 2.0 ** ns / ns, 'o--', color=C2, ms=3, label='2ⁿ/n')
    ax.set_yscale('log'); ax.set_xlabel('n'); ax.legend(fontsize=8); ax.set_title('N₄ = (2⁴ − 2²)/4 = 3')
    save('06-e4')


@fig('06-e5')
def _():
    ns = np.arange(1, 61)
    ps = [int(n * np.prod([1 + 1 / p for p in factor(int(n))])) for n in ns]
    ax = plt.gca()
    ax.plot(ns, [phi(int(n)) for n in ns], 'o', ms=3, color=C1, label='φ(n)')
    ax.plot(ns, ps, 's', ms=3, color=C4, label='ψ(n) (Dedekind)')
    ax.plot(ns, ns, color=GR, lw=.6, label='n')
    ax.set_xlabel('n'); ax.legend(fontsize=8); ax.set_title('φ(n) ≤ n ≤ ψ(n), and J₂(n) = φ(n)ψ(n)')
    save('06-e5')


@fig('06-e6')
def _():
    ns = np.arange(1, 101)
    lam = lambda m: (-1) ** sum(factor(m).values()) if m > 1 else 1
    v = [sum(lam(d_) for d_ in divisors(int(n))) for n in ns]
    ax = plt.gca()
    ax.bar(ns, v, color=[C2 if x else C1 for x in v])
    for n in ns:
        if v[n - 1]:
            ax.text(n, 1.05, str(n), ha='center', fontsize=7)
    ax.set_ylim(0, 1.3); ax.set_xlabel('n'); ax.set_title('Σ_{d|n} λ(d) = 1 exactly at the squares')
    save('06-e6')


@fig('06-e7')
def _():
    fig_, ax = plt.subplots(figsize=(4.4, 4.2))
    ax.add_patch(plt.Circle((0, 0), 1, fill=False, color='#dddddd'))
    for a in (1, 5):
        z = cmath.exp(2j * pi * a / 6); w = z ** 4
        ax.scatter(z.real, z.imag, s=70, color=C1); ax.annotate(f'e^{{2πi·{a}/6}}', (z.real, z.imag), xytext=(6, 6), textcoords='offset points', fontsize=8)
        ax.scatter(w.real, w.imag, s=70, color=C2); ax.annotate('4th power', (w.real, w.imag), xytext=(6, -12), textcoords='offset points', fontsize=8, color=C2)
    ax.annotate('', xy=(-1, 0), xytext=(0, 0), arrowprops=dict(arrowstyle='->', color=C3, lw=2))
    ax.text(-.6, .08, 'sum = −1', color=C3)
    ax.set_aspect('equal'); ax.set_xlim(-1.3, 1.3); ax.set_ylim(-1.3, 1.3); ax.axis('off'); ax.set_title('c₆(4): the two red points add up to −1')
    save('06-e7')


# ---------- lesson 7 ----------
@fig('07-e1')
def _():
    T = np.array([[pow(a, k, 7) for k in range(1, 7)] for a in range(1, 7)])
    ax = plt.gca(); plt.gcf().set_size_inches(5, 3.6)
    ax.imshow(T, cmap='Pastel1')
    for i in range(6):
        for j in range(6):
            ax.text(j, i, str(T[i, j]), ha='center', va='center', fontweight='bold' if T[i, j] == 1 else None)
    ax.set_xticks(range(6)); ax.set_xticklabels(range(1, 7)); ax.set_yticks(range(6)); ax.set_yticklabels(range(1, 7))
    ax.set_xlabel('k'); ax.set_ylabel('a'); ax.set_title('a^k mod 7: the first 1 in each row is the order (3 and 5 reach k = 6)', fontsize=9)
    save('07-e1')


@fig('07-e2')
def _():
    fig_, ax = plt.subplots(figsize=(4.6, 4.6))
    power_cycle(ax, 5, 23, '5 is a primitive root mod 23: all 22 residues')
    save('07-e2')


@fig('07-e3')
def _():
    fig_, ax = plt.subplots(figsize=(4.4, 4.4))
    order = [pow(3, k, 7) for k in range(6)]
    pts = circle_nodes(ax, 6, labels=[f'3^{k}={v}' for k, v in enumerate(order)])
    for k in (1, 3, 5):
        ax.scatter(*pts[k], s=130, color=C2, zorder=4)
    ax.set_title('index of 6 is 3; x³ ≡ 6 ⇔ 3k ≡ 3 (mod 6) ⇔ k odd → x = 3, 6, 5', fontsize=8.5)
    save('07-e3')


@fig('07-e4')
def _():
    fig_, ax = plt.subplots(figsize=(4.4, 4.4))
    pts = circle_nodes(ax, 11, labels=list(range(11)))
    qr = {x * x % 11 for x in range(1, 11)}
    for r in qr:
        ax.scatter(*pts[r], s=120, color=C1, zorder=4)
    for x in range(1, 6):
        arrow(ax, pts[x], pts[x * x % 11], color=GR, rad=.25)
    ax.set_title('squares mod 11 (blue): 1, 3, 4, 5, 9 — exactly half')
    save('07-e4')


@fig('07-e5')
def _():
    p = 19
    ax = plt.gca()
    vals = [pow(a, 9, p) for a in range(1, p)]
    ax.bar(range(1, p), [1 if v == 1 else -1 for v in vals], color=[C1 if v == 1 else C2 for v in vals])
    ax.annotate('5⁹ ≡ 1', (5, 1), xytext=(0, 8), textcoords='offset points', ha='center')
    ax.axhline(0, color='k', lw=.5); ax.set_xlabel('a'); ax.set_ylabel('a⁹ mod 19 (as ±1)'); ax.set_title("Euler's criterion: a^((p−1)/2) = +1 for residues, −1 otherwise")
    save('07-e5')


@fig('07-e6')
def _():
    ps = [p for p in PR if 3 < p < 400]
    ax = plt.gca()
    ax.scatter(ps, [p % 12 for p in ps], c=[C1 if legendre(3, p) == 1 else C2 for p in ps], s=12)
    ax.scatter([383], [383 % 12], s=90, facecolors='none', edgecolors='k')
    ax.set_yticks([1, 5, 7, 11]); ax.set_xlabel('prime p'); ax.set_ylabel('p mod 12')
    ax.set_title('(3/p) = +1 (blue) exactly when p ≡ ±1 (mod 12)')
    save('07-e6')


@fig('07-e7')
def _():
    ps = [p for p in PR if 3 < p < 1000]
    T = np.zeros((2, 12))
    for p in ps:
        T[0 if legendre(3, p) == 1 else 1, p % 12] += 1
    ax = plt.gca()
    for r in (1, 5, 7, 11):
        ax.bar(r - .2, T[0, r], width=.4, color=C1); ax.bar(r + .2, T[1, r], width=.4, color=C2)
    ax.set_xticks([1, 5, 7, 11]); ax.set_xlabel('p mod 12'); ax.set_ylabel('number of primes < 1000')
    ax.set_title('blue: 3 is a square mod p; red: it is not — decided by p mod 12')
    save('07-e7')


@fig('07-e8')
def _():
    chain = [(219, 383), (164, 219), (41, 219), (14, 41), (7, 41), (6, 7), (3, 7), (1, 3)]
    ax = plt.gca()
    ax.plot(range(len(chain)), [b for _, b in chain], 'o-', color=C1, label='n')
    ax.plot(range(len(chain)), [a for a, _ in chain], 's-', color=C4, label='a')
    for i, (a, b) in enumerate(chain):
        ax.annotate(f'({a}/{b})', (i, b), xytext=(3, 6), textcoords='offset points', fontsize=7)
    ax.set_yscale('log'); ax.legend(fontsize=8); ax.set_xlabel('step'); ax.set_title('(219/383) with Jacobi symbols only — no factoring')
    save('07-e8')


@fig('07-e9')
def _():
    fig_, ax = plt.subplots(figsize=(4.6, 4.4))
    tot = 0
    for a in range(5):
        z = cmath.exp(2j * pi * a * a / 5)
        ax.annotate('', xy=((tot + z).real, (tot + z).imag), xytext=(tot.real, tot.imag), arrowprops=dict(arrowstyle='->', color=C1, lw=1.5))
        tot += z
    ax.scatter([tot.real], [tot.imag], color=C2, s=60, zorder=3); ax.annotate(f'√5 ≈ {tot.real:.4f}', (tot.real, tot.imag), xytext=(6, 8), textcoords='offset points', color=C2)
    ax.set_xlim(-.5, 3); ax.set_ylim(-1.5, 1.5); ax.set_aspect('equal'); ax.axhline(0, color='#eeeeee')
    ax.set_title('Gauss sum Σ e^{2πi a²/5}: five unit steps end at √5', fontsize=9)
    save('07-e9')


# ---------- lesson 8 ----------
@fig('08-e1')
def _():
    fig_, axs = plt.subplots(1, 2, figsize=(6.4, 2.6))
    axs[0].bar(range(3), [x * x % 3 for x in range(3)], color=C1); axs[0].set_title('x² mod 3 ∈ {0, 1}', fontsize=9); axs[0].set_xticks(range(3))
    axs[1].bar(range(3), [(3 * y * y + 2) % 3 for y in range(3)], color=C2); axs[1].set_title('3y² + 2 mod 3 = 2 always', fontsize=9); axs[1].set_xticks(range(3))
    save('08-e1')


@fig('08-e2')
def _():
    ax = plt.gca()
    xs = np.linspace(6.7, 25, 300)
    ax.plot(xs, np.sqrt(xs ** 2 - 45), color=C1, label='x² − y² = 45')
    pts = [(23, 22), (9, 6), (7, 2)]
    ax.scatter(*zip(*pts), color=C2, s=50, zorder=3)
    for p in pts:
        ax.annotate(str(p), p, xytext=(5, -10), textcoords='offset points', fontsize=8)
    X, Y = np.meshgrid(range(0, 26), range(0, 24))
    ax.scatter(X, Y, s=2, color=GR); ax.legend(fontsize=8); ax.set_title('45 = 1·45 = 3·15 = 5·9 → three lattice points')
    save('08-e2')


@fig('08-e3')
def _():
    ax = plt.gca(); plt.gcf().set_size_inches(4.6, 4.4)
    t = np.linspace(0, pi / 2, 200); ax.plot(np.cos(t), np.sin(t), color='#cccccc')
    for m in range(2, 12):
        for n in range(1, m):
            if gcd(m, n) == 1 and (m - n) % 2:
                x, y, z = m * m - n * n, 2 * m * n, m * m + n * n
                if z < 150:
                    ax.scatter([x / z, y / z], [y / z, x / z], s=14, color=C1 if z < 50 else C4)
    ax.set_aspect('equal'); ax.set_title('primitive triples = rational points on the unit circle\n(blue: z < 50)', fontsize=9)
    save('08-e3')


@fig('08-e4')
def _():
    fig_, axs = plt.subplots(1, 2, figsize=(6.8, 3.4))
    for ax, n in zip(axs, (65, 1105)):
        R = sqrt(n); t = np.linspace(0, pi / 2, 200)
        ax.plot(R * np.cos(t), R * np.sin(t), color=C1)
        pts = [(x, int(round(sqrt(n - x * x)))) for x in range(0, int(R) + 1) if int(round(sqrt(n - x * x))) ** 2 == n - x * x]
        ax.scatter(*zip(*pts), color=C2, zorder=3, s=25)
        for p in pts:
            ax.annotate(str(p), p, xytext=(3, 3), textcoords='offset points', fontsize=7)
        ax.set_aspect('equal'); ax.set_title(f'x² + y² = {n}', fontsize=9); ax.grid(alpha=.3)
    save('08-e4')


@fig('08-e5')
def _():
    def two(n):
        f = factor(n)
        return all(e % 2 == 0 for p, e in f.items() if p % 4 == 3)
    ns = range(2010, 2041)
    ax = plt.gca()
    ax.bar(ns, [1] * 31, color=[C3 if two(n) else '#dddddd' for n in ns])
    for n in (2026, 2027):
        ax.text(n, 1.05, str(n), ha='center', color=C2)
    ax.set_yticks([]); ax.set_ylim(0, 1.3); ax.set_xlabel('n (green: sum of two squares)')
    save('08-e5')


@fig('08-e6')
def _():
    fig_, ax = plt.subplots(figsize=(6.4, 2.2))
    for row, (n, parts) in enumerate([(7, [4, 1, 1, 1]), (15, [9, 4, 1, 1]), (2026, [2025, 1])]):
        left = 0
        for k, v in enumerate(parts):
            w = v if n < 100 else v * 15 / n
            ax.barh(row, w, left=left, color=[C1, C3, C4, C2][k], ec='w'); left += w
        ax.text(left + .3, row, f'{n} = ' + ' + '.join(f'{int(sqrt(v))}²' for v in parts), va='center', fontsize=8)
    ax.set_yticks([]); ax.set_xlim(0, 24); ax.set_xticks([]); ax.set_title('7 and 15 need four squares; 2026 needs only two')
    save('08-e6')


@fig('08-e7')
def _():
    ax = plt.gca()
    xs = np.linspace(1, 100, 500)
    ax.plot(xs, np.sqrt((xs ** 2 - 1) / 2), color=C1, label='x² − 2y² = 1')
    pts = [(3, 2), (17, 12), (99, 70)]
    ax.scatter(*zip(*pts), color=C2, zorder=3)
    for p in pts:
        ax.annotate(f'{p}: {p[0]}/{p[1]} ≈ {p[0]/p[1]:.5f}', p, xytext=(-10, 10), textcoords='offset points', fontsize=8, ha='right')
    ax.legend(fontsize=8); ax.set_title('Pell solutions give the best approximations of √2 = 1.41421…')
    save('08-e7')


@fig('08-e8')
def _():
    from fractions import Fraction
    a0 = int(sqrt(61)); m, d, a = 0, 1, a0
    cf = [a0]
    for _ in range(12):
        m = d * a - m; d = (61 - m * m) // d; a = (a0 + m) // d; cf.append(a)
    p0, q0, p1, q1 = 1, 0, a0, 1
    errs, labels = [abs(p1 / q1 - sqrt(61))], [f'{p1}/{q1}']
    for a in cf[1:11]:
        p0, p1 = p1, a * p1 + p0; q0, q1 = q1, a * q1 + q0
        errs.append(abs(p1 / q1 - sqrt(61)) + 1e-18); labels.append(str(p1))
    ax = plt.gca()
    ax.semilogy(range(len(errs)), errs, 'o-', color=C1)
    ax.set_xlabel('convergent of √61 = [7; 1,4,3,1,2,2,1,3,4,1,14, …]'); ax.set_ylabel('|p/q − √61|')
    ax.set_title('the period is 11 (odd) — the Pell solution needs two periods: x = 1,766,319,049', fontsize=9)
    save('08-e8')


@fig('08-e9')
def _():
    vals = set()
    for a in range(1, 40):
        for b in range(a + 1, 40):
            for c in range(b + 1, 80):
                v = a * b + b * c + c * a
                if v <= 120: vals.add(v)
    ns = range(1, 121)
    ax = plt.gca()
    ax.bar(ns, [1] * 120, width=1, color=[C1 if n in vals else C2 for n in ns])
    ax.set_yticks([]); ax.set_xlabel('n (red: idoneal — not ab+bc+ca with 0<a<b<c)')
    save('08-e9')


# ---------- lesson 9 ----------
def dsum(M):
    d = [0] * (M + 1)
    for a in range(1, M + 1):
        for m in range(a, M + 1, a):
            d[m] += 1
    return d


@fig('09-e1')
def _():
    M = 2000; d = dsum(M); xs = np.arange(1, M + 1); S = np.cumsum(d[1:])
    ax = plt.gca()
    ax.plot(xs, S, color=C1, label='Σ d(n)'); ax.plot(xs, xs * np.log(xs), color=C2, ls='--', label='x log x')
    ax.legend(fontsize=8); ax.set_xlabel('x'); ax.set_title('average of d(n) ≈ log n')
    save('09-e1')


@fig('09-e2')
def _():
    M = 5000
    sig = [0] * (M + 1)
    for a in range(1, M + 1):
        for m in range(a, M + 1, a):
            sig[m] += a
    xs = np.arange(1, M + 1)
    ax = plt.gca()
    ax.plot(xs, np.cumsum(sig[1:]) / xs ** 2, color=C1, label='Σσ(n) / x²'); ax.axhline(pi ** 2 / 12, color=C2, ls='--', label='π²/12')
    ax.set_xscale('log'); ax.legend(fontsize=8); ax.set_xlabel('x')
    save('09-e2')


@fig('09-e3')
def _():
    M = 3000
    ph = list(range(M + 1))
    for p in PR:
        if p > M: break
        for m in range(p, M + 1, p):
            ph[m] -= ph[m] // p
    xs = np.arange(1, M + 1)
    ax = plt.gca()
    ax.plot(xs, (2 * np.cumsum(ph[1:]) - 1) / xs ** 2, color=C1, label='share of coprime pairs (a,b) ≤ x')
    ax.axhline(6 / pi ** 2, color=C2, ls='--', label='6/π² ≈ 0.608')
    ax.set_xscale('log'); ax.legend(fontsize=8); ax.set_xlabel('x')
    save('09-e3')


@fig('09-e4')
def _():
    M = 20000; d = dsum(M); xs = np.arange(1, M + 1)
    D = np.cumsum(d[1:]) - (xs * np.log(xs) + (2 * 0.5772156649 - 1) * xs)
    ax = plt.gca()
    ax.plot(xs, D, color=C1, lw=.5, label='Δ(x) = Σd(n) − x log x − (2γ−1)x')
    ax.plot(xs, np.sqrt(xs), color=C2, ls='--', label='±√x'); ax.plot(xs, -np.sqrt(xs), color=C2, ls='--')
    ax.plot(xs, xs ** .25, color=C4, ls=':', label='±x^(1/4)'); ax.plot(xs, -xs ** .25, color=C4, ls=':')
    ax.legend(fontsize=7); ax.set_xlabel('x')
    save('09-e4')


@fig('09-e5')
def _():
    M = 100000; d = dsum(M); xs = np.arange(1, M + 1)
    ax = plt.gca()
    for e, c in ((.25, C1), (.5, C4)):
        ax.scatter(xs, np.array(d[1:]) / xs ** e, s=.3, color=c, label=f'd(n)/n^{e}')
    ax.set_xscale('log'); ax.legend(fontsize=8, markerscale=12); ax.set_xlabel('n'); ax.set_title('d(n)/n^ε stays bounded')
    save('09-e5')


@fig('09-e6')
def _():
    fig_, ax = plt.subplots(figsize=(6.4, 2.6))
    x0 = 0
    for L, c in ((2, C1), (3, C3), (5, C4)):
        cx = x0 + 1.2
        pts = circle_nodes(ax, L, labels=[''] * L, r=.9, color=c, size=50)
        ax.cla() if False else None
        x0 += 3
    ax.cla()
    x0 = 0
    for L, c in ((2, C1), (3, C3), (5, C4)):
        ang = [pi / 2 - 2 * pi * k / L for k in range(L)]
        P = [(x0 + np.cos(a), np.sin(a)) for a in ang]
        for k in range(L):
            arrow(ax, P[k], P[(k + 1) % L], color=c, rad=.3)
            ax.scatter(*P[k], s=60, color=c, zorder=3)
        ax.text(x0, -1.5, f'cycle of length {L}', ha='center', fontsize=8)
        x0 += 3
    ax.set_xlim(-1.5, 7.5); ax.set_ylim(-1.8, 1.3); ax.set_aspect('equal'); ax.axis('off')
    ax.set_title('g(10) = 30: cycles 2 + 3 + 5 = 10 points, order lcm(2,3,5) = 30', fontsize=9)
    save('09-e6')


@fig('09-e7')
def _():
    def smooth_share(x):
        n_big = sum(x // p for p in PR if sqrt(x) < p <= x)
        return 1 - n_big / x
    xs = [10 ** k for k in range(2, 7)]
    ax = plt.gca()
    ax.plot(xs, [smooth_share(x) for x in xs], 'o-', color=C1, label='share of n ≤ x with all primes ≤ √x')
    ax.axhline(1 - log(2), color=C2, ls='--', label='1 − log 2 ≈ 0.307')
    ax.set_xscale('log'); ax.legend(fontsize=8); ax.set_xlabel('x')
    save('09-e7')


# ---------- lesson 10 ----------
@fig('10-e1')
def _():
    fig_, ax = plt.subplots(figsize=(6.4, 2.6))
    ns = range(1, 101)
    ax.bar(ns, [1 if n % 5 == 0 else 0 for n in ns], color=C1, label='multiples of 5 (20)')
    ax.bar(ns, [1 if n % 25 == 0 else 0 for n in ns], bottom=[1 if n % 5 == 0 else 0 for n in ns], color=C2, label='multiples of 25 (4 extra)')
    ax.set_yticks([0, 1, 2]); ax.legend(fontsize=8); ax.set_xlabel('k in 100!'); ax.set_title('factors of 5 in 100!: 20 + 4 = 24 → 24 zeros')
    save('10-e1')


@fig('10-e2')
def _():
    f = factor(comb(20, 10))
    ps = [p for p in PR if p <= 20]
    ax = plt.gca()
    ax.bar([str(p) for p in ps], [f.get(p, 0) for p in ps], color=[C2 if p > 10 else C1 for p in ps])
    ax.set_ylabel('exponent in C(20,10) = 184756'); ax.set_title('every prime in (10, 20] divides C(20,10) once (red)')
    save('10-e2')


@fig('10-e3')
def _():
    from mpmath import li
    xs = np.logspace(2, 6.3, 60)
    pis = np.array([np.searchsorted(PR, x, side='right') for x in xs])
    ax = plt.gca()
    ax.plot(xs, xs / np.log(xs) / pis, color=C4, label='x / log x')
    ax.plot(xs, xs / (np.log(xs) - 1) / pis, color=C3, label='x / (log x − 1)')
    ax.plot(xs, [float(li(x) - li(2)) / p for x, p in zip(xs, pis)], color=C1, label='Li(x)')
    ax.axhline(1, color='k', lw=.6); ax.set_xscale('log'); ax.set_ylabel('approximation / π(x)'); ax.legend(fontsize=8); ax.set_xlabel('x')
    save('10-e3')


@fig('10-e4')
def _():
    ax = plt.gca()
    labels = ['100', '− singles\n(50+33+20+14)', '+ pairs', '− triples', '= φ(100,4)', '+ π(10) − 1']
    vals = [100, -117, 45, -6, 22, 3]
    run = 0; bottoms = []
    for i, v in enumerate(vals):
        if i == 4:
            bottoms.append(0); ax.bar(i, 22, color=C3); continue
        b = run if v >= 0 else run + v
        ax.bar(i, abs(v), bottom=b, color=C1 if v > 0 else C2); run += v
    ax.bar(5, 3, bottom=22, color=C4); ax.text(5, 26, 'π(100) = 25', ha='center')
    ax.set_xticks(range(6)); ax.set_xticklabels(labels, fontsize=7); ax.set_title('inclusion–exclusion for π(100)')
    save('10-e4')


# ---------- lesson 11 ----------
@fig('11-e1')
def _():
    ks = np.arange(1, 21)
    ax = plt.gca()
    ax.plot(ks, np.cumsum(1 / ks ** 4), 'o-', ms=3, color=C1, label='1 + 1/2⁴ + … + 1/k⁴')
    ax.axhline(pi ** 4 / 90, color=C2, ls='--', label='π⁴/90 ≈ 1.0823')
    ax.legend(fontsize=8); ax.set_xlabel('k')
    save('11-e1')


@fig('11-e2')
def _():
    from mpmath import zeta
    s = np.linspace(-9.5, 6, 800); s = s[np.abs(s - 1) > .06]
    ax = plt.gca()
    ax.plot(s, [float(zeta(x)) for x in s], color=C1)
    for n in range(0, 10):
        ax.scatter([-n], [float(zeta(-n))], color=C2 if n % 2 == 0 and n else C4, s=25, zorder=3)
    ax.annotate('ζ(−1) = −1/12', (-1, -1 / 12), xytext=(-10, -40), textcoords='offset points', arrowprops=dict(arrowstyle='->'), fontsize=8)
    ax.annotate('ζ(0) = −1/2', (0, -.5), xytext=(10, -30), textcoords='offset points', arrowprops=dict(arrowstyle='->'), fontsize=8)
    ax.axhline(0, color='k', lw=.5); ax.set_ylim(-1.5, 3); ax.set_xlabel('s (real)'); ax.set_title('ζ(s) on the real line: trivial zeros at −2, −4, …')
    save('11-e2')


@fig('11-e3')
def _():
    from mpmath import zeta
    s = np.linspace(1.2, 6, 200)
    ax = plt.gca()
    ax.plot(s, [float(zeta(x, .5)) for x in s], color=C1, lw=3, alpha=.5, label='ζ(s, 1/2)')
    ax.plot(s, [float((2 ** x - 1) * zeta(x)) for x in s], color=C2, ls='--', label='(2^s − 1) ζ(s)')
    ax.set_yscale('log'); ax.legend(fontsize=8); ax.set_xlabel('s')
    save('11-e3')


@fig('11-e4')
def _():
    M = 3000; d = dsum(M); xs = np.arange(1, M + 1)
    ax = plt.gca()
    ax.plot(xs, np.cumsum(d[1:]), color=C1, label='Σ d(n)')
    ax.plot(xs, xs * np.log(xs) + (2 * 0.5772 - 1) * xs, color=C2, ls='--', label='residue at s=1: x log x + (2γ−1)x')
    ax.legend(fontsize=8); ax.set_xlabel('x'); ax.set_title('Perron: the pole of ζ(s)² x^s/s gives the main term')
    save('11-e4')


@fig('11-e5')
def _():
    X = 100
    xs = np.linspace(1.5, X, 3000)
    lam = np.zeros(X + 1)
    for p in PR:
        if p > X: break
        k = p
        while k <= X:
            lam[k] = log(p); k *= p
    psi = np.cumsum(lam)
    ax = plt.gca()
    ax.step(range(X + 1), psi, where='post', color=C1, label='ψ(x)')
    ax.plot(xs, xs, color=C2, ls='--', label='x (pole of ζ at s = 1)')
    ax.legend(fontsize=8); ax.set_xlabel('x'); ax.set_title('the zeros of ζ create the jumps around the line x')
    save('11-e5')


# ---------- lesson 12 ----------
@fig('12-e1')
def _():
    from mpmath import zetazero
    zs = [complex(zetazero(k)) for k in range(1, 51)]
    X = 60
    xs = np.linspace(2, X, 1500)
    lam = np.zeros(X + 1)
    for p in PR:
        if p > X: break
        k = p
        while k <= X:
            lam[k] = log(p); k *= p
    psi = np.cumsum(lam)
    def approx(x, K):
        s = x - log(2 * pi) - .5 * np.log(1 - x ** -2.0)
        for r in zs[:K]:
            s -= 2 * (x ** r / r).real
        return s
    ax = plt.gca()
    ax.step(range(X + 1), psi, where='post', color='k', lw=1, label='ψ(x)')
    for K, c in ((3, C4), (50, C2)):
        ax.plot(xs, [approx(x, K) for x in xs], color=c, lw=.9, label=f'explicit formula, {K} pairs of zeros')
    ax.legend(fontsize=8); ax.set_xlabel('x')
    save('12-e1')


@fig('12-e2')
def _():
    from mpmath import zetazero
    zs = [float(zetazero(k).imag) for k in range(1, 30)]
    ax = plt.gca(); plt.gcf().set_size_inches(3.4, 4.8)
    ax.scatter([.5] * len(zs), zs, color=C2, s=14)
    ax.axvline(.5, color=GR, ls='--'); ax.axvline(0, color='k', lw=.5); ax.axvline(1, color='k', lw=.5)
    ax.set_xlim(-.2, 1.2); ax.set_ylim(0, 102); ax.set_xlabel('Re s'); ax.set_ylabel('Im s')
    ax.set_title('the 29 zeros with 0 < γ ≤ 100', fontsize=9)
    save('12-e2')


@fig('12-e3')
def _():
    from mpmath import siegelz
    t = np.linspace(10, 24, 400)
    ax = plt.gca()
    ax.plot(t, [float(siegelz(x)) for x in t], color=C1)
    ax.axhline(0, color='k', lw=.5)
    for a, b in ((14, 15), (20, 22)):
        ax.scatter([a, b], [float(siegelz(a)), float(siegelz(b))], color=C2, zorder=3)
    ax.set_xlabel('t'); ax.set_ylabel('Z(t)'); ax.set_title('Z(14) < 0 < Z(15) and Z(20) > 0 > Z(22): zeros at 14.13 and 21.02')
    save('12-e3')


@fig('12-e4')
def _():
    n = 12
    A = np.array([[1 if (j == 1 or j % i == 0) else 0 for j in range(1, n + 1)] for i in range(1, n + 1)])
    ax = plt.gca(); plt.gcf().set_size_inches(4.4, 4.2)
    ax.imshow(A, cmap='Blues')
    ax.add_patch(plt.Rectangle((-.5, -.5), 4, 4, fill=False, ec=C2, lw=2))
    ax.set_xticks(range(n)); ax.set_xticklabels(range(1, n + 1), fontsize=7); ax.set_yticks(range(n)); ax.set_yticklabels(range(1, n + 1), fontsize=7)
    ax.set_title('Redheffer A₁₂ (red: A₄, det = −1 = M(4))', fontsize=9)
    save('12-e4')


# ---------- lesson 13 ----------
@fig('13-e1')
def _():
    fig_, axs = plt.subplots(1, 4, figsize=(7.2, 2.2))
    vals = {0: [1, 1, 1, 1], 1: [1, 1j, -1j, -1], 2: [1, -1, -1, 1], 3: [1, -1j, 1j, -1]}
    for ax, (k, v) in zip(axs, vals.items()):
        ax.add_patch(plt.Circle((0, 0), 1, fill=False, color='#dddddd'))
        for n, z in zip((1, 2, 3, 4), v):
            ax.scatter(z.real if isinstance(z, complex) else z, z.imag if isinstance(z, complex) else 0, s=40, color=C1)
        for n, z in zip((1, 2, 3, 4), v):
            zz = complex(z)
            ax.annotate(str(n), (zz.real, zz.imag), xytext=(4, 4 + 6 * list(v).count(z) * 0), textcoords='offset points', fontsize=7)
        ax.set_xlim(-1.4, 1.4); ax.set_ylim(-1.4, 1.4); ax.set_aspect('equal'); ax.axis('off'); ax.set_title(f'χ{k} mod 5', fontsize=9)
    fig_.suptitle('values χ(n), n = 1..4, are 4th roots of unity', fontsize=9)
    save('13-e1')


@fig('13-e2')
def _():
    ks = np.arange(1, 101)
    ax = plt.gca()
    ax.plot(ks, np.cumsum([(-1) ** (k + 1) / (2 * k - 1) for k in ks]), color=C1, label='1 − 1/3 + 1/5 − …')
    ax.axhline(pi / 4, color=C2, ls='--', label='π/4')
    ax.legend(fontsize=8); ax.set_xlabel('terms')
    save('13-e2')


@fig('13-e3')
def _():
    ps = [p for p in PR if 2 < p < 100]
    ax = plt.gca()
    ax.step(ps, np.cumsum([1 if p % 4 == 1 else 0 for p in ps]), where='post', color=C1, label='≡ 1 (mod 4): 11')
    ax.step(ps, np.cumsum([1 if p % 4 == 3 else 0 for p in ps]), where='post', color=C2, label='≡ 3 (mod 4): 13')
    ax.step(ps, np.cumsum([1 if p % 4 == 1 else -1 for p in ps]), where='post', color=GR, label='Σ χ₄(p)')
    ax.legend(fontsize=8); ax.set_xlabel('x')
    save('13-e3')


@fig('13-e4')
def _():
    p = 101
    ax = plt.gca()
    ax.plot(range(1, p), np.cumsum([legendre(n, p) for n in range(1, p)]), color=C1, label='Σ_{n≤h} (n/101)')
    b = sqrt(p) * log(p)
    ax.axhline(b, color=C2, ls='--', label='±√p log p ≈ 46.4'); ax.axhline(-b, color=C2, ls='--')
    ax.legend(fontsize=8); ax.set_xlabel('h'); ax.set_title('the character sum never exceeds 7 in absolute value')
    save('13-e4')


@fig('13-e5')
def _():
    fig_, axs = plt.subplots(1, 2, figsize=(6.8, 2.8))
    for ax, p in zip(axs, (7, 23)):
        ch = [legendre(a, p) for a in range(1, p)]
        ax.bar(range(1, p), [a * c for a, c in zip(range(1, p), ch)], color=[C1 if c > 0 else C2 for c in ch])
        S = sum(a * c for a, c in zip(range(1, p), ch))
        ax.set_title(f'Σ a·(a/{p}) = {S} → h(−{p}) = {-S // p}', fontsize=9); ax.axhline(0, color='k', lw=.5)
    save('13-e5')


@fig('13-e6')
def _():
    ns = range(0, 46)
    vals = [n * n + n + 41 for n in ns]
    ax = plt.gca()
    ax.bar(ns, vals, color=[C3 if isp(v) else C2 for v in vals])
    ax.annotate('1681 = 41²', (40, 1681), xytext=(-80, 20), textcoords='offset points', arrowprops=dict(arrowstyle='->'), color=C2)
    ax.set_xlabel('n'); ax.set_ylabel('n² + n + 41'); ax.set_title('green = prime for n = 0..39')
    save('13-e6')


# ---------- lesson 14 ----------
@fig('14-e1')
def _():
    ax = plt.gca(); plt.gcf().set_size_inches(6.4, 3.4)
    for n in range(1, 201):
        r, c = (n - 1) // 25, (n - 1) % 25
        tw = isp(n) and isp(n + 2)
        ax.add_patch(plt.Rectangle((c, -r), .95, .95, fc=C2 if tw else ('#fde0dd' if isp(n) else '#f4f4f4')))
    ax.set_xlim(0, 25); ax.set_ylim(-7, 1); ax.set_aspect('equal'); ax.axis('off')
    ax.set_title('n ≤ 200 with n and n+2 both prime (red) — sieve dimension 2', fontsize=9)
    save('14-e1')


@fig('14-e2')
def _():
    ax = plt.gca(); plt.gcf().set_size_inches(5.4, 3.2)
    for n in range(1, 101):
        r, c = (n - 1) // 20, (n - 1) % 20
        ok = gcd(n, 30) == 1
        ax.add_patch(plt.Rectangle((c, -r), .95, .95, fc=C3 if ok else '#eeeeee'))
        ax.text(c + .47, -r + .47, str(n), ha='center', va='center', fontsize=6, color='w' if ok else 'k')
    ax.set_xlim(0, 20); ax.set_ylim(-4, 1); ax.set_aspect('equal'); ax.axis('off')
    ax.set_title('n ≤ 100 coprime to 30: 26 (expected 26.67)', fontsize=9)
    save('14-e2')


@fig('14-e3')
def _():
    y = 1000
    xs = np.arange(10 ** 6, 2 * 10 ** 6, y)
    cnt = [np.searchsorted(PR, x + y, side='right') - np.searchsorted(PR, x, side='right') for x in xs]
    ax = plt.gca()
    ax.plot(xs, cnt, color=C1, lw=.6, label='primes in (x, x+1000]')
    ax.axhline(2 * y / log(y), color=C2, ls='--', label='Selberg bound 2y/log y ≈ 290')
    ax.plot(xs, y / np.log(xs), color=C4, label='expected y/log x')
    ax.legend(fontsize=8); ax.set_xlabel('x')
    save('14-e3')


@fig('14-e4')
def _():
    Nn = 10000
    Qs = list(range(2, 60))
    alive = np.ones(Nn + 1, bool); alive[0] = False
    counts = []
    for Q in Qs:
        if isp(Q):
            qr = {x * x % Q for x in range(Q)}
            for n in range(1, Nn + 1):
                if alive[n] and n % Q not in qr:
                    alive[n] = False
        counts.append(alive.sum())
    ax = plt.gca()
    ax.plot(Qs, counts, 'o-', ms=3, color=C1, label='n ≤ 10⁴ that are squares mod every prime ≤ Q')
    ax.axhline(100, color=C2, ls='--', label='actual squares: 100')
    ax.set_yscale('log'); ax.legend(fontsize=8); ax.set_xlabel('Q')
    save('14-e4')


# ---------- lesson 15 ----------
@fig('15-e1')
def _():
    A = [k * k for k in range(1, 11)]
    al = np.linspace(0, 1, 3000)
    S = np.array([sum(np.exp(2j * pi * a * t) for a in A) for t in al])
    ax = plt.gca()
    ax.plot(al, np.abs(S), color=C1)
    for q in (2, 3, 4, 5):
        for a in range(q):
            if gcd(a, q) == 1:
                ax.axvline(a / q, color='#eeeeee', zorder=0)
    ax.set_xlabel('α'); ax.set_ylabel('|S(α)|, A = squares ≤ 100'); ax.set_title('peaks at fractions with small denominators (major arcs)')
    save('15-e1')


@fig('15-e2')
def _():
    Ns = np.arange(1, 2001)
    ax = plt.gca()
    for a, c, lab in ((sqrt(2), C1, 'α = √2'), (1 / 3, C2, 'α = 1/3')):
        ax.plot(Ns, np.abs(np.cumsum(np.exp(2j * pi * a * Ns ** 2))), color=c, lw=.8, label=lab)
    ax.plot(Ns, Ns, color=GR, ls='--', label='trivial bound N')
    ax.set_xscale('log'); ax.set_yscale('log'); ax.legend(fontsize=8); ax.set_xlabel('N'); ax.set_title('|Σ e(αn²)|: cancellation when α is irrational')
    save('15-e2')


@fig('15-e3')
def _():
    ps = [p for p in PR if 3 < p < 800]
    K = [sum(math.cos(2 * pi * ((x + pow(x, -1, p)) % p) / p) for x in range(1, p)) / sqrt(p) for p in ps]
    ax = plt.gca()
    ax.scatter(ps, K, s=6, color=C1)
    ax.axhline(2, color=C2, ls='--'); ax.axhline(-2, color=C2, ls='--')
    ax.set_xlabel('p'); ax.set_ylabel('K(1,1;p)/√p'); ax.set_title('Weil: always between −2 and 2')
    save('15-e3')


@fig('15-e4')
def _():
    fig_, ax = plt.subplots(figsize=(6.6, 2.0))
    left = 0
    for v, c in [(8, C1)] * 2 + [(1, C4)] * 7:
        ax.barh(0, v, left=left, color=c, ec='w'); left += v
    ax.text(8, .5, '2 × 8', ha='center'); ax.text(19.5, .5, '7 × 1', ha='center')
    ax.set_xlim(0, 24); ax.set_yticks([]); ax.set_ylim(-.6, .8); ax.set_xlabel('23 = 2·2³ + 7·1³: nine cubes (3³ = 27 > 23)')
    save('15-e4')


@fig('15-e5')
def _():
    ks = range(2, 11)
    ax = plt.gca()
    ax.plot(ks, [2 ** k + int(1.5 ** k) - 2 for k in ks], 'o-', color=C1, label='2^k + ⌊(3/2)^k⌋ − 2')
    ax.scatter([2, 3, 4], [4, 9, 19], color=C2, s=60, zorder=3, label='g(2)=4, g(3)=9, g(4)=19')
    ax.set_yscale('log'); ax.legend(fontsize=8); ax.set_xlabel('k')
    save('15-e5')


@fig('15-e6')
def _():
    ax = plt.gca(); plt.gcf().set_size_inches(4.6, 4.4)
    ps = [p for p in PR if p < 100]
    ax.scatter([p for p in ps for q in ps], [q for p in ps for q in ps], s=4, color=GR)
    xs = np.linspace(0, 100, 10); ax.plot(xs, 100 - xs, color=C1, label='p + q = 100')
    hits = [(p, 100 - p) for p in ps if isp(100 - p)]
    ax.scatter(*zip(*hits), color=C2, s=30, zorder=3)
    ax.set_aspect('equal'); ax.set_xlabel('p'); ax.set_ylabel('q'); ax.legend(fontsize=8)
    ax.set_title('prime grid: 100 = p + q in 6 ways (12 ordered points)', fontsize=9)
    save('15-e6')


# ---------- lesson 16 ----------
@fig('16-e1')
def _():
    ps = [p for p in PR if p > 2 and p < 3000]
    vals = np.cumprod([p * (p - 2) / (p - 1) ** 2 for p in ps])
    ax = plt.gca()
    ax.plot(ps, vals, color=C1, label='partial product over p ≤ x')
    ax.axhline(0.6601618, color=C2, ls='--', label='C₂ = 0.66016…')
    ax.set_xscale('log'); ax.legend(fontsize=8); ax.set_xlabel('x')
    save('16-e1')


@fig('16-e2')
def _():
    xs = np.logspace(3, 6, 40)
    c2 = np.cumsum([1 if (isp(n) and isp(n + 2)) else 0 for n in range(1, 1_000_001)])
    c6 = np.cumsum([1 if (isp(n) and isp(n + 6)) else 0 for n in range(1, 1_000_001)])
    ax = plt.gca()
    ax.plot(xs, [c6[int(x) - 1] / c2[int(x) - 1] for x in xs], 'o-', ms=3, color=C1)
    ax.axhline(2, color=C2, ls='--'); ax.set_xscale('log'); ax.set_xlabel('x'); ax.set_ylabel('#(p, p+6) / #(p, p+2)')
    ax.set_title('the ratio tends to 2 (the factor of p = 3)')
    save('16-e2')


@fig('16-e3')
def _():
    xs = np.arange(1, 1_000_001)
    ax = plt.gca()
    for pat, c in (((0, 2, 4), C2), ((0, 2, 6), C1), ((0, 4, 6), C3)):
        cnt = np.cumsum([1 if all(isp(n + h) for h in pat) else 0 for n in range(1, 1_000_001)])
        ax.plot(xs[::1000], cnt[::1000], color=c, label=str(pat))
    ax.set_xscale('log'); ax.set_yscale('symlog'); ax.legend(fontsize=8); ax.set_xlabel('x'); ax.set_title('(0,2,4) stops at (3,5,7); the admissible patterns keep going')
    save('16-e3')


@fig('16-e4')
def _():
    from mpmath import li
    xs = np.logspace(1, 4, 30)
    def isprime(m):
        if m <= N: return isp(m)
        return all(m % p for p in PR if p * p <= m)
    cnt = np.cumsum([1 if isprime(n * n + 1) else 0 for n in range(1, 10001)])
    ax = plt.gca()
    ax.plot(xs, [cnt[int(x) - 1] for x in xs], 'o', ms=3, color=C1, label='n ≤ x with n²+1 prime')
    ax.plot(xs, [1.3728 / 2 * float(li(x) - li(2)) for x in xs], color=C2, label='Bateman–Horn (C/2)·Li(x)')
    ax.set_xscale('log'); ax.set_yscale('log'); ax.legend(fontsize=8); ax.set_xlabel('x')
    save('16-e4')


@fig('16-e5')
def _():
    g = 0; rec = []
    for i in range(len(PR) - 1):
        d = PR[i + 1] - PR[i]
        if d > g:
            g = d; rec.append((PR[i], d))
    ax = plt.gca()
    ax.scatter([r[0] for r in rec], [r[1] for r in rec], color=C1, s=18, label='record gaps')
    xs = np.logspace(.5, 6.3, 100); ax.plot(xs, np.log(xs) ** 2, color=C2, ls='--', label='log² p (Cramér)')
    ax.set_xscale('log'); ax.legend(fontsize=8); ax.set_xlabel('p')
    save('16-e5')


@fig('16-e6')
def _():
    ps = np.array(PR[:20000], dtype=float)
    ax = plt.gca()
    ax.scatter(ps[:-1], np.sqrt(ps[1:]) - np.sqrt(ps[:-1]), s=1, color=C1)
    ax.scatter([7], [sqrt(11) - sqrt(7)], color=C2, s=50, zorder=3); ax.annotate('p = 7: 0.6709', (7, .6709), xytext=(8, -4), textcoords='offset points', color=C2)
    ax.axhline(1, color='k', ls='--', lw=.6); ax.set_xscale('log'); ax.set_xlabel('pₙ'); ax.set_ylabel('√pₙ₊₁ − √pₙ'); ax.set_title('Andrica: always below 1')
    save('16-e6')




@fig('08-lr')
def _():
    X = 10 ** 7
    s = np.zeros(X, dtype=bool)
    for a in range(int(sqrt(X)) + 1):
        c = np.arange(a, int(sqrt(max(X - 1 - a * a, 0))) + 1)
        s[a * a + c * c] = True
    s[0] = False
    cum = np.cumsum(s)
    xs = np.unique(np.logspace(2, 7, 60).astype(int) - 1)
    r = cum[xs] / (xs / np.sqrt(np.log(xs)))
    ax = plt.gca()
    ax.semilogx(xs, r, color=C1, label='N(x) / (x/√log x)')
    ax.axhline(0.7642236536, color=C2, ls='--', label='b ≈ 0.76422')
    ax.set_xlabel('x'); ax.set_ylim(0.7, 0.95); ax.legend()
    ax.set_title('Sums of two squares below x: slow convergence to b')
    save('08-lr')


@fig('16-op')
def _():
    ns = np.arange(2, 61)
    lo = [sum(isp(k) for k in range(n * n - n + 1, n * n)) for n in ns]
    hi = [sum(isp(k) for k in range(n * n + 1, n * n + n)) for n in ns]
    ax = plt.gca()
    ax.bar(ns - .2, lo, .4, color=C1, label='primes in (n²−n, n²)')
    ax.bar(ns + .2, hi, .4, color=C3, label='primes in (n², n²+n)')
    ax.axhline(1, color=C2, ls='--', lw=1)
    ax.set_xlabel('n'); ax.set_ylabel('count'); ax.legend()
    ax.set_title("Oppermann: neither bar ever drops to 0")
    save('16-op')


@fig('06-7')
def _():
    n = 12
    ks = np.arange(1, n + 1)
    g = [gcd(int(k), n) for k in ks]
    fig_, axs = plt.subplots(1, 2, figsize=(6.8, 3.0))
    cols = {1: GR, 2: C1, 3: C3, 4: C4, 6: C2, 12: 'k'}
    axs[0].bar(ks, g, color=[cols[v] for v in g])
    axs[0].set_xticks(ks); axs[0].set_xlabel('k'); axs[0].set_title('gcd(k, 12): sum = P(12) = 40', fontsize=9)
    ns = np.arange(1, 301)
    P = [sum(gcd(int(k), int(m)) for k in range(1, m + 1)) for m in ns]
    pr = [isp(int(m)) for m in ns]
    axs[1].scatter(ns, np.array(P) / ns, s=6, c=[C2 if q else C1 for q in pr])
    axs[1].set_xlabel('n'); axs[1].set_title('P(n)/n (red: primes, = 2 − 1/n)', fontsize=9)
    save('06-7')


@fig('05-cm')
def _():
    N = 4000
    ph = list(range(N + 1))
    for p in range(2, N + 1):
        if ph[p] == p:
            for k in range(p, N + 1, p):
                ph[k] -= ph[k] // p
    A = {}
    for m in range(1, N + 1):
        A[ph[m]] = A.get(ph[m], 0) + 1
    ks = [k for k in range(1, 201) if k in A]
    ax = plt.gca()
    ax.bar(ks, [A[k] for k in ks], color=C1, width=1.6)
    ax.axhline(1, color=C2, ls='--', lw=1)
    ax.set_xlabel('k'); ax.set_ylabel('A(k) = #{n : φ(n) = k}')
    ax.set_title('Carmichael: A(k) is never exactly 1 (dashed line)')
    save('05-cm')



if __name__ == '__main__':
    import sys
    keys = sys.argv[1:] or sorted(FIGS)
    for k in keys:
        FIGS[k]()
    print('drew', len(keys), 'figures into', OUT)

