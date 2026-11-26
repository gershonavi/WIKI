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
        ax.annotate(str(labels[k] if labels else k), (x * 1.16, y * 1.16), ha='center', va='center', fontsize=9, annotation_clip=False)
    ax.set_xlim(-1.3 * r, 1.3 * r); ax.set_ylim(-1.3 * r, 1.3 * r)
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


@fig('07-7')
def _():
    fig_, axs = plt.subplots(1, 2, figsize=(6.8, 3.0))
    for ax, p in zip(axs, (97, 1537)):
        x, e, ch, ex = pow(5, 3, p), 3, [], []
        ch.append(x); ex.append(e)
        while e * 2 <= (p - 1) // 2:
            x = x * x % p; e *= 2; ch.append(x); ex.append(e)
        cols = [C1] * (len(ch) - 1) + [C3 if ch[-1] == p - 1 else C2]
        ax.bar(range(len(ch)), ch, color=cols)
        ax.axhline(p - 1, color='k', ls='--', lw=.8)
        ax.set_xticks(range(len(ch))); ax.set_xticklabels([str(v) for v in ex], fontsize=7, rotation=45)
        ax.set_xlabel('exponent e  (value 5^e mod p)', fontsize=8)
        ax.set_title(f'p = {p}: last = {ch[-1]}' + (' = p−1 → prime' if ch[-1] == p - 1 else ' ≠ p−1 → composite'), fontsize=9)
    save('07-7')


@fig('09-ew')
def _():
    N = 200000
    ph = np.arange(N + 1, dtype=float)
    for p in range(2, N + 1):
        if ph[p] == p:
            ph[p::p] *= (1 - 1 / p)
    r = np.sort(ph[1:] / np.arange(1, N + 1))
    ax = plt.gca()
    ax.plot(r, np.arange(1, N + 1) / N, color=C1)
    ax.axvline(6 / pi ** 2, color=C2, ls='--', lw=1, label='mean 6/π² ≈ 0.608')
    ax.set_xlabel('y'); ax.set_ylabel('share of n ≤ 200000 with φ(n)/n ≤ y')
    ax.set_title('Erdős–Wintner: φ(n)/n has a continuous limiting distribution'); ax.legend()
    save('09-ew')


@fig('09-6')
def _():
    fig_, axs = plt.subplots(1, 2, figsize=(6.8, 3.0))
    ds = divisors(24)
    ax = axs[0]
    ax.scatter(np.log(ds), [0] * len(ds), color=C1, zorder=3)
    for d in ds:
        ax.annotate(str(d), (log(d), 0.05), ha='center', fontsize=8)
    ax.axvspan(log(3), log(3) + 1, color=C3, alpha=.3, label='[3, 3e]: 4 divisors')
    ax.set_yticks([]); ax.set_ylim(-.3, .4); ax.set_xlabel('log d'); ax.legend(fontsize=7, loc='lower right')
    ax.set_title('divisors of 24 on a log scale; window of width 1', fontsize=9)
    def D(n):
        dd = divisors(n)
        return max(sum(1 for x in dd if u <= x <= math.e * u) for u in dd)
    ns = np.arange(1, 241)
    axs[1].bar(ns, [D(int(n)) for n in ns], color=C1, width=1)
    axs[1].set_xlabel('n'); axs[1].set_title('Δ(n) for n ≤ 240', fontsize=9)
    save('09-6')


@fig('01-7')
def _():
    fig_, axs = plt.subplots(1, 3, figsize=(6.8, 2.6))
    for ax, run in zip(axs, ([4, 5, 6], [1, 2, 3, 4, 5], [7, 8])):
        for i, v in enumerate(run):
            for j in range(v):
                ax.add_patch(plt.Rectangle((i, j), .9, .9, color=C1 if len(run) % 2 else C3))
        ax.set_xlim(-.2, 5.2); ax.set_ylim(-.2, 8.4); ax.set_aspect('equal'); ax.axis('off')
        ax.set_title(' + '.join(map(str, run)) + ' = 15', fontsize=9)
    save('01-7')


@fig('08-15')
def _():
    v = set()
    for w in range(0, 9):
        for x in range(0, 6):
            for y in range(0, 4):
                for z in range(0, 4):
                    v.add(w * w + 2 * x * x + 5 * y * y + 5 * z * z)
    ns = np.arange(1, 61)
    ax = plt.gca()
    ax.bar(ns, [1] * len(ns), color=[C3 if n in v else C2 for n in ns], width=.85)
    ax.annotate('15', (15, 1.05), ha='center', color=C2)
    ax.set_yticks([]); ax.set_ylim(0, 1.3); ax.set_xlabel('n')
    ax.set_title('w² + 2x² + 5y² + 5z² takes every value except 15 (red)')
    save('08-15')


@fig('15-ro')
def _():
    N = 10 ** 6
    S = np.zeros(N + 1, bool)
    S[[p for p in PR if p <= N]] = True
    rep = np.zeros(N + 1, bool)
    k = 1
    while 2 ** k < N:
        rep[2 ** k:] |= S[:N + 1 - 2 ** k]; k += 1
    xs = np.unique(np.logspace(2, 6, 60).astype(int))
    c = np.cumsum(rep)
    ax = plt.gca()
    ax.semilogx(xs, c[xs] / xs, color=C1, label='share of n ≤ x of the form p + 2^k')
    ax.axhline(0.5, color='k', ls=':', lw=1, label='0.5 (all odd numbers)')
    ax.axhline(0.107648, color=C2, ls='--', lw=1, label='proven lower bound 0.1076')
    ax.set_xlabel('x'); ax.set_ylim(0, 0.6); ax.legend(fontsize=7)
    ax.set_title('Romanov: a positive proportion of integers are p + 2^k')
    save('15-ro')


@fig('04-7')
def _():
    fig_, axs = plt.subplots(1, 2, figsize=(6.8, 2.8))
    xs = np.arange(9)
    cub = [pow(int(x), 3, 9) for x in xs]
    axs[0].bar(xs, [c if c < 5 else c - 9 for c in cub], color=C1)
    axs[0].set_xticks(xs); axs[0].set_xlabel('x mod 9'); axs[0].axhline(0, color='k', lw=.5)
    axs[0].set_title('x³ mod 9 ∈ {0, 1, −1}', fontsize=9)
    sums = {(a + b + c) % 9 for a in (0, 1, 8) for b in (0, 1, 8) for c in (0, 1, 8)}
    axs[1].bar(range(9), [1] * 9, color=[C3 if r in sums else C2 for r in range(9)])
    axs[1].set_xticks(range(9)); axs[1].set_yticks([]); axs[1].set_xlabel('n mod 9')
    axs[1].set_title('sums of three cubes mod 9: never 4 or 5 (red)', fontsize=9)
    save('04-7')


@fig('08-7')
def _():
    from mpl_toolkits.mplot3d import Axes3D  # noqa: F401
    fig_ = plt.figure(figsize=(6.8, 3.0))
    ax = fig_.add_subplot(1, 2, 1, projection='3d')
    a, b, c = 1, 2, 2
    for (x0, y0, z0), (x1, y1, z1) in [((0,0,0),(a,0,0)),((0,0,0),(0,b,0)),((0,0,0),(0,0,c)),((a,0,0),(a,b,0)),((a,0,0),(a,0,c)),((0,b,0),(a,b,0)),((0,b,0),(0,b,c)),((0,0,c),(a,0,c)),((0,0,c),(0,b,c)),((a,b,0),(a,b,c)),((a,0,c),(a,b,c)),((0,b,c),(a,b,c))]:
        ax.plot([x0, x1], [y0, y1], [z0, z1], color=C1)
    ax.plot([0, a], [0, b], [0, c], color=C2, lw=2)
    ax.set_title('box 1×2×2, diagonal 3', fontsize=9); ax.set_xticks([]); ax.set_yticks([]); ax.set_zticks([])
    ax2 = fig_.add_subplot(1, 2, 2)
    from math import gcd as g
    ds = {}
    for x in range(1, 60):
        for y in range(x, 60):
            for z in range(y, 60):
                d2 = x * x + y * y + z * z; d = math.isqrt(d2)
                if d * d == d2 and d < 60 and g(g(x, y), g(z, d)) == 1:
                    ds[d] = ds.get(d, 0) + 1
    ks = sorted(ds)
    ax2.bar(ks, [ds[k] for k in ks], color=C1, width=1.2)
    ax2.set_xlabel('d (always odd)'); ax2.set_title('primitive quadruples with norm d', fontsize=9)
    save('08-7')


@fig('15-6')
def _():
    rng = np.random.default_rng(7)
    N = 200000
    m = np.arange(N + 1, dtype=float)
    pr = np.zeros(N + 1)
    pr[3:] = np.minimum(1, 1.2 * m[3:] ** -0.5 * np.sqrt(np.log(m[3:])))
    pr[:3] = 1
    B = rng.random(N + 1) < pr
    ind = B.astype(float)
    r = np.rint(np.fft.irfft(np.fft.rfft(ind, 2 * N + 2) ** 2, 2 * N + 2)[:N + 1])
    sq = np.zeros(N + 1); sq[np.arange(int(np.sqrt(N)) + 1) ** 2] = 1
    rs = np.rint(np.fft.irfft(np.fft.rfft(sq, 2 * N + 2) ** 2, 2 * N + 2)[:N + 1])
    ns = np.arange(1000, N + 1, 997)
    ax = plt.gca()
    ax.scatter(ns, r[ns], s=4, color=C1, label='random basis B (|B∩[1,x]| ≈ √x·√log x)')
    cst = float(np.mean(r[ns] / np.log(ns)))
    ax.plot(ns, cst * np.log(ns), color=C2, lw=1.5, label=f'{cst:.1f} · log n (fit)')
    ax.scatter(ns, rs[ns], s=4, color=GR, label='squares: often 0')
    ax.set_xlabel('n'); ax.set_ylabel('r(n) = #{(a,b): a+b=n}')
    ax.set_title('An Erdős-type random basis of order 2: r(n) ≍ log n', fontsize=10)
    ax.legend(fontsize=7)
    save('15-6')


@fig('16-ma')
def _():
    N = 2 * 10 ** 6 - 1000
    c = np.concatenate([[0], np.cumsum([isp(int(k)) for k in range(1, N + 2)])])
    xs = np.arange(200000, N - 400, 97)
    h = (np.log(xs) ** 2).astype(int)
    real = (c[xs + h] - c[xs]) / np.log(xs)
    rng = np.random.default_rng(3)
    model = rng.binomial(h, 1 / np.log(xs)) / np.log(xs)
    ax = plt.gca()
    bins = np.linspace(0, 2.2, 45)
    ax.hist(model, bins, color=GR, alpha=.6, label='Cramér model (independent coins)')
    ax.hist(real, bins, histtype='step', color=C1, lw=2, label='real primes')
    ax.axvline(1, color=C2, ls='--', lw=1)
    ax.set_xlabel('(π(x + log²x) − π(x)) / log x'); ax.set_yticks([])
    ax.set_title('Primes in short intervals vs. Cramér\'s model', fontsize=10); ax.legend(fontsize=7)
    save('16-ma')


@fig('11-6')
def _():
    from fractions import Fraction as Fr
    from math import comb
    import mpmath
    mpmath.mp.dps = 60
    z3 = mpmath.zeta(3)
    ns = range(1, 13)
    ap, ps = [], []
    for n in ns:
        cnk = lambda k: sum(Fr(1, m ** 3) for m in range(1, n + 1)) + sum(Fr((-1) ** (m - 1), 2 * m ** 3 * comb(n, m) * comb(n + m, m)) for m in range(1, k + 1))
        b = sum(comb(n, k) ** 2 * comb(n + k, k) ** 2 for k in range(n + 1))
        a = sum(cnk(k) * comb(n, k) ** 2 * comb(n + k, k) ** 2 for k in range(n + 1))
        ap.append(float(abs(mpmath.mpf(a.numerator) / a.denominator / b - z3)))
        ps.append(float(abs(mpmath.fsum(mpmath.mpf(1) / m ** 3 for m in range(1, n + 1)) - z3)))
    ax = plt.gca()
    ax.semilogy(list(ns), ap, 'o-', color=C1, label='Apéry: a_n / b_n')
    ax.semilogy(list(ns), ps, 's-', color=GR, label='partial sums Σ 1/m³')
    ax.semilogy(list(ns), [(np.sqrt(2) - 1) ** (8 * n) for n in ns], '--', color=C2, lw=1, label='(√2 − 1)^{8n} ≈ 0.00087^n')
    ax.set_xlabel('n'); ax.set_ylabel('error |· − ζ(3)|'); ax.legend(fontsize=7)
    ax.set_title('Apéry\'s approximations to ζ(3) gain ~3 digits per step', fontsize=10)
    save('11-6')


@fig('15-po')
def _():
    N = 1000
    T = [n * (n + 1) * (n + 2) // 6 for n in range(1, 30) if n * (n + 1) * (n + 2) // 6 <= N]
    d = np.full(N + 1, 99); d[0] = 0
    for m in range(1, N + 1):
        d[m] = 1 + min(d[m - t] for t in T if t <= m)
    ns = np.arange(1, N + 1)
    cols = {1: '#bbbbbb', 2: C3, 3: C1, 4: C4, 5: C2}
    ax = plt.gca()
    ax.scatter(ns, d[1:], s=6, c=[cols[int(v)] for v in d[1:]])
    ax.set_yticks([1, 2, 3, 4, 5]); ax.set_ylim(0.5, 5.6)
    ax.set_xlabel('n'); ax.set_ylabel('fewest tetrahedral numbers')
    ax.set_title('Pollock: every n needs at most 5 tetrahedral numbers (1, 4, 10, 20, ...)', fontsize=9)
    save('15-po')


@fig('09-7')
def _():
    N = 300000
    c2 = np.zeros(N + 1, int)
    sv = np.ones(N + 1, bool); sv[:2] = False
    for p in range(2, int(N ** .5) + 1):
        if sv[p]:
            sv[p * p::p] = False
            c2[p * p::p * p] += 1
    even = (c2[1:] % 2 == 0)
    xs = np.unique(np.logspace(1, np.log10(N), 80).astype(int))
    cum = np.cumsum(even)
    ax = plt.gca()
    ax.semilogx(xs, cum[xs - 1] / xs, color=C1, label='share with ω₂(k) even')
    ax.axhline(0.66131705, color=C2, ls='--', lw=1, label='C_FT = ½(1 + ∏(1 − 2/p²)) ≈ 0.6613')
    ax.axhline(6 / pi ** 2, color=GR, ls=':', lw=1, label='squarefree only: 6/π² ≈ 0.6079')
    ax.set_xlabel('x'); ax.set_ylim(0.55, 0.75); ax.legend(fontsize=7)
    ax.set_title('Feller–Tornier: an even number of primes with p² | k', fontsize=10)
    save('09-7')


@fig('02-7')
def _():
    F = [0, 1]
    for _ in range(40):
        F.append(F[-1] + F[-2])
    M = 24
    G = np.array([[gcd(F[m], F[n]) == F[gcd(m, n)] for n in range(1, M + 1)] for m in range(1, M + 1)])
    V = np.array([[gcd(m, n) for n in range(1, M + 1)] for m in range(1, M + 1)])
    ax = plt.gca()
    im = ax.imshow(V, origin='lower', cmap='viridis', extent=(0.5, M + .5, 0.5, M + .5))
    plt.colorbar(im, ax=ax, fraction=.046, label='gcd(m, n)')
    ax.set_xlabel('n'); ax.set_ylabel('m')
    ax.set_title(f'gcd(F_m, F_n) = F_gcd(m,n): holds in all {G.sum()} of {M*M} cells', fontsize=9)
    save('02-7')


@fig('16-fi')
def _():
    X = 10 ** 6
    pts = []
    b = 1
    while b ** 4 < X:
        a = 1
        while a * a + b ** 4 <= X:
            if isp(a * a + b ** 4):
                pts.append((a, b))
            a += 1
        b += 1
    A = np.array(pts)
    fig_, axs = plt.subplots(1, 2, figsize=(6.8, 3.0))
    axs[0].scatter(A[:, 0], A[:, 1], s=1, color=C1)
    axs[0].set_xlabel('a'); axs[0].set_ylabel('b'); axs[0].set_title('a² + b⁴ prime, ≤ 10⁶', fontsize=9)
    xs = np.unique(np.logspace(2, 6, 40).astype(int))
    vals = np.array([a * a + b ** 4 for a, b in pts])
    cnt = [4 * (vals <= x).sum() for x in xs]
    axs[1].loglog(xs, cnt, 'o', ms=3, color=C1, label='count (a, b ∈ ℤ)')
    axs[1].loglog(xs, 4.798 * xs ** 0.75 / np.log(xs), color=C2, label='4.80·x^{3/4}/log x')
    axs[1].set_xlabel('x'); axs[1].legend(fontsize=7); axs[1].set_title('Friedlander–Iwaniec asymptotic', fontsize=9)
    save('16-fi')


@fig('14-jr')
def _():
    g = 0.5772156649015329
    h = 1e-3
    s = np.arange(1, 8 + h / 2, h)
    F = np.zeros_like(s); f = np.zeros_like(s)
    for i, t in enumerate(s):
        if t <= 3:
            F[i] = 2 * np.exp(g) / t
        if t <= 2:
            f[i] = 0
        elif t <= 4:
            f[i] = 2 * np.exp(g) * np.log(t - 1) / t
    k = int(round(1 / h))
    # (sF)' = f(s-1) for s > 3 ; (sf)' = F(s-1) for s > 4
    sF = s * F; sf = s * f
    for i in range(len(s)):
        t = s[i]
        if t > 3 + h / 2:
            sF[i] = sF[i - 1] + h * f[i - k]
            F[i] = sF[i] / t
        if t > 4 + h / 2:
            sf[i] = sf[i - 1] + h * F[i - k]
            f[i] = sf[i] / t
    ax = plt.gca()
    ax.plot(s, F, color=C2, label='F(s): upper bound factor')
    ax.plot(s, f, color=C1, label='f(s): lower bound factor')
    ax.axhline(1, color='k', lw=.6, ls=':')
    ax.axvline(2, color=GR, lw=.8, ls='--')
    ax.set_xlabel('s = log y / log z'); ax.set_ylim(0, 2.5); ax.legend(fontsize=8)
    ax.set_title('Linear sieve: f(s) ≤ 1 ≤ F(s); the lower bound is 0 until s = 2', fontsize=9)
    save('14-jr')


@fig('14-bdh')
def _():
    x = 10 ** 6
    P = np.array([p for p in PR if p <= x]); L = np.log(P)
    Qmax = 2000
    ph = list(range(Qmax + 1))
    for p in range(2, Qmax + 1):
        if ph[p] == p:
            for k in range(p, Qmax + 1, p):
                ph[k] -= ph[k] // p
    V = 0.0; qs = []; rat = []
    for q in range(1, Qmax + 1):
        th = np.bincount(P % q, weights=L, minlength=q)
        a = np.array([gcd(r, q) == 1 for r in range(q)])
        V += ((th[a] - x / ph[q]) ** 2).sum()
        qs.append(q); rat.append(V / (q * x * np.log(x)))
    ax = plt.gca()
    ax.semilogx(qs, rat, color=C1)
    ax.axhline(1, color=C2, ls='--', lw=1, label='Q·x·log x')
    ax.set_xlabel('Q'); ax.set_ylabel('V(x, Q) / (Q x log x)'); ax.set_ylim(0, 1.2); ax.legend(fontsize=8)
    ax.set_title('Barban–Davenport–Halberstam at x = 10⁶: the variance stays below Q x log x', fontsize=9)
    save('14-bdh')


@fig('15-7')
def _():
    def J(X):
        x = np.arange(1, X + 1)
        a, b, c = np.meshgrid(x, x, x, indexing='ij')
        key = (a + b + c) * (3 * X * X + 1) + (a * a + b * b + c * c)
        _, cnt = np.unique(key.ravel(), return_counts=True)
        return float((cnt.astype(np.int64) ** 2).sum())
    Xs = [5, 8, 12, 16, 24, 32, 48, 64, 80]
    vals = [J(X) / X ** 3 for X in Xs]
    ax = plt.gca()
    ax.semilogx(Xs, vals, 'o-', color=C1, label='J_{3,2}(X) / X³')
    sl = np.polyfit(np.log(Xs[3:]), vals[3:], 1)
    ax.semilogx(Xs, np.polyval(sl, np.log(Xs)), '--', color=C2, lw=1, label=f'≈ {sl[0]:.2f}·log X + {sl[1]:.2f}')
    ax.set_xlabel('X'); ax.legend(fontsize=8)
    ax.set_title('Critical case s = k(k+1)/2 = 3, k = 2: J grows like X³ log X', fontsize=9)
    save('15-7')


@fig('09-8')
def _():
    N = 100000
    ts = np.linspace(0, 1, 101)
    divs = [[] for _ in range(N + 1)]
    for d in range(1, N + 1):
        for m in range(d, N + 1, d):
            divs[m].append(d)
    acc = np.zeros_like(ts)
    for n in range(2, N + 1):
        L = np.log(np.array(divs[n])) / np.log(n)
        acc += np.searchsorted(np.sort(L), ts + 1e-12, side='right') / len(L)
    acc /= N
    ax = plt.gca()
    ax.plot(ts, acc, color=C1, label='average of P(D_n ≤ t), n ≤ 10⁵')
    ax.plot(ts, 2 / np.pi * np.arcsin(np.sqrt(ts)), '--', color=C2, label='(2/π) arcsin √t')
    ax.plot(ts, ts, ':', color=GR, lw=1, label='uniform')
    ax.set_xlabel('t'); ax.legend(fontsize=8)
    ax.set_title('Deshouillers–Dress–Tenenbaum: log d / log n follows the arcsine law', fontsize=9)
    save('09-8')




# ================= proof-methods course (P01–P06) =================
def _grid_table(ax, rows, cols, cell, title, hl=None, rlab='', clab=''):
    """cell(r,c) -> text; hl(r,c) -> facecolor or None"""
    for i, r in enumerate(rows):
        ax.text(-0.5, -i, str(r), ha='center', va='center', fontsize=9, weight='bold')
        for j, c in enumerate(cols):
            fc = (hl(r, c) if hl else None) or 'white'
            ax.add_patch(plt.Rectangle((j, -i - .5), 1, 1, fc=fc, ec='#bbbbbb'))
            ax.text(j + .5, -i, str(cell(r, c)), ha='center', va='center', fontsize=9)
    for j, c in enumerate(cols):
        ax.text(j + .5, .85, str(c), ha='center', va='center', fontsize=9, weight='bold')
    ax.text(-0.5, .85, rlab + '\\' + clab if rlab else '', ha='center', va='center', fontsize=8, color=GR)
    ax.set_xlim(-1.1, len(cols) + .1); ax.set_ylim(-len(rows) + .3, 1.4)
    ax.set_aspect('equal'); ax.axis('off'); ax.set_title(title, fontsize=9)


@fig('P01-e1')
def _():
    ax = plt.gca()
    a, b = 4, 3
    for k in range(a):
        ax.scatter([k, k], [1, 0], s=70, color=C1)
    ax.scatter([a], [1], s=70, color=C2)
    for k in range(b):
        ax.scatter([k + a + 1.6, k + a + 1.6], [1, 0], s=70, color=C3)
    ax.scatter([a + b + 1.6], [1], s=70, color=C2)
    ax.text(a / 2, -0.8, '2a + 1 = 9', ha='center'); ax.text(a + 1.6 + b / 2, -0.8, '2b + 1 = 7', ha='center')
    ax.annotate('', xy=(a + b + 1.6, 0.05), xytext=(a, 0.95), arrowprops=dict(arrowstyle='->', color=C2, lw=1.5, connectionstyle='arc3,rad=-0.2'))
    ax.text(a + 1.2, 0.35, 'the two leftover dots\nform one more pair', color=C2, fontsize=8)
    ax.set_xlim(-1, 11); ax.set_ylim(-1.2, 1.7); ax.axis('off')
    ax.set_title('odd + odd: every dot gets a partner, so the sum 2(a+b+1) is even', fontsize=9)
    save('P01-e1')


@fig('P01-e2')
def _():
    ax = plt.gca()
    ns = np.arange(1, 13)
    for n in ns:
        ax.bar(n - .18, n, .36, color=C1 if n % 2 == 0 else '#c6dbef')
        ax.bar(n + .18, n + 1, .36, color=C1 if (n + 1) % 2 == 0 else '#c6dbef')
        ax.text(n, n + 1.6, str(n * (n + 1)), ha='center', fontsize=7)
    ax.set_xticks(ns); ax.set_xlabel('n   (left bar: n, right bar: n+1; dark = even)')
    ax.set_title('n(n+1): in each pair exactly one factor is even, so the product (on top) is even', fontsize=9)
    save('P01-e2')


@fig('P01-e3')
def _():
    ax = plt.gca()
    rows = list(range(2, 11))
    cols = ['n-1', 'n', 'n+1']
    vals = lambda n, c: {'n-1': n - 1, 'n': n, 'n+1': n + 1}[c]
    def hl(n, c):
        v = vals(n, c)
        if v % 3 == 0 and v % 2 == 0: return '#c7b3e5'
        if v % 3 == 0: return '#fdd0a2'
        if v % 2 == 0: return '#c6dbef'
    _grid_table(ax, rows, cols, vals, '', hl)
    for i, n in enumerate(rows):
        ax.text(3.3, -i, f'n³−n = {n**3 - n} = 6·{(n**3 - n)//6}', va='center', fontsize=8)
    ax.set_xlim(-1.1, 8)
    ax.set_title('three consecutive numbers: one is ≡0 mod 3 (orange), one is even (blue); purple = both', fontsize=9)
    save('P01-e3')


@fig('P01-x1')
def _():
    ax = plt.gca()
    a, b, c = 4, 12, 20
    xs = np.arange(0, 37)
    ax.plot([0, 36], [0, 0], color=GR, lw=1)
    for x in xs:
        ax.plot([x, x], [-.08, .08], color='#cccccc', lw=.8)
    ax.scatter(xs[::a], 0 * xs[::a], s=40, color=C1, zorder=3, label='multiples of a = 4')
    for v, name, col, y in [(b, 'b = 12', C3, .5), (c, 'c = 20', C4, .5), (b + c, 'b + c = 32', C2, .5)]:
        ax.annotate(name, (v, 0.05), (v, y), ha='center', color=col, arrowprops=dict(arrowstyle='->', color=col))
    ax.annotate('', xy=(32, -.3), xytext=(12, -.3), arrowprops=dict(arrowstyle='->', color=C4, lw=1.3))
    ax.text(22, -.45, 'jump by c = 5 steps of 4', ha='center', color=C4, fontsize=8)
    ax.set_ylim(-.7, .8); ax.set_yticks([]); ax.legend(fontsize=8, loc='upper left')
    ax.spines['left'].set_visible(False)
    ax.set_title('b = 3·4 and c = 5·4, so b + c = (3+5)·4 lands on a multiple of 4 again', fontsize=9)
    save('P01-x1')


@fig('P01-x2')
def _():
    ax = plt.gca()
    _grid_table(ax, ['n even', 'n odd'], ['n²', 'n', '1', 'n²+n+1'],
                lambda r, c: {'n²': 'even' if r == 'n even' else 'odd', 'n': 'even' if r == 'n even' else 'odd',
                              '1': 'odd', 'n²+n+1': 'odd'}[c],
                'two cases cover all n; in both the sum is odd',
                lambda r, c: '#fde0dd' if c == 'n²+n+1' else None)
    ax.set_xlim(-1.6, 4.2)
    save('P01-x2')


@fig('P01-x3')
def _():
    ax = plt.gca()
    _grid_table(ax, ['n mod 5', 'n⁵ mod 5', 'n⁵−n mod 5'], list(range(5)),
                lambda r, c: {'n mod 5': c, 'n⁵ mod 5': pow(c, 5, 5), 'n⁵−n mod 5': (pow(c, 5) - c) % 5}[r],
                'five cases (n ≡ 0,1,2,3,4 mod 5); in every case n⁵ − n ≡ 0',
                lambda r, c: '#c7e9c0' if r == 'n⁵−n mod 5' else None)
    ax.set_xlim(-1.8, 5.2)
    save('P01-x3')


@fig('P01-x4')
def _():
    fig_, axs = plt.subplots(1, 4, figsize=(6.4, 2.1))
    cols = [C1, C4, C3, '#9467bd']
    for ax, k in zip(axs, [1, 2, 3, 4]):
        n = 2 * k + 1
        for i in range(n):
            for j in range(n):
                if (i, j) == (k, k):
                    c = C2
                elif i < k + 1 and j < k:      # bottom-left k+1 wide, k tall
                    c = cols[0]
                elif i >= k + 1 and j < k + 1:  # bottom-right
                    c = cols[1]
                elif i >= k and j >= k + 1:     # top-right
                    c = cols[2]
                else:
                    c = cols[3]
                ax.add_patch(plt.Rectangle((i, j), .9, .9, fc=c))
        ax.set_xlim(-.2, n); ax.set_ylim(-.2, n)
        ax.set_title(f'{n}² = 4·{k}·{k+1} + 1', fontsize=8)
        ax.set_aspect('equal'); ax.axis('off')
    plt.suptitle('(2k+1)² = four k×(k+1) rectangles + the centre; k(k+1) is even, so 4k(k+1) is divisible by 8', fontsize=8.5)
    save('P01-x4')


@fig('P02-e1')
def _():
    ax = plt.gca()
    cols = [C1, C4, C3, C2, '#9467bd', '#8c564b']
    n = 6
    for k in range(n):
        for i in range(k + 1):
            ax.add_patch(plt.Rectangle((i, k), .92, .92, fc=cols[k], alpha=.75))
            if i < k:
                ax.add_patch(plt.Rectangle((k, i), .92, .92, fc=cols[k], alpha=.75))
        ax.text(n + .4, k + .45, f'+{2*k+1}  → {(k+1)**2}', va='center', fontsize=8, color=cols[k])
    ax.set_xlim(-.2, n + 3); ax.set_ylim(-.2, n + .2); ax.set_aspect('equal'); ax.axis('off')
    ax.set_title('the induction step: an L of 2n+1 squares turns n² into (n+1)²', fontsize=9)
    save('P02-e1')


@fig('P02-e2')
def _():
    ax = plt.gca()
    ns = np.arange(1, 9)
    v = [4 ** n - 1 for n in ns]
    ax.bar(ns, v, color=C1)
    for n, x in zip(ns, v):
        ax.text(n, x * 1.15, f'3·{x//3}', ha='center', fontsize=7)
    ax.set_yscale('log'); ax.set_xlabel('n'); ax.set_ylabel('4ⁿ − 1')
    ax.set_title('4ⁿ⁺¹ − 1 = 4(4ⁿ − 1) + 3: divisibility by 3 passes from each bar to the next', fontsize=9)
    save('P02-e2')


@fig('P02-e3')
def _():
    ax = plt.gca()
    factor_tree(ax, 360, 0, 'strong induction: 360 = 2·180, and 180 < 360 is already a product of primes')
    ax.axis('off')
    save('P02-e3')


@fig('P02-e4')
def _():
    ax = plt.gca()
    rep = lambda n: [(a, b) for a in range(n // 3 + 1) for b in range(n // 5 + 1) if 3 * a + 5 * b == n]
    for n in range(1, 25):
        r = rep(n)
        c = C3 if r else '#dddddd'
        ax.bar(n, 1, color=c, ec='white')
        if r:
            a, b = r[0]
            ax.text(n, .5, f'{a}·3\n+{b}·5', ha='center', va='center', fontsize=5.5, rotation=0)
    for n in [8, 9, 10]:
        ax.bar(n, 1, fill=False, ec=C2, lw=2)
    ax.annotate('base: 8, 9, 10', (9, 1.02), (9, 1.35), ha='center', color=C2, arrowprops=dict(arrowstyle='->', color=C2))
    for n in range(11, 25):
        arrow(ax, (n - 3, 1.08), (n, 1.08), color=GR, rad=-.6)
    ax.set_xticks(range(1, 25)); ax.set_yticks([]); ax.set_ylim(0, 1.8); ax.tick_params(labelsize=7)
    ax.set_title('green = can be paid with 3s and 5s; from 8 on, n is reached from n − 3', fontsize=9)
    save('P02-e4')


@fig('P02-x1')
def _():
    ax = plt.gca()
    n = 7
    for k in range(1, n + 1):
        for j in range(k):
            ax.add_patch(plt.Rectangle((k - 1, j), .92, .92, fc=C1))
        for j in range(k, n + 1):
            ax.add_patch(plt.Rectangle((k - 1, j), .92, .92, fc=C4, alpha=.6))
    ax.text(n / 2, -.8, f'n = {n} columns', ha='center'); ax.text(n + .4, (n + 1) / 2, f'n+1 = {n+1}\nrows', va='center')
    ax.set_xlim(-.3, n + 2); ax.set_ylim(-1.2, n + 1.3); ax.set_aspect('equal'); ax.axis('off')
    ax.set_title('two copies of 1+2+…+n (blue, orange) fill an n×(n+1) rectangle', fontsize=9)
    save('P02-x1')


@fig('P02-x2')
def _():
    ax = plt.gca()
    n = np.arange(1, 11)
    ax.plot(n, 2.0 ** n, 'o-', color=C1, label='2ⁿ'); ax.plot(n, n ** 2, 's-', color=C2, label='n²')
    ax.axvspan(4.5, 10.5, color=C3, alpha=.08)
    ax.text(7.5, 30, 'induction works here:\nbase n = 5 (32 > 25)', ha='center', color=C3, fontsize=8)
    ax.set_yscale('log'); ax.set_xticks(n); ax.legend(); ax.set_xlabel('n')
    ax.set_title('2ⁿ > n² fails at n = 2, 3, 4 – the base case matters', fontsize=9)
    save('P02-x2')


@fig('P02-x3')
def _():
    ax = plt.gca()
    euclid_tiles(ax, 55, 34, 'gcd(F₁₀, F₉) = gcd(55, 34): each step returns two consecutive Fibonacci numbers')
    save('P02-x3')


@fig('P02-x4')
def _():
    ax = plt.gca()
    ax.add_patch(plt.Circle((0, 0), .8, fill=False, ec=C1, lw=2)); ax.add_patch(plt.Circle((1.9, 0), .8, fill=False, ec=C4, lw=2))
    ax.scatter([0], [0], s=200, color='#8c564b'); ax.scatter([1.9], [0], s=200, color='#bbbbbb')
    ax.text(0, -1.1, 'horses 1…n  (n = 1)', ha='center', color=C1); ax.text(1.9, -1.1, 'horses 2…n+1', ha='center', color=C4)
    ax.text(.95, 1.0, 'no common horse!', ha='center', color=C2)
    ax.set_xlim(-1.2, 3.1); ax.set_ylim(-1.4, 1.3); ax.set_aspect('equal'); ax.axis('off')
    ax.set_title('the step n = 1 → 2 breaks: the two groups of size n do not overlap', fontsize=9)
    save('P02-x4')


@fig('P03-e1')
def _():
    ax = plt.gca()
    a, b = 17, 12  # 17² = 289, 2·12² = 288: nearly a solution
    ax.add_patch(plt.Rectangle((0, 0), a, a, fill=False, ec='k', lw=1.5))
    ax.add_patch(plt.Rectangle((0, 0), b, b, fc=C1, alpha=.35, ec=C1))
    ax.add_patch(plt.Rectangle((a - b, a - b), b, b, fc=C4, alpha=.35, ec=C4))
    ax.add_patch(plt.Rectangle((a - b, a - b), 2 * b - a, 2 * b - a, fc='#7a4fa3', alpha=.6))
    ax.add_patch(plt.Rectangle((b, 0), a - b, a - b, fc='none', ec=C2, lw=1.5, hatch='//'))
    ax.add_patch(plt.Rectangle((0, b), a - b, a - b, fc='none', ec=C2, lw=1.5, hatch='//'))
    ax.text(a + .5, a / 2, 'side a', va='center'); ax.text(b / 2, -1.2, 'side b', ha='center', color=C1)
    ax.text(a / 2, a / 2, 'overlap:\nside 2b − a', ha='center', va='center', color='white', fontsize=8)
    ax.text(a + .5, 2, 'uncovered corners:\nside a − b (red)', fontsize=8, color=C2)
    ax.set_xlim(-1, a + 8); ax.set_ylim(-2, a + 1); ax.set_aspect('equal'); ax.axis('off')
    ax.set_title('if a² = 2b², overlap area = uncovered area: (2b−a)² = 2(a−b)², a smaller solution', fontsize=9)
    save('P03-e1')


@fig('P03-e2')
def _():
    ax = plt.gca()
    import sympy
    ks = range(1, 9)
    for k in ks:
        P = math.prod(PR[:k]) + 1
        f = sympy.factorint(P)
        ok = len(f) == 1 and list(f.values())[0] == 1
        ax.bar(k, math.log10(P), color=C3 if ok else C4)
        lab = str(P) if ok else '·'.join(map(str, f))
        ax.text(k, math.log10(P) + .15, lab, ha='center', fontsize=6.5, rotation=0 if k < 6 else 20)
    ax.set_xlabel('k  (N = p₁p₂…p_k + 1)'); ax.set_ylabel('log₁₀ N'); ax.set_ylim(0, 8.3)
    ax.set_title('green: N is prime; orange: N is not prime, but its prime factors are new', fontsize=9)
    save('P03-e2')


@fig('P03-x3')
def _():
    ax = plt.gca()
    bs = np.arange(1, 31)
    best = [min(abs(a ** 3 - 2 * int(b) ** 3) for a in range(1, 2 * int(b) + 2)) for b in bs]
    ax.bar(bs, best, color=C1)
    ax.set_yscale('log'); ax.set_xlabel('b'); ax.set_ylabel('min over a of |a³ − 2b³|')
    ax.axhline(1, color=C2, lw=1, ls=':')
    ax.set_title('a³ = 2b³ never holds: the closest a always misses (the bars never reach 0)', fontsize=9)
    save('P03-x3')


@fig('P03-x1')
def _():
    ax = plt.gca()
    _grid_table(ax, ['a mod 3', 'a² mod 3'], [0, 1, 2], lambda r, c: c if r == 'a mod 3' else c * c % 3,
                'a² ≡ 0 mod 3 only when a ≡ 0: so 3 | a² forces 3 | a',
                lambda r, c: '#fdd0a2' if c == 0 else None)
    ax.set_xlim(-1.8, 3.2)
    save('P03-x1')


@fig('P03-x2')
def _():
    ax = plt.gca()
    rows = [([3], 11, {11: 1}), ([3, 7], 83, {83: 1}), ([3, 7, 11], 923, {13: 1, 71: 1}), ([3, 7, 11, 19], 17555, {5: 1, 3511: 1})]
    for i, (ps, N, f) in enumerate(rows):
        ax.text(0, -i, f'4·{"·".join(map(str, ps))} − 1 = {N}', va='center', fontsize=9)
        x = 5.2
        for p in f:
            ax.text(x, -i, str(p), va='center', fontsize=9, color='white',
                    bbox=dict(boxstyle='round', fc=C2 if p % 4 == 3 else C1))
            x += 1.1
    ax.text(5.2, .8, 'prime factors (red ≡ 3 mod 4, blue ≡ 1 mod 4)', fontsize=8)
    ax.set_xlim(-.2, 9); ax.set_ylim(-3.6, 1.2); ax.axis('off')
    ax.set_title('N ≡ 3 mod 4 always has a red factor, and it is not in the list', fontsize=9)
    save('P03-x2')


@fig('P03-x4')
def _():
    ax = plt.gca()
    ax.plot([0, 1.05], [0, 0], color='k', lw=1)
    q = 1.0
    for k in range(7):
        ax.scatter([q], [0], s=30, color=C1 if k == 0 else C4, zorder=3)
        if k < 4: ax.text(q, .08 if k % 2 == 0 else -.14, f'r/{2**k}' if k else 'r', ha='center', fontsize=8)
        q /= 2
    ax.scatter([0], [0], s=30, color='k'); ax.text(0, .08, '0', ha='center')
    ax.set_ylim(-.3, .3); ax.axis('off')
    ax.set_title('any positive rational r has r/2 below it: no smallest one can exist', fontsize=9)
    save('P03-x4')


@fig('P04-e1')
def _():
    ax = plt.gca()
    s = '111111'
    def row(y, blocks, lab, col):
        x = 0
        for bl in blocks:
            for ch in bl:
                ax.add_patch(plt.Rectangle((x, y), .9, .9, fc=col, alpha=.6)); ax.text(x + .45, y + .45, ch, ha='center', va='center')
                x += 1
            x += .4
        ax.text(x + .3, y + .45, lab, va='center', fontsize=8)
    row(2, [s], '2⁶ − 1 = 63 in binary', '#dddddd')
    row(1, ['11'] * 3, '= 11₂ · 10101₂ = 3 · 21', C1)
    row(0, ['111'] * 2, '= 111₂ · 1001₂ = 7 · 9', C4)
    ax.set_xlim(-.3, 14); ax.set_ylim(-.3, 3.1); ax.axis('off')
    ax.set_title('n = 6 = 2·3 is composite ⇒ 2⁶−1 splits into blocks of 2 or 3 ones ⇒ composite', fontsize=9)
    save('P04-e1')


@fig('P04-e2')
def _():
    ax = plt.gca()
    ax.add_patch(plt.Rectangle((0, 0), 50, 50, fc=C2, alpha=.15))
    xs = np.linspace(0, 100, 10)
    ax.plot(xs, 100 - xs, color=C1, lw=1.5)
    ax.fill_between(xs, 100 - xs, 100, color=C1, alpha=.1)
    ax.text(25, 25, 'x < 50 and y < 50\n⇒ x + y < 100', ha='center', va='center', color=C2)
    ax.text(70, 75, 'x + y ≥ 100', ha='center', color=C1)
    ax.set_xlim(0, 100); ax.set_ylim(0, 100); ax.set_aspect('equal'); ax.set_xlabel('x'); ax.set_ylabel('y')
    ax.set_title('the red square (¬Q) lies entirely outside the blue region (P): ¬Q ⇒ ¬P', fontsize=9)
    save('P04-e2')


@fig('P04-e3')
def _():
    ax = plt.gca()
    import sympy
    for n in range(1, 17):
        f = sympy.factorint(2 ** n + 1)
        pr = len(f) == 1 and list(f.values())[0] == 1
        pow2 = n & (n - 1) == 0
        ax.bar(n, math.log2(2 ** n + 1), color=C3 if pr else ('#dddddd'), ec=C2 if pow2 else 'none', lw=1.5)
        if not pow2:
            m = n
            while m % 2 == 0: m //= 2
            a = n // m
            ax.text(n, math.log2(2 ** n + 1) + .3, str(2 ** a + 1), ha='center', fontsize=6.5, color=C4)
    ax.set_xticks(range(1, 17)); ax.set_xlabel('n'); ax.set_ylabel('log₂(2ⁿ+1)')
    ax.set_title('green = 2ⁿ+1 prime; red frame = n a power of 2; orange = the factor 2ᵃ+1 found', fontsize=9)
    save('P04-e3')


@fig('P04-x1')
def _():
    ax = plt.gca()
    for n in range(1, 13):
        ax.scatter(n, n * n, s=60, color=C1 if n % 2 == 0 else C4, zorder=3)
    ax.plot(range(1, 13), [n * n for n in range(1, 13)], color='#dddddd', zorder=1)
    ax.scatter([], [], color=C1, label='n even ⇒ n² even'); ax.scatter([], [], color=C4, label='n odd ⇒ n² odd')
    ax.legend(fontsize=8); ax.set_xlabel('n'); ax.set_ylabel('n²')
    ax.set_title('n² has the same parity as n', fontsize=9)
    save('P04-x1')


@fig('P04-x2')
def _():
    ax = plt.gca()
    for n in range(-6, 7):
        ax.scatter(n, 3 * n + 2, s=50, color=C4 if n % 2 else C1, zorder=3)
        ax.text(n, 3 * n + 3.5, str(3 * n + 2), ha='center', fontsize=7)
    ax.axhline(0, color=GR, lw=.6)
    ax.scatter([], [], color=C1, label='n even ⇒ 3n+2 even'); ax.scatter([], [], color=C4, label='n odd ⇒ 3n+2 odd')
    ax.legend(fontsize=8); ax.set_xlabel('n')
    ax.set_title('contrapositive: n even ⇒ 3n + 2 even', fontsize=9)
    save('P04-x2')


@fig('P04-x3')
def _():
    ax = plt.gca()
    m = 12
    T = np.array([[a * x % m for x in range(m)] for a in range(m)])
    ax.imshow(T == 1, cmap='Greens', aspect='equal')
    for a in range(m):
        g = math.gcd(a, m)
        ax.text(m - .2, a, f'gcd={g}', fontsize=7, va='center', color=C3 if g == 1 else C2)
    ax.set_xticks(range(m)); ax.set_yticks(range(m)); ax.set_xlabel('x'); ax.set_ylabel('a')
    ax.set_xlim(-.5, m + 1.8)
    ax.set_title('a·x ≡ 1 mod 12 (green cells) only in rows with gcd(a,12) = 1', fontsize=9)
    save('P04-x3')


@fig('P04-x4')
def _():
    ax = plt.gca()
    import sympy
    ps = [p for p in PR if p <= 31]
    for p in ps:
        ax.bar(p, 1, color=C3 if sympy.isprime(2 ** p - 1) else C2, width=1.2)
    ax.text(11, 1.05, '2047 = 23·89', ha='center', color=C2, fontsize=8)
    ax.set_xticks(ps); ax.set_yticks([]); ax.set_ylim(0, 1.3); ax.set_xlabel('prime p')
    ax.set_title('2ᵖ − 1 for prime p: green = prime, red = composite. The converse fails.', fontsize=9)
    save('P04-x4')


@fig('P05-e1')
def _():
    ax = plt.gca()
    nums = [17, 42, 8, 33, 91, 64]
    for r in range(5):
        ax.add_patch(plt.Rectangle((r * 1.3, 0), 1.1, 2.4, fill=False, ec='k'))
        ax.text(r * 1.3 + .55, -.3, f'≡{r} (mod 5)', ha='center', fontsize=8)
    cnt = [0] * 5
    for x in nums:
        r = x % 5
        ax.text(r * 1.3 + .55, .4 + .6 * cnt[r], str(x), ha='center', fontsize=10,
                color=C2 if nums.count(x) and [y % 5 for y in nums].count(r) > 1 else 'k')
        cnt[r] += 1
    ax.set_xlim(-.2, 6.6); ax.set_ylim(-.6, 2.7); ax.axis('off')
    ax.set_title('6 numbers, 5 boxes (remainders): 42 and 17 share a box, so 5 | 42 − 17', fontsize=9)
    save('P05-e1')


@fig('P05-e2')
def _():
    ax = plt.gca()
    n = 6
    chosen = [2, 3, 5, 8, 9, 11, 12]
    for k in range(n):
        ax.add_patch(plt.Rectangle((k * 1.3, 0), 1.1, 1, fill=False, ec='k'))
        for j, v in enumerate([2 * k + 1, 2 * k + 2]):
            ax.text(k * 1.3 + .3 + .5 * j, .5, str(v), ha='center', va='center',
                    color='white' if v in chosen else 'k',
                    bbox=dict(boxstyle='circle', fc=(C2 if all(w in chosen for w in [2*k+1, 2*k+2]) else C1) if v in chosen else 'white', ec='none'))
    ax.set_xlim(-.2, 8); ax.set_ylim(-.3, 1.3); ax.axis('off')
    ax.set_title('7 numbers from 1…12 in 6 boxes {2k−1, 2k}: a box holds two consecutive, coprime numbers', fontsize=9)
    save('P05-e2')


@fig('P05-e3')
def _():
    ax = plt.gca()
    rs = [int('1' * k) % 7 for k in range(1, 9)]
    ax.plot(range(1, 9), rs, 'o-', color=C1)
    for k, r in enumerate(rs, 1):
        ax.text(k, r + .3, '1' * k, ha='center', fontsize=6, rotation=30)
    ax.scatter([6], [0], s=120, facecolors='none', edgecolors=C2, lw=2)
    ax.set_xlabel('k (number of ones)'); ax.set_ylabel('111…1 mod 7'); ax.set_yticks(range(7)); ax.set_ylim(-.6, 7.5)
    ax.set_title('remainders of 1, 11, 111, … mod 7: among 8 of them two repeat; here 111111 ≡ 0', fontsize=9)
    save('P05-e3')


@fig('P05-e4')
def _():
    ax = plt.gca()
    N = 10
    a = math.sqrt(2)
    for k in range(N + 1):
        ax.axvline(k / N, color='#dddddd', lw=.8)
    fr = [(q * a) % 1 for q in range(0, N + 1)]
    for q, f in enumerate(fr):
        ax.scatter(f, 0, s=40, color=C1, zorder=3); ax.text(f, .06 + .05 * (q % 3), str(q), ha='center', fontsize=7)
    ax.annotate('', xy=(fr[5], -.1), xytext=(fr[0], -.1), arrowprops=dict(arrowstyle='<->', color=C2))
    ax.text((fr[0] + fr[5]) / 2, -.18, f'q = 5: |5√2 − 7| = {abs(5*a-7):.3f} < 1/10', ha='center', color=C2, fontsize=8)
    ax.set_ylim(-.3, .3); ax.set_yticks([]); ax.set_xlabel('fractional part of q√2, q = 0…10, in 10 boxes')
    ax.set_title('11 points in 10 boxes: two are within 1/10 of each other', fontsize=9)
    save('P05-e4')


@fig('P05-x1')
def _():
    ax = plt.gca()
    n = 5
    for i, o in enumerate(range(1, 2 * n, 2)):
        chain = []
        x = o
        while x <= 2 * n:
            chain.append(x); x *= 2
        for j, v in enumerate(chain):
            ax.text(j, -i, str(v), ha='center', va='center', bbox=dict(boxstyle='round', fc='#c6dbef'))
            if j: ax.annotate('', (j - .25, -i), (j - .75, -i), arrowprops=dict(arrowstyle='->', color=GR))
        ax.text(-1, -i, f'odd part {o}', ha='right', va='center', fontsize=8)
    ax.set_xlim(-3, 4); ax.set_ylim(-n + .4, .6); ax.axis('off')
    ax.set_title('1…10 split into 5 chains by odd part; 6 numbers ⇒ two in one chain ⇒ one divides the other', fontsize=9)
    save('P05-x1')


@fig('P05-x2')
def _():
    ax = plt.gca()
    pts = [(1, 2), (4, 7), (3, 3), (6, 1), (2, 5)]
    cls = {(0, 0): C1, (0, 1): C3, (1, 0): C4, (1, 1): C2}
    for x, y in pts:
        ax.scatter(x, y, s=70, color=cls[(x % 2, y % 2)], zorder=3)
        ax.text(x + .15, y + .2, f'({x},{y})', fontsize=8)
    ax.plot([1, 3], [3 - 2 + 2, 3], alpha=0)
    ax.plot([1, 3], [5 - 3, 3], color=GR, ls=':')
    ax.plot([4, 2], [7, 5], color=C2, ls='--'); ax.scatter([3], [6], marker='x', color=C2, s=60)
    ax.text(3.1, 6.2, 'midpoint (3,6)', color=C2, fontsize=8)
    ax.set_xticks(range(8)); ax.set_yticks(range(9)); ax.grid(alpha=.3); ax.set_aspect('equal')
    ax.set_title('4 parity colours, 5 points: (4,7) and (2,5) share a colour; midpoint is a lattice point', fontsize=9)
    save('P05-x2')


@fig('P05-x3')
def _():
    ax = plt.gca()
    a = [3, 5, 7, 2, 4, 9]
    n = len(a)
    S = np.cumsum(a)
    ax.bar(range(1, n + 1), S % n, color=C1)
    for i, s in enumerate(S, 1):
        ax.text(i, s % n + .15, f'S{i}={s}', ha='center', fontsize=7)
    ax.set_xlabel('k'); ax.set_ylabel('S_k mod 6'); ax.set_xticks(range(1, n + 1))
    ax.set_title('a = 3,5,7,2,4,9: S₁ ≡ S₃ (mod 6), so a₂+a₃ = 12 is divisible by 6', fontsize=9)
    save('P05-x3')


@fig('P05-x4')
def _():
    ax = plt.gca()
    pts = circle_nodes(ax, 7, labels=list(range(7)))
    r, seq = 1, []
    for _ in range(6):
        nr = r * 10 % 7
        arrow(ax, pts[r], pts[nr]); seq.append(r * 10 // 7); r = nr
    ax.set_aspect('equal'); ax.axis('off')
    ax.set_title('long division 1/7: remainders 1→3→2→6→4→5→1; digits ' + ''.join(map(str, seq)) + ' repeat', fontsize=9)
    save('P05-x4')


def _sq_circle(ax, m, k, title):
    pts = circle_nodes(ax, m, labels=list(range(m)))
    S = sorted({x ** k % m for x in range(m)})
    for s in S:
        ax.scatter(*pts[s], s=180, color=C3, zorder=4)
    for x in range(m):
        arrow(ax, pts[x], pts[x ** k % m], color='#bbbbbb', rad=.25)
    ax.set_aspect('equal'); ax.axis('off'); ax.set_title(title, fontsize=9)


@fig('P06-e1')
def _():
    ax = plt.gca()
    _grid_table(ax, [0, 1], [0, 1], lambda a, b: (a + b) % 4, 'x² + y² mod 4: the squares are only 0 or 1, the sum never reaches 3',
                lambda a, b: '#c7e9c0', 'x²', 'y²')
    ax.set_xlim(-1.4, 2.4)
    save('P06-e1')


@fig('P06-e2')
def _():
    _sq_circle(plt.gca(), 5, 2, 'squares mod 5 (green): 0, 1, 4. The value 2 is never hit.')
    save('P06-e2')


@fig('P06-e3')
def _():
    ax = plt.gca()
    sums = sorted({(a + b + c) % 9 for a in (0, 1, 8) for b in (0, 1, 8) for c in (0, 1, 8)})
    for r in range(9):
        ax.bar(r, 1, color=C3 if r in sums else C2)
    ax.set_xticks(range(9)); ax.set_yticks([]); ax.set_xlabel('residue mod 9')
    ax.set_title('cubes mod 9 ∈ {0, 1, 8}; sums of three hit the green residues only, never 4 or 5', fontsize=9)
    save('P06-e3')


@fig('P06-e4')
def _():
    ax = plt.gca()
    sums = sorted({(a + b + c) % 8 for a in (0, 1, 4) for b in (0, 1, 4) for c in (0, 1, 4)})
    for r in range(8):
        ax.bar(r, 1, color=C3 if r in sums else C2)
    ax.set_xticks(range(8)); ax.set_yticks([]); ax.set_xlabel('residue mod 8')
    ax.set_title('squares mod 8 ∈ {0, 1, 4}; three of them never sum to 7 mod 8', fontsize=9)
    save('P06-e4')


@fig('P06-x1')
def _():
    ax = plt.gca()
    pts = circle_nodes(ax, 7, labels=list(range(7)))
    x = 1
    for _ in range(3):
        arrow(ax, pts[x], pts[2 * x % 7]); x = 2 * x % 7
    for v in (1, 2, 4):
        ax.scatter(*pts[v], s=160, color=C1, zorder=4)
    for v in (2, 3, 5):
        ax.scatter(*pts[v], s=60, facecolors='none', edgecolors=C4, lw=2, zorder=5)
    ax.set_aspect('equal'); ax.axis('off')
    ax.set_title('2ⁿ mod 7 cycles 1→2→4 (blue); 2ⁿ+1 is 2, 3 or 5 (orange) – never 0', fontsize=9)
    save('P06-x1')


@fig('P06-x2')
def _():
    _sq_circle(plt.gca(), 16, 4, 'fourth powers mod 16 are 0 or 1 (green); 2023 ≡ 7 is out of reach')
    save('P06-x2')


@fig('P06-x3')
def _():
    ax = plt.gca()
    _grid_table(ax, ['n mod 5', 'n²+n+1 mod 5'], list(range(5)), lambda r, c: c if r == 'n mod 5' else (c * c + c + 1) % 5,
                'n² + n + 1 mod 5 takes only the values 1, 2, 3', lambda r, c: '#c6dbef' if r != 'n mod 5' else None)
    ax.set_xlim(-2.3, 5.2)
    save('P06-x3')


@fig('P06-x4')
def _():
    ax = plt.gca()
    ds = [x * x % 10 for x in range(10)]
    for d in range(10):
        ax.bar(d, ds.count(d), color=C3 if ds.count(d) else C2)
        if not ds.count(d): ax.text(d, .1, '✗', ha='center', color='white')
    ax.set_xticks(range(10)); ax.set_xlabel('last digit of n²'); ax.set_ylabel('how many n mod 10')
    ax.set_title('last digit of a square: never 2, 3, 7, 8', fontsize=9)
    save('P06-x4')


# ================= proof-methods course (P07–P12) =================
def _descent_chain(ax, triples, title, labels=('x', 'y', 'z')):
    for i, t in enumerate(triples):
        y = -i
        ax.text(0, y, '(' + ', '.join(map(str, t)) + ')', ha='center', va='center', fontsize=10,
                bbox=dict(boxstyle='round', fc='#c6dbef' if i < len(triples) - 1 else '#fde0dd'))
        if i < len(triples) - 1:
            ax.annotate('', (0, y - .7), (0, y - .3), arrowprops=dict(arrowstyle='->', color=C2, lw=1.5))
    ax.set_xlim(-3, 3); ax.set_ylim(-len(triples) + .4, .6); ax.axis('off'); ax.set_title(title, fontsize=9)


@fig('P07-e1')
def _():
    fig_, (a1, a2) = plt.subplots(1, 2, figsize=(6.4, 3.0), gridspec_kw={'width_ratios': [1.1, 1]})
    _grid_table(a1, [0, 1, 2], [0, 1, 2], lambda x, y: (x * x + y * y) % 3, 'x² + y² mod 3 (rows x, columns y mod 3)',
                lambda x, y: '#c7e9c0' if (x * x + y * y) % 3 == 0 else None)
    a1.set_xlim(-1.2, 3.2)
    a2.set_xlim(0, 1); a2.axis('off')
    a2.text(.05, .8, 'if x² + y² = 3z² then 3 | x² + y²', fontsize=9)
    a2.text(.05, .65, '⇒ x = 3x₁, y = 3y₁  (only green cell)', fontsize=9)
    a2.text(.05, .5, '⇒ 9(x₁² + y₁²) = 3z² ⇒ 3 | z', fontsize=9)
    a2.text(.05, .35, '⇒ (x₁, y₁, z/3) is a smaller solution', fontsize=9, color=C2)
    a2.text(.05, .15, 'positive z cannot shrink forever', fontsize=9, color=C2)
    save('P07-e1')


@fig('P07-e2')
def _():
    ax = plt.gca()
    rows = [(0, 1), (1, 0), (1, 1)]
    ax.axis('off')
    lines = ['x³ + 2y³ + 4z³ = 0',
             'mod 2: x³ ≡ 0 ⇒ x = 2x₁',
             '8x₁³ + 2y³ + 4z³ = 0 ⇒ y³ + 2z³ + 4x₁³ = 0',
             'same equation, variables rotated: (y, z, x₁)',
             'repeat ⇒ y, z even too ⇒ (x/2, y/2, z/2) is a solution',
             'so 2ᵏ divides x, y, z for every k ⇒ x = y = z = 0']
    for i, l in enumerate(lines):
        ax.text(0, -i, l, fontsize=9, va='center', color=C2 if i == len(lines) - 1 else 'k')
        if i: ax.annotate('', (-.04, -i + .25), (-.04, -i + .75), arrowprops=dict(arrowstyle='->', color=C1), xycoords='data')
    ax.set_xlim(-.1, 1); ax.set_ylim(-len(lines) + .4, .6)
    ax.set_title('descent by halving: a nonzero solution would give an endless chain of halvings', fontsize=9)
    save('P07-e2')


@fig('P07-e3')
def _():
    ax = plt.gca()
    seq = [100]
    while seq[-1] > 1:
        seq.append(seq[-1] // 2 if seq[-1] % 2 == 0 else seq[-1] - 1)
    ax.step(range(len(seq)), seq, where='post', color=C1)
    ax.scatter(range(len(seq)), seq, color=C1, s=20)
    for i, s in enumerate(seq):
        ax.text(i, s + 3, str(s), ha='center', fontsize=7)
    ax.axhline(0, color=C2, lw=1); ax.text(len(seq) - 1, 6, 'floor: 1', color=C2, ha='right', fontsize=8)
    ax.set_xlabel('step'); ax.set_ylabel('value')
    ax.set_title('a strictly decreasing sequence of positive integers must stop (here after 9 steps)', fontsize=9)
    save('P07-e3')


@fig('P07-x1')
def _():
    _descent_chain(plt.gca(), [('x', 'y'), ('y', 'x − y'), ('2y − x', 'x − y'), ('…', '…')],
                   'x² = 2y²  ⇒  (2y − x)² = 2(x − y)², with 0 < x − y < y: a smaller solution')
    save('P07-x1')


@fig('P07-x2')
def _():
    _sq_circle(plt.gca(), 7, 2, 'squares mod 7: 0, 1, 2, 4. No two nonzero ones add up to 0 mod 7.')
    save('P07-x2')


@fig('P07-x3')
def _():
    ax = plt.gca()
    cubes = sorted({x ** 3 % 9 for x in range(9)})
    _grid_table(ax, ['x mod 3', 'x³ mod 9'], [0, 1, 2], lambda r, c: c if r == 'x mod 3' else c ** 3 % 9,
                'x³ + 3y³ + 9z³ = 0: mod 3 gives 3 | x; then mod 9 gives 3 | y; then 3 | z', lambda r, c: '#fdd0a2' if c == 0 else None)
    ax.set_xlim(-1.8, 3.2)
    save('P07-x3')


@fig('P07-x4')
def _():
    ax = plt.gca()
    _grid_table(ax, [0, 1], [0, 1, 2, 3], lambda a, k: '', '', None)
    ax.cla()
    trip = [(a, b, c) for a in (0, 1) for b in (0, 1) for c in (0, 1)]
    ok = [(a + b + c) % 4 == 0 for a, b, c in trip]
    for i, (t, o) in enumerate(zip(trip, ok)):
        ax.bar(i, 1, color=C3 if o else '#dddddd')
        ax.text(i, .5, '\n'.join(map(str, t)), ha='center', va='center', fontsize=8)
        ax.text(i, 1.05, str(sum(t)), ha='center', fontsize=8)
    ax.set_xticks([]); ax.set_yticks([]); ax.set_ylim(0, 1.3)
    ax.set_title('x², y², z² mod 4 ∈ {0,1}; the sum is ≡ 0 mod 4 only when all three are 0, i.e. all even', fontsize=9)
    save('P07-x4')


@fig('P08-e1')
def _():
    ax = plt.gca()
    a, b = 12, 18
    X, Y = np.meshgrid(range(-4, 5), range(-4, 5))
    V = a * X + b * Y
    sc = ax.scatter(X, Y, c=V, cmap='coolwarm', s=120)
    for x, y, v in zip(X.flat, Y.flat, V.flat):
        ax.text(x, y, str(v), ha='center', va='center', fontsize=6)
    pos = V[V > 0].min()
    for x, y, v in zip(X.flat, Y.flat, V.flat):
        if v == pos:
            ax.scatter(x, y, s=260, facecolors='none', edgecolors='k', lw=1.5)
    ax.set_xlabel('x'); ax.set_ylabel('y'); ax.set_aspect('equal')
    ax.set_title(f'12x + 18y: the smallest positive value (circled) is {pos} = gcd(12, 18)', fontsize=9)
    save('P08-e1')


@fig('P08-e2')
def _():
    ax = plt.gca()
    a, b = 7, 31
    ax.plot([-5, 36], [0, 0], color=GR)
    for q in range(0, 6):
        ax.plot([q * a] * 2, [-.15, .15], color=C1)
        ax.text(q * a, -.4, f'{q}·7', ha='center', fontsize=8, color=C1)
    ax.scatter([b], [0], color=C2, s=50, zorder=3); ax.text(b, .3, 'b = 31', color=C2, ha='center')
    for q in range(0, 5):
        r = b - q * a
        ax.annotate('', (b, .7 + .25 * q), (q * a, .7 + .25 * q), arrowprops=dict(arrowstyle='<->', color=C3 if q == 4 else '#bbbbbb'))
        ax.text(q * a - .5, .7 + .25 * q, f'r = {r}', ha='right', va='center', fontsize=7, color=C3 if q == 4 else GR)
    ax.set_ylim(-.7, 2.1); ax.set_xlim(-8, 36); ax.axis('off')
    ax.set_title('the least non-negative b − 7q is r = 3 < 7 (green): 31 = 4·7 + 3', fontsize=9)
    save('P08-e2')


@fig('P08-e3')
def _():
    ax = plt.gca()
    ns = range(2, 41)
    sd = [min(d for d in range(2, n + 1) if n % d == 0) for n in ns]
    ax.bar(ns, sd, color=[C3 if isp(n) else C1 for n in ns])
    ax.set_xlabel('n'); ax.set_ylabel('smallest divisor > 1')
    ax.set_title('the smallest divisor > 1 is always prime (green bars: n itself is prime)', fontsize=9)
    save('P08-e3')


@fig('P08-x1')
def _():
    ax = plt.gca()
    p, a, b = 7, 4, 21
    X = np.arange(-6, 7)
    Y = np.arange(-6, 7)
    for x in X:
        for y in Y:
            v = p * x + a * y
            if v == 1:
                ax.scatter(x, y, color=C2, s=50, zorder=3); ax.text(x + .2, y + .2, f'7·{x} + 4·{y} = 1', fontsize=7, color=C2)
            else:
                ax.scatter(x, y, color='#dddddd', s=8)
    ax.set_aspect('equal'); ax.set_xlabel('x'); ax.set_ylabel('y')
    ax.set_title('gcd(7, 4) = 1: points with 7x + 4y = 1 exist. Multiply by b: b = 7bx + 4by', fontsize=9)
    save('P08-x1')


@fig('P08-x2')
def _():
    ax = plt.gca()
    for x in range(0, 13):
        for y in range(0, 10):
            ax.scatter(x, y, color='#dddddd', s=6)
    ax.plot([0, 12], [0, 9], color=C1)
    for k in range(1, 4):
        ax.scatter(4 * k, 3 * k, color=C1, s=40, zorder=3); ax.text(4 * k + .2, 3 * k - .6, f'{3*k}/{4*k}', fontsize=8)
    ax.scatter(4, 3, color=C2, s=90, zorder=4)
    ax.set_xlabel('denominator'); ax.set_ylabel('numerator'); ax.set_aspect('equal')
    ax.set_title('fractions equal to 6/8 lie on one ray; the lattice point nearest 0 gives 3/4', fontsize=9)
    save('P08-x2')


@fig('P08-x3')
def _():
    ax = plt.gca()
    n = 45
    rem, y = n, 0
    while rem:
        p = 1 << (rem.bit_length() - 1)
        ax.add_patch(plt.Rectangle((n - rem, 0), p, 1, fc=[C1, C4, C3, C2, '#9467bd'][y % 5], ec='white'))
        ax.text(n - rem + p / 2, .5, str(p), ha='center', va='center', color='white')
        ax.text(n - rem + p / 2, 1.2, f'left: {rem - p}', ha='center', fontsize=7)
        rem -= p; y += 1
    ax.set_xlim(-1, n + 1); ax.set_ylim(-.3, 1.6); ax.axis('off')
    ax.set_title('take the largest power of 2 that fits, repeat: 45 = 32 + 8 + 4 + 1', fontsize=9)
    save('P08-x3')


@fig('P08-x4')
def _():
    ax = plt.gca()
    from fractions import Fraction
    n = 10
    terms = [Fraction(1, k) for k in range(1, n + 1)]
    v2 = lambda k: (k & -k).bit_length() - 1
    ax.bar(range(1, n + 1), [v2(k) for k in range(1, n + 1)], color=[C2 if k == 8 else C1 for k in range(1, n + 1)])
    ax.set_xlabel('k'); ax.set_ylabel('power of 2 in k')
    H = sum(terms)
    ax.set_title(f'only k = 8 has the largest power of 2; H₁₀ = {H.numerator}/{H.denominator} has even denominator', fontsize=9)
    save('P08-x4')


@fig('P09-e1')
def _():
    ax = plt.gca()
    for x in range(110, 132):
        c = C3 if isp(x) else ('#fdd0a2' if 122 <= x <= 125 else '#dddddd')
        ax.bar(x, 1, color=c, ec='white')
        if 122 <= x <= 125:
            d = x - 120
            ax.text(x, .5, f'{d}|', ha='center', va='center', fontsize=7)
    ax.set_yticks([]); ax.set_xlabel('n'); ax.set_xticks(range(110, 132, 2))
    ax.set_title('5! + 2, …, 5! + 5 = 122…125 (orange) are composite: k divides 5! + k. Green = primes.', fontsize=9)
    save('P09-e1')


@fig('P09-e2')
def _():
    ax = plt.gca()
    ns = range(0, 51)
    v = [n * n + n + 41 for n in ns]
    ax.bar(ns, [1] * len(v), color=[C3 if isp(x) else C2 for x in v])
    ax.text(40, 1.05, '40: 1681 = 41²', ha='center', color=C2, fontsize=8)
    ax.set_yticks([]); ax.set_ylim(0, 1.25); ax.set_xlabel('n')
    ax.set_title('n² + n + 41: prime (green) for n = 0…39, and then a counterexample', fontsize=9)
    save('P09-e2')


@fig('P09-e3')
def _():
    ax = plt.gca()
    for k in range(6):
        F = 2 ** (2 ** k) + 1
        ax.bar(k, math.log2(F), color=C3 if k < 5 else C2)
        ax.text(k, math.log2(F) + .6, str(F) if k < 5 else '641 · 6700417', ha='center', fontsize=8)
    ax.set_xlabel('k'); ax.set_ylabel('log₂ F_k'); ax.set_ylim(0, 37)
    ax.set_title('Fermat numbers F_k = 2^(2^k) + 1: prime for k ≤ 4, composite at k = 5 (Euler)', fontsize=9)
    save('P09-e3')


@fig('P09-x1')
def _():
    ax = plt.gca()
    for k in range(7):
        v = 127 - 2 ** k
        f = factor(v)
        ax.barh(k, v, color='#dddddd')
        ax.text(v + 2, k, f'127 − {2**k} = {v} = ' + '·'.join(f'{p}^{e}' if e > 1 else str(p) for p, e in f.items()) if isinstance(f, dict) else f'{v}', va='center', fontsize=8)
    ax.set_yticks(range(7)); ax.set_yticklabels([f'2^{k}' for k in range(7)]); ax.set_xlim(0, 230)
    ax.set_title('127 − 2ᵏ is never prime: 127 is not "prime + power of 2"', fontsize=9)
    save('P09-x1')


@fig('P09-x2')
def _():
    ax = plt.gca()
    for x in range(14, 34):
        ax.bar(x, 1, color=C3 if isp(x) else ('#fdd0a2' if 24 <= x <= 28 else '#dddddd'), ec='white')
        ax.text(x, .5, str(x), ha='center', va='center', fontsize=7, rotation=90)
    ax.set_yticks([]); ax.set_xticks([])
    ax.set_title('24, 25, 26, 27, 28: the first run of five composite numbers (6! + 2 = 722 is far larger)', fontsize=9)
    save('P09-x2')


@fig('P09-x3')
def _():
    ax = plt.gca()
    for i in range(5):
        for j in range(2):
            d = 2 ** i * 3 ** j
            ax.text(i, j, str(d), ha='center', va='center', bbox=dict(boxstyle='round', fc='#c6dbef'))
            if i: ax.plot([i - 1 + .2, i - .2], [j, j], color=GR)
            if j: ax.plot([i, i], [.2, .8], color=GR)
    ax.set_xlim(-.5, 4.5); ax.set_ylim(-.6, 1.6); ax.axis('off')
    ax.set_title('48 = 2⁴·3: divisors 2ⁱ3ʲ form a 5 × 2 grid, so d(48) = 10', fontsize=9)
    save('P09-x3')


@fig('P09-x4')
def _():
    ax = plt.gca()
    r = math.sqrt(2)
    x = np.linspace(.5, 2.2, 200)
    ax.plot(x, x ** r, color=C1, label='t^√2')
    ax.scatter([r], [r ** r], color=C4, zorder=3); ax.text(r + .05, r ** r - .25, f'√2^√2 ≈ {r**r:.4f}', color=C4, fontsize=8)
    ax.scatter([r ** r], [2], color=C2, zorder=3); ax.text(r ** r - .05, 2.15, '(√2^√2)^√2 = 2', color=C2, fontsize=8, ha='right')
    ax.axhline(2, color=GR, lw=.6, ls=':')
    ax.legend(fontsize=8); ax.set_xlabel('t')
    ax.set_title('either √2^√2 is rational, or raising it to √2 gives the rational 2', fontsize=9)
    save('P09-x4')


@fig('P10-e1')
def _():
    ax = plt.gca()
    x = 12
    for a in range(1, x + 1):
        for b in range(1, x // a + 1):
            ax.scatter(a, b, color=C1, s=18, zorder=3)
    t = np.linspace(1, x, 200)
    ax.plot(t, x / t, color=C2, lw=1)
    for a in range(1, x + 1):
        ax.text(a, -0.6, str(x // a), ha='center', fontsize=7, color=C4)
    for n in range(1, x + 1):
        pass
    ax.text(x + .3, -0.6, f'Σ = {sum(x // a for a in range(1, x + 1))}', fontsize=8, color=C4)
    ax.set_xlim(0, x + 2); ax.set_ylim(-1.2, x + .5); ax.set_xlabel('d'); ax.set_ylabel('m')
    ax.set_title('points (d, m) with dm ≤ 12: column d holds ⌊12/d⌋ points; each n = dm counts d(n) times', fontsize=9)
    save('P10-e1')


@fig('P10-e2')
def _():
    ax = plt.gca()
    n = 12
    from fractions import Fraction
    dens = sorted({Fraction(k, n).denominator for k in range(1, n + 1)})
    cols = dict(zip(dens, [C1, C4, C3, C2, '#9467bd', '#8c564b']))
    for k in range(1, n + 1):
        f = Fraction(k, n)
        ax.bar(k, 1, color=cols[f.denominator])
        ax.text(k, .5, f'{f.numerator}/{f.denominator}', ha='center', va='center', fontsize=7, color='white', rotation=90)
    from matplotlib.patches import Patch
    ax.legend(handles=[Patch(color=cols[d], label=f'denominator {d}: φ({d}) = {phi(d)}') for d in dens],
              fontsize=6.5, ncol=3, loc='upper center', bbox_to_anchor=(.5, -.05)); ax.set_xticks([]); ax.set_yticks([])
    ax.set_title('k/12 in lowest terms: grouping by denominator gives Σ_{d|12} φ(d) = 12', fontsize=9)
    save('P10-e2')


@fig('P10-e3')
def _():
    ax = plt.gca()
    p = 11
    pts = circle_nodes(ax, p - 1, labels=list(range(1, p)))
    done = set()
    for a in range(1, p):
        b = pow(a, -1, p)
        if a in done: continue
        done |= {a, b}
        if a == b:
            ax.scatter(*pts[a - 1], s=200, facecolors='none', edgecolors=C2, lw=2)
        else:
            ax.plot(*zip(pts[a - 1], pts[b - 1]), color=C1, lw=1.2)
    ax.set_aspect('equal'); ax.axis('off')
    ax.set_title('mod 11: each a is paired with a⁻¹ (lines); only 1 and 10 = −1 pair with themselves', fontsize=9)
    save('P10-e3')


@fig('P10-x1')
def _():
    ax = plt.gca()
    n = 10
    for k in range(1, n + 1):
        ax.bar(k, k, color=C1); ax.bar(k, n + 1 - k, bottom=k, color=C4)
    ax.axhline(n + 1, color=C2, ls=':')
    ax.set_xlabel('k'); ax.set_title('k + (n+1−k) = n+1 in every column: 2(1+…+n) = n(n+1)', fontsize=9)
    save('P10-x1')


@fig('P10-x2')
def _():
    fig_, axs = plt.subplots(1, 2, figsize=(6.4, 2.6))
    for ax, n in zip(axs, [36, 40]):
        ds = divisors(n)
        for i, d in enumerate([d for d in ds if d * d <= n]):
            e = n // d
            ax.text(0, -i, str(d), ha='center', va='center', bbox=dict(boxstyle='round', fc='#c6dbef'))
            if e != d:
                ax.text(2, -i, str(e), ha='center', va='center', bbox=dict(boxstyle='round', fc='#fdd0a2'))
                ax.plot([.3, 1.7], [-i, -i], color=GR)
            else:
                ax.text(1, -i, 'alone', ha='center', va='center', color=C2, fontsize=8)
        ax.set_xlim(-.6, 2.6); ax.set_ylim(-5, .6); ax.axis('off')
        ax.set_title(f'n = {n}: d(n) = {len(ds)}', fontsize=9)
    plt.suptitle('divisors pair up as d ↔ n/d; only √n (for a square) is left alone', fontsize=9)
    save('P10-x2')


@fig('P10-x3')
def _():
    ax = plt.gca()
    n = 15
    U = [k for k in range(1, n) if math.gcd(k, n) == 1]
    for k in U:
        ax.scatter(k, 0, s=80, color=C1, zorder=3); ax.text(k, -.15, str(k), ha='center', fontsize=8)
    for i, k in enumerate(U[:len(U) // 2]):
        ax.annotate('', (n - k, .05), (k, .05), arrowprops=dict(arrowstyle='-', color=C4, connectionstyle='arc3,rad=-.5'))
    ax.set_ylim(-.3, 1.2); ax.set_xlim(0, n); ax.axis('off')
    ax.set_title(f'units mod 15 pair as k ↔ 15 − k (each pair sums to 15): sum = 15·8/2 = {sum(U)}', fontsize=9)
    save('P10-x3')


@fig('P10-x4')
def _():
    ax = plt.gca()
    n = 20
    for k in range(1, n + 1):
        v = (k & -k).bit_length() - 1
        for j in range(v):
            ax.add_patch(plt.Rectangle((k - .4, j), .8, .9, fc=[C1, C4, C3, C2][j]))
    for j in range(4):
        ax.text(n + 1, j + .45, f'row {j+1}: ⌊20/{2**(j+1)}⌋ = {n // 2**(j+1)}', va='center', fontsize=8, color=[C1, C4, C3, C2][j])
    ax.set_xlim(0, n + 7); ax.set_ylim(-.2, 4.5); ax.set_xticks(range(1, n + 1)); ax.set_yticks([])
    ax.set_title('the 2s in 20!: count by columns (per k) or by rows: 10 + 5 + 2 + 1 = 18', fontsize=9)
    save('P10-x4')


@fig('P11-e1')
def _():
    ax = plt.gca()
    v2 = lambda k: (int(k) & -int(k)).bit_length() - 1
    a = np.arange(1, 25)
    ax.scatter(a, [2 * v2(x) for x in a], color=C1, label='exponent of 2 in a² (always even)')
    ax.scatter(a + .3, [2 * v2(x) + 1 for x in a], color=C2, marker='s', label='exponent of 2 in 2b² (always odd)')
    ax.set_xlabel('a or b'); ax.set_yticks(range(0, 10)); ax.legend(fontsize=8)
    ax.set_title('a² = 2b² would need one number with both an even and an odd exponent of 2', fontsize=9)
    save('P11-e1')


@fig('P11-e2')
def _():
    ax = plt.gca()
    for i in range(4):
        for j in range(3):
            ax.text(i, j, str(2 ** i * 3 ** j), ha='center', va='center', bbox=dict(boxstyle='round', fc='#c7e9c0'))
            if i: ax.plot([i - .8, i - .2], [j, j], color=GR)
            if j: ax.plot([i, i], [j - .75, j - .25], color=GR)
    ax.text(1.5, -.8, '2⁰ … 2³  (4 choices)', ha='center'); ax.text(3.6, 1, '3⁰ … 3²\n(3 choices)', va='center')
    ax.set_xlim(-.5, 4.6); ax.set_ylim(-1.1, 2.5); ax.axis('off')
    ax.set_title('72 = 2³·3²: each divisor is 2ⁱ3ʲ, so d(72) = 4·3 = 12', fontsize=9)
    save('P11-e2')


@fig('P11-e3')
def _():
    ax = plt.gca()
    ps = [2, 3, 5, 7]
    e = lambda n, p: (lambda f: f.get(p, 0))(factor(n))
    a, b = 360, 84
    x = np.arange(len(ps))
    ax.bar(x - .2, [e(a, p) for p in ps], .4, color=C1, label='360 = 2³·3²·5')
    ax.bar(x + .2, [e(b, p) for p in ps], .4, color=C4, label='84 = 2²·3·7')
    for i, p in enumerate(ps):
        lo, hi = min(e(a, p), e(b, p)), max(e(a, p), e(b, p))
        ax.text(i, hi + .25, f'min {lo} / max {hi}', ha='center', fontsize=7)
    ax.set_xticks(x); ax.set_xticklabels(map(str, ps)); ax.set_xlabel('prime'); ax.set_ylabel('exponent'); ax.legend(fontsize=8)
    ax.set_ylim(0, 4)
    ax.set_title(f'gcd = 2²·3 = {math.gcd(a,b)} (minima), lcm = 2³·3²·5·7 = {a*b//math.gcd(a,b)} (maxima)', fontsize=9)
    save('P11-e3')


@fig('P11-x1')
def _():
    ax = plt.gca()
    a = np.arange(0, 12)
    ax.scatter(a, a * math.log10(2), color=C1, label='log 2ᵃ'); ax.scatter(a, a * math.log10(3), color=C4, marker='s', label='log 3ᵇ')
    ax.set_xlabel('exponent'); ax.legend(fontsize=8)
    ax.set_title('2ᵃ is even and 3ᵇ is odd: the two families meet only at 1 (a = b = 0)', fontsize=9)
    save('P11-x1')


@fig('P11-x2')
def _():
    ax = plt.gca()
    a, b = 2 ** 2 * 3 ** 4, 5 ** 2 * 7 ** 2
    ps = [2, 3, 5, 7]
    ax.bar(range(4), [factor(a).get(p, 0) for p in ps], color=C1, label=f'a = {a}')
    ax.bar(range(4), [factor(b).get(p, 0) for p in ps], color=C4, label=f'b = {b}')
    ax.set_xticks(range(4)); ax.set_xticklabels(map(str, ps)); ax.set_ylabel('exponent'); ax.set_yticks(range(5)); ax.legend(fontsize=8)
    ax.set_title('gcd(a,b) = 1: each prime belongs to a or to b; ab square ⇒ every bar even', fontsize=9)
    save('P11-x2')


@fig('P11-x3')
def _():
    ax = plt.gca()
    for a in range(0, 7):
        for b in range(0, 7):
            c1 = (a - 1) % 2 == 0 and b % 2 == 0
            c2 = a % 3 == 0 and (b - 1) % 3 == 0
            col = C2 if c1 and c2 else (C1 if c1 else (C4 if c2 else '#eeeeee'))
            ax.scatter(a, b, s=120, color=col)
    ax.scatter([], [], color=C1, label='n/2 is a square'); ax.scatter([], [], color=C4, label='n/3 is a cube'); ax.scatter([], [], color=C2, label='both')
    ax.set_xlabel('a (exponent of 2)'); ax.set_ylabel('b (exponent of 3)'); ax.legend(fontsize=8, loc='upper right')
    ax.set_title('n = 2ᵃ3ᵇ: the first red point is (3, 4), n = 648', fontsize=9)
    save('P11-x3')


@fig('P11-x4')
def _():
    ax = plt.gca()
    D8, D9 = [1, 2, 4, 8], [1, 3, 9]
    for i, a in enumerate(D8):
        for j, b in enumerate(D9):
            ax.add_patch(plt.Rectangle((i, j), .95, .95, fc='#c6dbef'))
            ax.text(i + .47, j + .47, str(a * b), ha='center', va='center')
    for i, a in enumerate(D8): ax.text(i + .47, -.4, str(a), ha='center', color=C1)
    for j, b in enumerate(D9): ax.text(-.4, j + .47, str(b), va='center', color=C4)
    ax.text(2, -1, 'row sums × column sums: 15 · 13 = 195', ha='center')
    ax.set_xlim(-.8, 4.2); ax.set_ylim(-1.3, 3.2); ax.set_aspect('equal'); ax.axis('off')
    ax.set_title('σ(72): the divisors fill a grid, so σ(72) = σ(8)·σ(9)', fontsize=9)
    save('P11-x4')


@fig('P12-e1')
def _():
    ax = plt.gca()
    ns = np.arange(1, 31)
    C = [math.comb(2 * n, n) for n in ns]
    P = [math.prod(p for p in PR if n < p <= 2 * n) for n in ns]
    ax.plot(ns, [math.log(c) for c in C], 'o-', color=C1, label='log C(2n, n)', ms=3)
    ax.plot(ns, ns * math.log(4), color=C2, label='n log 4')
    ax.plot(ns, [math.log(p) for p in P], 's-', color=C3, label='log Π_{n<p≤2n} p', ms=3)
    ax.legend(fontsize=8); ax.set_xlabel('n')
    ax.set_title('primes in (n, 2n] divide C(2n,n) ≤ 4ⁿ, so their product is at most 4ⁿ', fontsize=9)
    save('P12-e1')


@fig('P12-e2')
def _():
    ax = plt.gca()
    ns = np.arange(1, 9)
    P = [n * (n + 1) * (n + 2) * (n + 3) for n in ns]
    up = [(n * n + 3 * n + 1) ** 2 - x for n, x in zip(ns, P)]
    down = [x - (n * n + 3 * n) ** 2 for n, x in zip(ns, P)]
    ax.bar(ns - .2, down, .4, color=C1, label='P − (n²+3n)²  (distance to the square below)')
    ax.bar(ns + .2, up, .4, color=C2, label='(n²+3n+1)² − P  (always 1)')
    for n, d in zip(ns, down):
        ax.text(n - .2, d + 2, str(d), ha='center', fontsize=7)
    ax.set_xlabel('n'); ax.legend(fontsize=8)
    ax.set_title('P = n(n+1)(n+2)(n+3) lies strictly between two consecutive squares', fontsize=9)
    save('P12-e2')


@fig('P12-e3')
def _():
    ax = plt.gca()
    X = 3000
    d = np.zeros(X + 1)
    for k in range(1, X + 1):
        d[k::k] += 1
    xs = np.arange(1, X + 1)
    ax.plot(xs, d[1:], '.', ms=1, color='#bbbbbb', label='d(n)')
    ax.plot(xs, np.cumsum(d[1:]) / xs, color=C1, label='average of d(1…n)')
    ax.plot(xs, np.log(xs) + 2 * 0.5772 - 1, '--', color=C2, label='log n + 2γ − 1')
    ax.set_ylim(0, 30); ax.legend(fontsize=8); ax.set_xlabel('n')
    ax.set_title('d(n) jumps around, but its average grows like log n', fontsize=9)
    save('P12-e3')


@fig('P12-x1')
def _():
    ax = plt.gca()
    for n in range(1, 9):
        ax.plot([n - .3, n + .3], [n * n] * 2, color=C1); ax.plot([n - .3, n + .3], [(n + 1) ** 2] * 2, color=C1)
        ax.scatter(n, n * n + n + 1, color=C2, zorder=3)
    ax.set_xlabel('n'); ax.set_title('n² < n² + n + 1 < (n+1)²: trapped strictly between consecutive squares', fontsize=9)
    save('P12-x1')


@fig('P12-x2')
def _():
    ax = plt.gca()
    n = np.arange(1, 31)
    lf = [math.lgamma(k + 1) for k in n]
    ax.plot(n, lf, 'o', color=C1, ms=3, label='log n!')
    ax.plot(n, n * np.log(n), color=C2, label='n log n')
    ax.plot(n, n * np.log(n) - n, color=C3, label='n log n − n')
    ax.legend(fontsize=8); ax.set_xlabel('n')
    ax.set_title('(n/e)ⁿ ≤ n! ≤ nⁿ, on a log scale', fontsize=9)
    save('P12-x2')


@fig('P12-x3')
def _():
    ax = plt.gca()
    xs = np.arange(1, 201)
    pi = np.cumsum([isp(k) for k in xs])
    ax.step(xs, pi, color=C1, label='π(x)')
    ax.plot(xs, xs / 3 + 2, color=C2, label='x/3 + 2')
    ax.legend(fontsize=8); ax.set_xlabel('x')
    ax.set_title('primes > 3 are ≡ ±1 mod 6, so π(x) ≤ x/3 + 2', fontsize=9)
    save('P12-x3')


# ================= toolkit lessons (T01–T13) =================
@fig('T01-e1')
def _():
    ax = plt.gca(); n = 10
    for k in range(1, n + 1):
        ax.text(k, 1, str(k), ha='center', va='center', color=C1)
        ax.text(k, 0, str(n + 1 - k), ha='center', va='center', color=C2)
        ax.text(k, -1, str(n + 1), ha='center', va='center', weight='bold')
    ax.text(0, 1, 'S =', ha='right', va='center'); ax.text(0, 0, 'S =', ha='right', va='center'); ax.text(0, -1, '2S =', ha='right', va='center')
    ax.plot([0.5, n + .5], [-.5, -.5], color=GR)
    ax.set_xlim(-1, n + 1); ax.set_ylim(-1.6, 1.6); ax.axis('off')
    ax.set_title('1+2+...+10 written twice (shown for n = 10): every column sums to 11, so 2S = 10·11', fontsize=9)
    save('T01-e1')


@fig('T01-e2')
def _():
    ax = plt.gca(); K = 8
    for k in range(1, K + 1):
        ax.bar(k, 1 / k, width=.8, color='#dde8f3', edgecolor=C1)
        ax.bar(k, 1 / k - 1 / (k + 1), bottom=1 / (k + 1), width=.8, color=C2, alpha=.6)
    ax.set_xlabel('k'); ax.set_ylabel('1/k')
    ax.set_title('red part of bar k = 1/k − 1/(k+1) = 1/(k(k+1)); red parts stack to 1 − 1/(K+1)', fontsize=9)
    save('T01-e2')


@fig('T01-e3')
def _():
    ax = plt.gca()
    x0, y0, w, h = 0, 0, 1, 1
    cols = [C1, C2, C3, C4, '#9467bd', '#8c564b', '#e377c2']
    for k in range(7):
        if k % 2 == 0:
            ax.add_patch(plt.Rectangle((x0, y0), w / 2, h, fc=cols[k], alpha=.55, ec='k'))
            ax.text(x0 + w / 4, y0 + h / 2, f'1/{2**(k+1)}', ha='center', va='center', fontsize=max(6, 11 - k))
            x0 += w / 2; w /= 2
        else:
            ax.add_patch(plt.Rectangle((x0, y0), w, h / 2, fc=cols[k], alpha=.55, ec='k'))
            ax.text(x0 + w / 2, y0 + h / 4, f'1/{2**(k+1)}', ha='center', va='center', fontsize=max(6, 11 - k))
            y0 += h / 2; h /= 2
    ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.set_aspect('equal'); ax.axis('off')
    ax.set_title('1/2 + 1/4 + 1/8 + ... fills the unit square but never all of it', fontsize=9)
    save('T01-e3')


def _divgrid(ax, x, weight=lambda d: 1, title=''):
    for n in range(1, x + 1):
        for d in range(1, x + 1):
            if n % d == 0:
                ax.scatter(n, d, s=30 + 8 * weight(d), color=C1)
    ax.set_xticks(range(1, x + 1)); ax.set_yticks(range(1, x + 1))
    ax.set_xlabel('n (columns: sum over d | n)'); ax.set_ylabel('d (rows: ⌊x/d⌋ points)')
    ax.grid(alpha=.3); ax.set_title(title, fontsize=9)


@fig('T01-e4')
def _():
    _divgrid(plt.gca(), 10, title='pairs (d, n) with d | n ≤ 10: 27 points counted by columns or by rows')
    save('T01-e4')


@fig('T01-x1')
def _():
    ax = plt.gca(); n = 6
    cols = [C1, C2, C3, C4, '#9467bd', '#8c564b']
    for k in range(1, n + 1):
        for i in range(k):
            for j in range(k):
                if max(i, j) == k - 1:
                    ax.add_patch(plt.Rectangle((i, j), 1, 1, fc=cols[k - 1], alpha=.6, ec='w'))
        ax.text(k - .5, k - .5, str(2 * k - 1), ha='center', va='center', fontsize=8, weight='bold')
    ax.set_xlim(0, n); ax.set_ylim(0, n); ax.set_aspect('equal'); ax.axis('off')
    ax.set_title('1 + 3 + 5 + ... + 11 = 6²: each L-shaped layer adds 2k − 1 squares', fontsize=9)
    save('T01-x1')


@fig('T01-x2')
def _():
    ax = plt.gca(); ns = np.arange(2, 31)
    P = np.cumprod([1 - 1 / k ** 2 for k in ns])
    ax.plot(ns, P, 'o', color=C1, ms=4, label='P(n) = ∏(1 − 1/k²)')
    ax.plot(ns, (ns + 1) / (2 * ns), '-', color=C2, label='(n+1)/(2n)')
    ax.axhline(.5, color=GR, ls='--'); ax.legend(fontsize=8); ax.set_xlabel('n')
    ax.set_title('telescoping product: P(n) = (n+1)/(2n) → 1/2', fontsize=9)
    save('T01-x2')


@fig('T01-x3')
def _():
    _divgrid(plt.gca(), 6, weight=lambda d: 6 * d, title='x = 6: point in row d weighs d; total = Σ σ(n) = Σ d⌊6/d⌋ = 33')
    save('T01-x3')


@fig('T01-x4')
def _():
    ax = plt.gca(); ns = np.arange(1, 11)
    S = np.cumsum([k * 2 ** k for k in ns])
    ax.semilogy(ns, S, 'o', color=C1, label='S(n) = Σ k·2^k')
    ax.semilogy(ns, (ns - 1) * 2.0 ** (ns + 1) + 2, '-', color=C2, label='(n−1)·2^(n+1) + 2')
    ax.legend(fontsize=8); ax.set_xlabel('n')
    ax.set_title('the closed form matches every partial sum', fontsize=9)
    save('T01-x4')


def _unit(ax, lim=1.35):
    t = np.linspace(0, 2 * np.pi, 300)
    ax.plot(np.cos(t), np.sin(t), color=GR, lw=.8)
    ax.axhline(0, color=GR, lw=.5); ax.axvline(0, color=GR, lw=.5)
    ax.set_xlim(-lim, lim); ax.set_ylim(-lim, lim); ax.set_aspect('equal')


def _arrow(ax, z, color, label=None, start=0j):
    ax.annotate('', xy=(z.real, z.imag), xytext=(start.real, start.imag),
                arrowprops=dict(arrowstyle='->', color=color, lw=1.6))
    if label:
        ax.text(z.real * 1.08 + .05, z.imag * 1.08 + .05, label, color=color, fontsize=9)


@fig('T02-e1')
def _():
    ax = plt.gca()
    for z, c, l in [(1 + 2j, C1, '1+2i'), (3 - 1j, C3, '3−i'), (5 + 5j, C2, '5+5i')]:
        _arrow(ax, z, c, l)
    ax.axhline(0, color=GR, lw=.5); ax.axvline(0, color=GR, lw=.5)
    ax.set_xlim(-1, 6.5); ax.set_ylim(-1.8, 6); ax.set_aspect('equal')
    ax.set_title('lengths √5·√10 = 5√2; angles 63.4° + (−18.4°) = 45°', fontsize=9)
    save('T02-e1')


@fig('T02-e2')
def _():
    fig_, (a, b) = plt.subplots(1, 2, figsize=(6.4, 3.2))
    w = [cmath.exp(2j * pi * k / 3) for k in range(3)]
    _unit(a)
    for k, z in enumerate(w):
        _arrow(a, z, [C1, C2, C3][k], ['1', 'ω', 'ω²'][k])
    a.set_title('z³ = 1: three roots', fontsize=9)
    _unit(b); p = 0j
    for k, z in enumerate(w):
        _arrow(b, p + z, [C1, C2, C3][k], start=p); p += z
    b.set_title('head to tail: 1 + ω + ω² = 0', fontsize=9)
    save('T02-e2')


@fig('T02-e3')
def _():
    ax = plt.gca(); n = 6; ks = np.arange(n + 1)
    cs = [comb(n, k) for k in ks]
    ax.bar(ks, cs, color=[C2 if k % 3 == 0 else '#c9d6e6' for k in ks])
    for k, c in zip(ks, cs):
        ax.text(k, c + .4, str(c), ha='center', fontsize=9)
    ax.set_xlabel('k'); ax.set_title('C(6,k): filter keeps 3 | k → 1 + 20 + 1 = 22 = (2⁶ + 2cos 2π)/3', fontsize=9)
    save('T02-e3')


@fig('T02-e4')
def _():
    ax = plt.gca(); th = 1.9; z = cmath.exp(1j * th)
    _unit(ax, 2.2)
    _arrow(ax, 1, C1, '1'); _arrow(ax, z, C3, 'e^(iθ)')
    ax.plot([1, 1 + z.real], [0, z.imag], color=C3, ls='--', lw=.8); ax.plot([z.real, 1 + z.real], [z.imag, z.imag], color=C1, ls='--', lw=.8)
    _arrow(ax, 1 + z, C2, '1 + e^(iθ)')
    ax.set_title('rhombus: |1 + e^(iθ)| = 2|cos(θ/2)| (here θ = 1.9)', fontsize=9)
    save('T02-e4')


@fig('T02-x1')
def _():
    ax = plt.gca(); p = 1 + 0j
    for k in range(9):
        z = (1 + 1j) ** k
        ax.scatter(z.real, z.imag, color=C1, s=20, zorder=3)
        ax.text(z.real + .3, z.imag + .3, f'k={k}', fontsize=7)
        if k:
            ax.plot([p.real, z.real], [p.imag, z.imag], color=C1, lw=.8)
        p = z
    ax.axhline(0, color=GR, lw=.5); ax.axvline(0, color=GR, lw=.5); ax.set_aspect('equal')
    ax.set_title('(1+i)^k: length ×√2, angle +45° each step; k = 8 gives 16', fontsize=9)
    save('T02-x1')


@fig('T02-x2')
def _():
    fig_, (a, b) = plt.subplots(1, 2, figsize=(6.4, 3.2))
    w = [cmath.exp(2j * pi * 2 * k / 5) for k in range(5)]
    _unit(a)
    for k in range(5):
        z0 = w[k]; z1 = w[(k + 1) % 5]
        a.plot([z0.real, z1.real], [z0.imag, z1.imag], color=C1)
        a.text(z0.real * 1.15, z0.imag * 1.15, 'ω' + '⁰²⁴⁶⁸'[k], fontsize=9, ha='center')
    a.set_title('ω^{2k}: star order', fontsize=9)
    _unit(b, 2.2); p = 0j
    for z in w:
        _arrow(b, p + z, C2, start=p); p += z
    b.set_title('head to tail: sum = 0', fontsize=9)
    save('T02-x2')


@fig('T02-x3')
def _():
    ax = plt.gca(); _unit(ax)
    for k in range(12):
        z = cmath.exp(2j * pi * k / 12)
        prim = gcd(k, 12) == 1
        ax.scatter(z.real, z.imag, s=60 if prim else 25, color=C2 if prim else C1, zorder=3)
        ax.text(z.real * 1.17, z.imag * 1.17, str(k), ha='center', va='center', fontsize=8, color=C2 if prim else 'k')
    ax.set_title('12th roots of unity e(k/12); primitive: k = 1, 5, 7, 11', fontsize=9)
    save('T02-x3')


@fig('T02-x4')
def _():
    ax = plt.gca(); n = 8; ks = np.arange(n + 1)
    cs = [comb(n, k) for k in ks]
    ax.bar(ks, cs, color=[C2 if k % 4 == 0 else '#c9d6e6' for k in ks])
    for k, c in zip(ks, cs):
        ax.text(k, c + 1, str(c), ha='center', fontsize=9)
    ax.set_xlabel('k'); ax.set_title('C(8,k): filter keeps 4 | k → 1 + 70 + 1 = 72 = (256 + 16 + 16)/4', fontsize=9)
    save('T02-x4')


@fig('T03-e1')
def _():
    ax = plt.gca(); p = 7; els = list(range(1, p))
    order = {a: next(k for k in range(1, p) if pow(a, k, p) == 1) for a in els}
    _grid_table(ax, els, els, lambda r, c: r * c % p,
                'multiplication mod 7 (1s highlighted); right: order of a',
                hl=lambda r, c: '#f6c9c9' if (r * c) % p == 1 else None, rlab='a', clab='b')
    for i, a in enumerate(els):
        ax.text(len(els) + .4, -i, f'ord {order[a]}', fontsize=8, va='center', color=C2 if order[a] == 6 else 'k')
    ax.set_xlim(-1.1, len(els) + 1.6)
    save('T03-e1')


@fig('T03-e2')
def _():
    ax = plt.gca(); H = [1, 2, 4, 8]; H7 = [7, 14, 13, 11]
    for i, x in enumerate(H):
        ax.add_patch(plt.Circle((i, 1), .35, fc='#dde8f3', ec=C1)); ax.text(i, 1, str(x), ha='center', va='center')
    for i, x in enumerate(H7):
        ax.add_patch(plt.Circle((i, 0), .35, fc='#f6dada', ec=C2)); ax.text(i, 0, str(x), ha='center', va='center')
    ax.text(-.9, 1, 'H = ⟨2⟩', ha='right', va='center', color=C1); ax.text(-.9, 0, '7H', ha='right', va='center', color=C2)
    for i in range(3):
        ax.annotate('', xy=(i + .62, 1), xytext=(i + .38, 1), arrowprops=dict(arrowstyle='->', color=GR))
    ax.text(1.5, 1.55, '×2', color=GR, ha='center')
    ax.set_xlim(-2.2, 3.6); ax.set_ylim(-.7, 1.8); ax.set_aspect('equal'); ax.axis('off')
    ax.set_title('(ℤ/15)^× = H ∪ 7H: two cosets of size 4, so |H| = 4 divides 8', fontsize=9)
    save('T03-e2')


@fig('T03-e3')
def _():
    ax = plt.gca()
    _grid_table(ax, [1, 3, 5, 7], [1, 3, 5, 7], lambda r, c: r * c % 8, 'multiplication mod 8: the diagonal is all 1s',
                hl=lambda r, c: '#f6c9c9' if r == c else None, rlab='a', clab='b')
    save('T03-e3')


@fig('T03-e4')
def _():
    fig_, axs = plt.subplots(1, 4, figsize=(6.4, 1.9))
    for j, ax in enumerate(axs):
        _unit(ax, 1.4)
        vals = [1j ** (j * k) for k in range(4)]
        for k, v in enumerate(vals):
            ax.scatter(v.real + .06 * k, v.imag + .06 * k, s=40, color=[C1, C2, C3, C4][k], zorder=3)
        ax.set_title(f'χ{j}: values at a = 1, 2, 4, 3', fontsize=7); ax.set_xticks([]); ax.set_yticks([])
    plt.suptitle('characters of (ℤ/5)^× (generator 2): χj(2^k) = i^(jk)', fontsize=9)
    save('T03-e4')


@fig('T03-x1')
def _():
    ax = plt.gca(); p = 11; els = list(range(1, p))
    ords = [next(k for k in range(1, p) if pow(a, k, p) == 1) for a in els]
    ax.bar(els, ords, color=[C2 if o == 10 else '#c9d6e6' for o in ords])
    ax.set_xticks(els); ax.set_yticks([1, 2, 5, 10]); ax.set_xlabel('a'); ax.set_ylabel('order of a mod 11')
    ax.set_title('orders divide 10; generators (order 10): 2, 6, 7, 8', fontsize=9)
    save('T03-x1')


@fig('T03-x2')
def _():
    fig_, (a, b) = plt.subplots(1, 2, figsize=(6.4, 3.0))
    for ax, p in [(a, 7), (b, 13)]:
        _unit(ax, 1.4)
        rs = [pow(10, k, p) for k in range(7)]
        for k in range(6):
            z0 = cmath.exp(2j * pi * rs[k] / p); z1 = cmath.exp(2j * pi * rs[k + 1] / p)
            ax.annotate('', xy=(z1.real, z1.imag), xytext=(z0.real, z0.imag), arrowprops=dict(arrowstyle='->', color=C1))
        for r in range(1, p):
            z = cmath.exp(2j * pi * r / p)
            ax.text(z.real * 1.2, z.imag * 1.2, str(r), fontsize=7, ha='center', va='center', color=C2 if r in rs else GR)
        ax.set_title(f'remainders 10^k mod {p}: cycle of 6', fontsize=9); ax.set_xticks([]); ax.set_yticks([])
    save('T03-x2')


@fig('T03-x3')
def _():
    ax = plt.gca(); ks = np.arange(0, 25)
    ax.plot(ks, [pow(3, int(k), 7) for k in ks], 'o-', color=C1, ms=4)
    for k in range(0, 25, 6):
        ax.axvline(k, color=GR, ls='--', lw=.7)
    ax.set_xlabel('k'); ax.set_ylabel('3^k mod 7'); ax.set_yticks(range(1, 7))
    ax.set_title('3^k mod 7 repeats with period 6; 3^100 ≡ 3^4 ≡ 4', fontsize=9)
    save('T03-x3')


@fig('T03-x4')
def _():
    ax = plt.gca(); p = 11
    for a in range(1, p):
        b = a * a % p
        ax.annotate('', xy=(1, b), xytext=(0, a), arrowprops=dict(arrowstyle='->', color=C1 if a <= 5 else C3, lw=1))
        ax.text(-.06, a, str(a), ha='right', va='center', fontsize=8)
    for b in sorted({a * a % p for a in range(1, p)}):
        ax.text(1.06, b, str(b), ha='left', va='center', fontsize=9, color=C2, weight='bold')
    ax.set_xlim(-.3, 1.3); ax.set_ylim(.3, 10.7); ax.axis('off')
    ax.text(0, 10.6, 'a', ha='center'); ax.text(1, 10.6, 'a² mod 11', ha='center')
    ax.set_title('a ↦ a² mod 11: each square {1,3,4,5,9} is hit twice (a and 11−a)', fontsize=9)
    save('T03-x4')


@fig('T04-e1')
def _():
    ax = plt.gca(); t = np.linspace(.7, 10.5, 400)
    for k in range(1, 10):
        ax.add_patch(plt.Rectangle((k, 0), 1, 1 / k, fc='#dde8f3', ec=C1, lw=.8))
    for k in range(2, 11):
        ax.add_patch(plt.Rectangle((k - 1, 0), 1, 1 / k, fc=C2, alpha=.35, ec=C2, lw=.8))
    ax.plot(t, 1 / t, color='k', lw=1.5, label='1/t')
    ax.set_xlim(.5, 10.8); ax.set_ylim(0, 1.15); ax.set_xlabel('t'); ax.legend(fontsize=8)
    ax.set_title('Σ_{k=2}^{10} 1/k  <  log 10 = ∫₁¹⁰ dt/t  <  Σ_{k=1}^{9} 1/k', fontsize=9)
    save('T04-e1')


@fig('T04-e2')
def _():
    ax = plt.gca(); t = np.linspace(1, 10.6, 300)
    for k in range(2, 11):
        ax.add_patch(plt.Rectangle((k - .5, 0), 1, np.log(k), fc='#dde8f3', ec=C1, lw=.8))
    ax.plot(t, np.log(t), color=C2, lw=1.5, label='log t')
    ax.set_xlabel('t'); ax.legend(fontsize=8)
    ax.set_title('log 10! = Σ log k = 15.10 (bars)  vs  ∫₁¹⁰ log t dt = 14.03', fontsize=9)
    save('T04-e2')


@fig('T04-e3')
def _():
    ax = plt.gca(); u = np.linspace(0, 40, 600)
    ax.plot(u, u, color=C1, label='log x  (= u)')
    ax.plot(u, np.exp(.1 * u), color=C2, label='x^0.1  (= e^{0.1u})')
    for r in (1.118, 35.77):
        ax.axvline(r, color=GR, ls='--', lw=.8)
    ax.set_ylim(0, 45); ax.set_xlabel('u = log x'); ax.legend(fontsize=8)
    ax.set_title('crossings at x ≈ 3.06 and x ≈ 3.4·10^15', fontsize=9)
    save('T04-e3')


@fig('T04-e4')
def _():
    ax = plt.gca(); x = np.linspace(0, 2, 300)
    ax.plot(x, x, color=C1, label='x'); ax.plot(x, np.log1p(x), color='k', lw=2, label='log(1+x)')
    ax.plot(x, x - x ** 2 / 2, color=C2, label='x − x²/2')
    ax.set_xlabel('x'); ax.legend(fontsize=8)
    ax.set_title('x − x²/2 ≤ log(1+x) ≤ x for x ≥ 0', fontsize=9)
    save('T04-e4')


@fig('T04-x1')
def _():
    ax = plt.gca(); x = np.linspace(.02, 1.6, 300)
    ax.plot(x, x ** x, color=C1)
    ax.scatter([1 / np.e], [np.exp(-1 / np.e)], color=C2, zorder=3)
    ax.annotate('x = 1/e, value e^(−1/e) ≈ 0.692', (1 / np.e, np.exp(-1 / np.e)), xytext=(.6, .9), arrowprops=dict(arrowstyle='->'), fontsize=8)
    ax.set_xlabel('x'); ax.set_title('y = x^x', fontsize=9)
    save('T04-x1')


@fig('T04-x2')
def _():
    ax = plt.gca(); t = np.linspace(2.2, 16, 400); f = 1 / (t * np.log(t))
    ax.plot(t, f, color=C1); tt = np.linspace(np.e, np.e ** np.e, 300)
    ax.fill_between(tt, 1 / (tt * np.log(tt)), color=C2, alpha=.3)
    ax.text(6.5, .1, 'area = 1', color=C2)
    ax.set_xlabel('t'); ax.set_title('∫ from e to e^e of dt/(t log t) = log log t |  = 1', fontsize=9)
    save('T04-x2')


@fig('T04-x3')
def _():
    ax = plt.gca(); n = np.unique(np.logspace(0, 4, 40).astype(int))
    ax.semilogx(n, (1 + 1 / n) ** n, 'o-', color=C1, ms=3)
    ax.axhline(np.e, color=C2, ls='--', label='e'); ax.legend(fontsize=8); ax.set_xlabel('n')
    ax.set_title('(1 + 1/n)^n increases to e', fontsize=9)
    save('T04-x3')


@fig('T04-x4')
def _():
    ax = plt.gca(); n = np.arange(2, 80)
    ax.plot(n, n * np.log(2), color=C1, label='n·log 2  (log of 2^n)')
    ax.plot(n, 10 * np.log(n), color=C2, label='10·log n  (log of n^10)')
    ax.axvline(59, color=GR, ls='--'); ax.text(60, 15, 'n = 59', fontsize=8)
    ax.set_xlabel('n'); ax.legend(fontsize=8); ax.set_title('2^n overtakes n^10 at n = 59', fontsize=9)
    save('T04-x4')


@fig('T05-e1')
def _():
    ax = plt.gca(); ks = np.arange(0, 13); ns = 2 ** ks
    H = np.cumsum(1 / np.arange(1, ns[-1] + 1))
    ax.plot(ks, H[ns - 1], 'o-', color=C1, label='S(2^k)')
    ax.plot(ks, 1 + ks / 2, '--', color=C2, label='1 + k/2 (lower bound)')
    ax.plot(ks, ks * np.log(2) + 0.5772, ':', color=GR, label='k·log 2 + γ')
    ax.set_xlabel('k  (n = 2^k)'); ax.legend(fontsize=8)
    ax.set_title('harmonic partial sums grow without bound, but only like log n', fontsize=9)
    save('T05-e1')


@fig('T05-e2')
def _():
    ax = plt.gca(); n = np.arange(2, 13)
    ax.bar(n - .2, 1 / n ** 2, width=.4, color=C1, label='1/n²')
    ax.bar(n + .2, 1 / (n * (n - 1)), width=.4, color=C2, alpha=.7, label='1/(n(n−1)) = 1/(n−1) − 1/n')
    ax.set_xlabel('n'); ax.legend(fontsize=8)
    ax.set_title('Σ_{n≥2} 1/n² < Σ_{n≥2} 1/(n(n−1)) = 1, so ζ(2) < 2 (true value 1.645)', fontsize=9)
    save('T05-e2')


@fig('T05-e3')
def _():
    ax = plt.gca(); N = 60
    a = np.cumsum([(-1) ** (n + 1) / n for n in range(1, N + 1)])
    terms = []
    for j in range(1, N // 3 + 1):
        terms += [1 / (2 * j - 1), -1 / (4 * j - 2), -1 / (4 * j)]
    b = np.cumsum(terms)
    ax.plot(range(1, N + 1), a, '.-', color=C1, lw=.7, label='1 − 1/2 + 1/3 − ...')
    ax.plot(range(1, len(b) + 1), b, '.-', color=C2, lw=.7, label='1 − 1/2 − 1/4 + 1/3 − ...')
    ax.axhline(np.log(2), color=C1, ls='--', lw=.8); ax.axhline(np.log(2) / 2, color=C2, ls='--', lw=.8)
    ax.set_xlabel('number of terms'); ax.legend(fontsize=8)
    ax.set_title('same terms, different order: log 2 ≈ 0.693 vs ½ log 2 ≈ 0.347', fontsize=9)
    save('T05-e3')


@fig('T05-e4')
def _():
    ax = plt.gca(); N = 10 ** 6; n = np.arange(2, N, dtype=float)
    s1 = np.cumsum(1 / (n * np.log(n))); s2 = np.cumsum(1 / (n * np.log(n) ** 2))
    idx = np.unique(np.logspace(0, np.log10(N - 3), 200).astype(int))
    ax.semilogx(n[idx], s1[idx], color=C1, label='Σ 1/(n log n)  (diverges)')
    ax.semilogx(n[idx], s2[idx], color=C2, label='Σ 1/(n log² n)  (→ 2.11)')
    ax.axhline(2.1097, color=C2, ls='--', lw=.8)
    ax.set_xlabel('N'); ax.legend(fontsize=8); ax.set_title('partial sums up to N = 10^6', fontsize=9)
    save('T05-e4')


@fig('T05-x1')
def _():
    ax = plt.gca(); N = np.arange(1, 21)
    ax.plot(N, np.cumsum(N / 2.0 ** N), 'o-', color=C1); ax.axhline(2, color=C2, ls='--')
    ax.set_xlabel('N'); ax.set_title('Σ_{n≤N} n/2^n = 2 − (N+2)/2^N → 2', fontsize=9)
    save('T05-x1')


@fig('T05-x2')
def _():
    ax = plt.gca(); N = np.arange(1, 31)
    tail = [np.pi ** 2 / 6 - sum(1 / k ** 2 for k in range(1, m + 1)) for m in N]
    ax.plot(N, tail, 'o', color=C1, ms=4, label='Σ_{n>N} 1/n²'); ax.plot(N, 1 / N, '-', color=C2, label='1/N')
    ax.plot(N, 1 / (N + 1), ':', color=GR, label='1/(N+1)')
    ax.set_xlabel('N'); ax.legend(fontsize=8); ax.set_title('the tail is squeezed between 1/(N+1) and 1/N', fontsize=9)
    save('T05-x2')


@fig('T05-x3')
def _():
    ax = plt.gca(); N = np.arange(2, 41)
    ax.plot(N, (N + 1) / (2 * N), 'o-', color=C1, ms=3); ax.axhline(.5, color=C2, ls='--')
    ax.set_xlabel('N'); ax.set_title('∏_{n=2}^N (1 − 1/n²) = (N+1)/(2N) → 1/2', fontsize=9)
    save('T05-x3')


@fig('T05-x4')
def _():
    ax = plt.gca(); n = np.arange(1, 41)
    ax.plot(n, n ** (1 / n), 'o-', color=C1, ms=3); ax.axhline(1, color=GR, ls='--'); ax.axhline(3 ** (1 / 3), color=C2, ls=':')
    ax.text(25, 3 ** (1 / 3) + .01, 'max ∛3 ≈ 1.442 at n = 3', color=C2, fontsize=8)
    ax.set_xlabel('n'); ax.set_title('n^(1/n) stays below 1.45, so 1/n^(1+1/n) > 1/(1.45 n)', fontsize=9)
    save('T05-x4')


@fig('T06-e1')
def _():
    ax = plt.gca(); x = np.linspace(1, 40, 2000); N = np.floor(x)
    ax.plot(x, N * (N + 1) / 2 - x ** 2 / 2, color=C1, lw=1, label='Σ_{n≤x} n − x²/2')
    ax.plot(x, x / 2 + 1 / 8, '--', color=C2, lw=.8, label='±(x/2 + 1/8)'); ax.plot(x, -x / 2 - 1 / 8, '--', color=C2, lw=.8)
    ax.set_xlabel('x'); ax.legend(fontsize=8); ax.set_title('the error stays inside a band of width O(x)', fontsize=9)
    save('T06-e1')


@fig('T06-e2')
def _():
    ax = plt.gca(); x = np.linspace(1, 300, 3000); N = np.floor(x).astype(int)
    H = np.cumsum(1 / np.arange(1, 301))[N - 1]
    ax.plot(x, H - np.log(x), color=C1, label='H(x) − log x')
    ax.axhline(0.5772, color=C2, ls='--', label='γ'); ax.axhline(1, color=GR, ls=':'); ax.axhline(0, color=GR, ls=':')
    ax.set_xlabel('x'); ax.legend(fontsize=8); ax.set_title('H(x) = log x + O(1): the difference stays in [0, 1]', fontsize=9)
    save('T06-e2')


@fig('T06-e3')
def _():
    ax = plt.gca(); x = np.logspace(1, 8, 200)
    for f, l, c in [(x * np.log(x), 'x log x', 'k'), (x, 'x', C1), (np.sqrt(x) * np.log(x), '√x log x', C2), (np.sqrt(x), '√x', C3)]:
        ax.loglog(x, f, color=c, label=l)
    ax.set_xlabel('x'); ax.legend(fontsize=8); ax.set_title('(x + O(√x))(log x + O(1)) = x log x + O(x)', fontsize=9)
    save('T06-e3')


@fig('T06-e4')
def _():
    ax = plt.gca(); X = 20000
    d = np.zeros(X + 1, dtype=int)
    for k in range(1, X + 1):
        d[k::k] += 1
    D = np.cumsum(d[1:]); x = np.arange(1, X + 1)
    ax.semilogx(x[9:], (D[9:] - x[9:] * np.log(x[9:])) / x[9:], color=C1, lw=.6, label='(D(x) − x log x)/x')
    ax.axhline(2 * 0.5772 - 1, color=C2, ls='--', label='2γ − 1 ≈ 0.154')
    ax.set_xlabel('x'); ax.legend(fontsize=8); ax.set_title('Σ_{n≤x} d(n) = x log x + O(x)', fontsize=9)
    save('T06-e4')


@fig('T06-x1')
def _():
    ax = plt.gca(); x = np.logspace(.5, 12, 300)
    ax.semilogx(x, x ** 2 / x ** 3, label='(a) x²/x³', color=C1)
    ax.semilogx(x, np.log(x) / x ** .01, label='(c) log x / x^0.01', color=C2)
    ax.semilogx(x, 2 + 0 * x, label='(e) 2^{x+1}/2^x', color=C3)
    ax.semilogx(x, 1 + 1 / np.sqrt(x), label='(f) (x+√x)/x', color=C4)
    ax.set_ylim(0, 30); ax.set_xlabel('x'); ax.legend(fontsize=8); ax.set_title('ratios f/g for the statements', fontsize=9)
    save('T06-x1')


@fig('T06-x2')
def _():
    ax = plt.gca(); X = 5000; x = np.arange(1, X + 1)
    S = np.cumsum(np.sqrt(x))
    ax.plot(x, (S - 2 / 3 * x ** 1.5) / np.sqrt(x), color=C1); ax.axhline(.5, color=C2, ls='--')
    ax.set_xlabel('x'); ax.set_title('(Σ√n − ⅔x^{3/2})/√x → ½', fontsize=9)
    save('T06-x2')


@fig('T06-x3')
def _():
    ax = plt.gca(); x = np.logspace(0, 4, 100)
    ax.semilogx(x, x * (np.e - (1 + 1 / x) ** x), color=C1); ax.axhline(np.e / 2, color=C2, ls='--', label='e/2')
    ax.set_xlabel('x'); ax.legend(fontsize=8); ax.set_title('x·(e − (1+1/x)^x) ≤ e/2', fontsize=9)
    save('T06-x3')


@fig('T06-x4')
def _():
    ax = plt.gca(); X = 200; x = np.arange(1, X + 1)
    tail = np.pi ** 2 / 6 - np.cumsum(1 / x ** 2)
    ax.plot(x, x * tail, color=C1); ax.axhline(1, color=C2, ls='--')
    ax.set_xlabel('x'); ax.set_title('x·(ζ(2) − Σ_{n≤x} 1/n²) → 1', fontsize=9)
    save('T06-x4')


@fig('T07-e1')
def _():
    fig_, (a1, a2) = plt.subplots(1, 2, figsize=(6.6, 3.2))
    X = 3000; x = np.arange(1, X + 1); H = np.cumsum(1 / x); g = 0.5772156649
    a1.semilogx(x, H - np.log(x), color=C1, label='H(x) − log x'); a1.axhline(g, color=C2, ls='--', label='γ ≈ 0.5772')
    a1.set_xlabel('x'); a1.legend(fontsize=8); a1.set_title('H(x) − log x → γ', fontsize=9)
    a2.semilogx(x, x * (H - np.log(x) - g), color=C1); a2.axhline(.5, color=C2, ls='--', label='½')
    a2.set_ylim(0.3, 0.55); a2.set_xlabel('x (integer)'); a2.legend(fontsize=8); a2.set_title('x·(H(x) − log x − γ) → ½', fontsize=9)
    save('T07-e1')


@fig('T07-e2')
def _():
    ax = plt.gca(); n = np.arange(1, 301)
    from math import lgamma
    lf = np.array([lgamma(k + 1) for k in n])
    ax.plot(n, lf - (n * np.log(n) - n), color=C1, label='log n! − (n log n − n)')
    ax.plot(n, .5 * np.log(2 * np.pi * n), color=C2, ls='--', label='½ log(2πn)')
    ax.plot(n, np.log(n + 1), color=GR, ls=':', label='log(n+1): bound from the proof')
    ax.set_xlabel('n'); ax.legend(fontsize=8); ax.set_title('the difference grows only like ½ log n', fontsize=9)
    save('T07-e2')


@fig('T07-e3')
def _():
    fig_, (a1, a2) = plt.subplots(1, 2, figsize=(6.6, 3.2))
    X = 100000; d = np.zeros(X + 1)
    for k in range(1, X + 1):
        d[k::k] += 1
    x = np.arange(1, X + 1); S = np.cumsum(d[1:] / x); L = np.log(x)
    idx = np.unique(np.logspace(0, 5, 400).astype(int)) - 1
    a1.semilogx(x[idx], S[idx], color=C1, label='Σ d(n)/n'); a1.semilogx(x[idx], .5 * L[idx] ** 2, color=C2, ls='--', label='½ log² x')
    a1.set_xlabel('x'); a1.legend(fontsize=8); a1.set_title('main term', fontsize=9)
    j = idx[idx >= 9]
    a2.semilogx(x[j], (S[j] - .5 * L[j] ** 2) / L[j], color=C1); a2.axhline(2 * 0.5772, color=C2, ls='--', label='2γ ≈ 1.154')
    a2.set_ylim(0, 2.5); a2.set_xlabel('x'); a2.legend(fontsize=8); a2.set_title('(Σ − ½ log² x)/log x stays bounded', fontsize=9)
    save('T07-e3')


@fig('T07-e4')
def _():
    ax = plt.gca(); n = np.arange(1, 41)
    from math import lgamma
    r = np.exp(np.array([lgamma(k + 1) for k in n]) - (.5 * np.log(2 * np.pi * n) + n * np.log(n) - n))
    ax.plot(n, r, 'o', ms=3, color=C1, label='n! / Stirling')
    ax.plot(n, 1 + 1 / (12 * n), color=C2, ls='--', label='1 + 1/(12n)')
    ax.axhline(1, color=GR, lw=.8); ax.set_xlabel('n'); ax.legend(fontsize=8); ax.set_title('Stirling: n! ~ √(2πn)(n/e)^n', fontsize=9)
    save('T07-e4')


@fig('T07-x1')
def _():
    ax = plt.gca(); X = 100000; x = np.arange(1, X + 1)
    S = np.cumsum(1 / np.sqrt(x)); idx = np.unique(np.logspace(0, 5, 400).astype(int)) - 1
    ax.semilogx(x[idx], S[idx] - 2 * np.sqrt(x[idx]), color=C1, label='Σ 1/√n − 2√x')
    ax.axhline(-1.4603545, color=C2, ls='--', label='C = ζ(½) ≈ −1.4604')
    ax.set_xlabel('x'); ax.legend(fontsize=8); ax.set_title('the constant C', fontsize=9)
    save('T07-x1')


@fig('T07-x2')
def _():
    ax = plt.gca(); X = 100000; x = np.arange(1, X + 1)
    S = np.cumsum(np.log(x) / x); idx = np.unique(np.logspace(0, 5, 400).astype(int)) - 1
    ax.semilogx(x[idx], S[idx] - .5 * np.log(x[idx]) ** 2, color=C1, label='Σ log n / n − ½ log² x')
    ax.axhline(-0.0728158, color=C2, ls='--', label='γ₁ ≈ −0.0728')
    ax.set_ylim(-0.4, 0.4); ax.set_xlabel('x'); ax.legend(fontsize=8); ax.set_title('Stieltjes constant γ₁', fontsize=9)
    save('T07-x2')


@fig('T07-x3')
def _():
    fig_, (a1, a2) = plt.subplots(1, 2, figsize=(6.6, 3.2))
    n = np.arange(1, 41); a = (-1.0) ** n
    a1.step(n, np.cumsum(a), where='post', color=C1); a1.set_ylim(-1.5, 0.5)
    a1.set_xlabel('x'); a1.set_title('A(x) = Σ_{n≤x} (−1)^n is bounded', fontsize=9)
    a2.plot(n, np.cumsum(a / n), 'o-', ms=3, lw=.7, color=C1, label='Σ_{n≤x} (−1)^n/n')
    a2.axhline(-np.log(2), color=C2, ls='--', label='−log 2')
    a2.set_xlabel('x'); a2.legend(fontsize=8); a2.set_title('converges', fontsize=9)
    save('T07-x3')


@fig('T07-x4')
def _():
    ax = plt.gca(); n = np.arange(1, 61)
    from math import lgamma
    lr = np.array([lgamma(2 * k + 1) - 2 * lgamma(k + 1) for k in n]) - (n * np.log(4) - .5 * np.log(np.pi * n))
    ax.plot(n, np.exp(lr), 'o', ms=3, color=C1, label='C(2n,n) / (4^n/√(πn))')
    ax.plot(n, 1 - 1 / (8 * n), color=C2, ls='--', label='1 − 1/(8n)')
    ax.axhline(1, color=GR, lw=.8); ax.set_xlabel('n'); ax.legend(fontsize=8); ax.set_title('central binomial coefficient', fontsize=9)
    save('T07-x4')


def _omega_upto(N):
    om = np.zeros(N + 1, dtype=np.int8)
    s = np.ones(N + 1, bool); s[:2] = False
    for i in range(2, int(N ** .5) + 1):
        if s[i]:
            s[i * i::i] = False
    for q in np.nonzero(s)[0]:
        om[q::q] += 1
    return om[1:]


@fig('T08-e1')
def _():
    fig_, ax = plt.subplots(figsize=(6.6, 2.2))
    for n in range(1, 31):
        r, c = divmod(n - 1, 10)
        col = '#9467bd' if n % 6 == 0 else C1 if n % 2 == 0 else C2 if n % 3 == 0 else 'white'
        ax.add_patch(plt.Rectangle((c, -r), .92, .92, fc=col, ec=GR, alpha=.85 if col != 'white' else 1))
        ax.text(c + .46, -r + .46, str(n), ha='center', va='center', fontsize=9, color='white' if col != 'white' else 'black')
    ax.set_xlim(-.1, 10); ax.set_ylim(-2.1, 1); ax.set_aspect('equal'); ax.axis('off')
    ax.set_title('blue: 2|n (15)   red: 3|n (10)   purple: 6|n (5) = 30·½·⅓', fontsize=9)
    save('T08-e1')


@fig('T08-e2')
def _():
    ax = plt.gca(); N = 200; d = np.zeros(N + 1)
    for k in range(1, N + 1):
        d[k::k] += 1
    n = np.arange(1, N + 1)
    ax.plot(n, d[1:], 'o', ms=2, color=GR, label='d(n)')
    ax.plot(n, np.cumsum(d[1:]) / n, color=C1, lw=1.5, label='average of d up to N')
    ax.plot(n, np.log(n) + 2 * 0.5772 - 1, color=C2, ls='--', label='log N + 2γ − 1')
    ax.set_xlabel('n, N'); ax.legend(fontsize=8); ax.set_title('E[d(n)] for n ≤ N', fontsize=9)
    save('T08-e2')


@fig('T08-e3')
def _():
    ax = plt.gca(); from math import comb
    k = np.arange(25, 76); p = np.array([comb(100, int(j)) / 2 ** 100 for j in k])
    tail = np.abs(k - 50) >= 10
    ax.bar(k[~tail], p[~tail], color=C1, width=.9); ax.bar(k[tail], p[tail], color=C2, width=.9, label='|X − 50| ≥ 10: 0.057')
    ax.set_xlabel('number of heads in 100 tosses'); ax.legend(fontsize=8); ax.set_title('Chebyshev bound: 25/10² = 0.25', fontsize=9)
    save('T08-e3')


@fig('T08-e4')
def _():
    ax = plt.gca(); o = _omega_upto(10 ** 6).astype(float)
    cnt = np.bincount(o.astype(int)) / len(o); mu, v = o.mean(), o.var()
    ax.bar(np.arange(len(cnt)), cnt, color=C1, width=.8, label='fraction of n ≤ 10⁶')
    z = np.linspace(-.5, 7.5, 300); ax.plot(z, np.exp(-(z - mu) ** 2 / (2 * v)) / np.sqrt(2 * np.pi * v), color=C2, label=f'normal, mean {mu:.2f}, var {v:.2f}')
    ax.set_xlabel('ω(n)'); ax.legend(fontsize=8); ax.set_title('distribution of ω(n)', fontsize=9)
    save('T08-e4')


@fig('T08-x1')
def _():
    ax = plt.gca(); P = np.array(PR[:40])
    ax.plot(np.arange(1, 41), np.cumprod(1 - 1 / P.astype(float) ** 2), 'o-', ms=3, color=C1, label='∏_{p ≤ p_k} (1 − 1/p²)')
    ax.axhline(6 / np.pi ** 2, color=C2, ls='--', label='6/π² ≈ 0.6079')
    ax.set_xlabel('k (number of primes)'); ax.legend(fontsize=8); ax.set_title('probability that two numbers are coprime', fontsize=9)
    save('T08-x1')


@fig('T08-x2')
def _():
    ax = plt.gca(); c = [8, 14, 7, 1]
    ax.bar(range(4), c, color=C1, width=.6)
    for i, v in enumerate(c):
        ax.text(i, v + .3, str(v), ha='center', fontsize=9)
    ax.axvline(31 / 30, color=C2, ls='--', label='E[X] = 31/30')
    ax.set_xticks(range(4)); ax.set_xlabel('X = number of p in {2,3,5} dividing n'); ax.set_ylabel('count, n ≤ 30')
    ax.legend(fontsize=8); ax.set_title('Var(X) = 569/900', fontsize=9)
    save('T08-x2')


@fig('T08-x3')
def _():
    ax = plt.gca(); N = 10 ** 6; d = np.zeros(N + 1, dtype=np.int32)
    for k in range(1, N + 1):
        d[k::k] += 1
    dd = d[1:]; a = np.arange(1, 241); h = np.bincount(dd, minlength=242)
    frac = 1 - np.cumsum(h)[a - 1] / N
    ax.semilogy(a, frac, color=C1, label='fraction with d(n) ≥ a')
    ax.semilogy(a, np.minimum(1, dd.mean() / a), color=C2, ls='--', label='Markov: E[d]/a')
    ax.axvline(100, color=GR, lw=.8); ax.set_xlabel('a'); ax.legend(fontsize=8); ax.set_title('n ≤ 10⁶', fontsize=9)
    save('T08-x3')


@fig('T08-x4')
def _():
    ax = plt.gca(); from math import comb
    k = np.arange(30, 71); p = np.array([comb(100, int(j)) / 2 ** 100 for j in k])
    inside = np.abs(k - 50) <= 10
    ax.bar(k[inside], p[inside], color=C1, width=.9, label='40 ≤ X ≤ 60: 0.9648')
    ax.bar(k[~inside], p[~inside], color=GR, width=.9)
    z = np.linspace(30, 70, 300); ax.plot(z, np.exp(-(z - 50) ** 2 / 50) / np.sqrt(50 * np.pi), color=C2, label='normal, μ = 50, σ = 5')
    ax.set_xlabel('number of heads'); ax.legend(fontsize=8); ax.set_title('central limit theorem', fontsize=9)
    save('T08-x4')


@fig('T09-e1')
def _():
    fig_, ax = plt.subplots(figsize=(4.6, 4.4)); _unit(ax, 1.15)
    s = 0.5 + 14.1347j; n = np.arange(1, 31); z = n ** (-s)
    ax.plot(z.real, z.imag, '-', color=GR, lw=.6)
    ax.scatter(z.real, z.imag, c=n, cmap='viridis', s=18, zorder=3)
    for k in (1, 2, 3, 10):
        ax.annotate(f'n={k}', (z[k - 1].real, z[k - 1].imag), fontsize=8, xytext=(4, 4), textcoords='offset points')
    ax.set_title('n^(−s), s = ½ + 14.1347i', fontsize=9)
    save('T09-e1')


@fig('T09-e2')
def _():
    fig_, ax = plt.subplots(figsize=(5.2, 3.6)); z = 0.5j; N = 12
    S = np.cumsum([-(z ** n) / n for n in range(1, N + 1)]); S = np.concatenate([[0], S])
    ax.plot(S.real, S.imag, 'o-', ms=3, color=C1, lw=.8, label='partial sums')
    t = np.log(1 - z); ax.plot(t.real, t.imag, '*', ms=12, color=C2, label='log(1 − i/2)')
    for k in (1, 2, 3):
        ax.annotate(str(k), (S[k].real, S[k].imag), fontsize=8, xytext=(4, -10), textcoords='offset points')
    ax.axhline(0, color=GR, lw=.6); ax.axvline(0, color=GR, lw=.6)
    ax.set_xlim(-.03, .16); ax.set_ylim(-.55, .05); ax.set_xlabel('Re'); ax.set_ylabel('Im'); ax.legend(fontsize=8, loc='upper right')
    save('T09-e2')


@fig('T09-e3')
def _():
    fig_, ax = plt.subplots(figsize=(6.2, 3.2)); th = np.linspace(0, 2 * np.pi, 200)
    for c, col, lab in ((0, C1, '|z| = 1: 2πi'), (2, C2, '|z − 2| = 1: 0')):
        ax.plot(c + np.cos(th), np.sin(th), color=col, label=lab)
        ax.annotate('', xy=(c + np.cos(1.7), np.sin(1.7)), xytext=(c + np.cos(1.4), np.sin(1.4)), arrowprops=dict(arrowstyle='->', color=col, lw=1.5))
    ax.plot(0, 0, 'kx', ms=8); ax.annotate('pole of 1/z', (0, 0), xytext=(-0.5, -0.3), fontsize=8)
    ax.axhline(0, color=GR, lw=.6); ax.axvline(0, color=GR, lw=.6); ax.set_aspect('equal'); ax.legend(fontsize=8, loc='upper right')
    ax.set_xlim(-1.5, 3.8); ax.set_ylim(-1.4, 1.4)
    save('T09-e3')


@fig('T09-e4')
def _():
    fig_, ax = plt.subplots(figsize=(4.8, 4.4)); s = 2 + 1j; n = np.arange(1, 201)
    S = np.cumsum(n.astype(complex) ** (-s))
    th = np.linspace(0, 2 * np.pi, 300); R = np.pi ** 2 / 6
    ax.plot(R * np.cos(th), R * np.sin(th), color=GR, ls=':', label='|z| = ζ(2)')
    ax.plot(S.real, S.imag, 'o-', ms=2, lw=.6, color=C1, label='partial sums')
    ax.plot(1.15036, -0.43753, '*', ms=12, color=C2, label='ζ(2 + i)')
    ax.axhline(0, color=GR, lw=.6); ax.axvline(0, color=GR, lw=.6); ax.set_aspect('equal'); ax.legend(fontsize=8, loc='upper left')
    save('T09-e4')


@fig('T09-x1')
def _():
    fig_, ax = plt.subplots(figsize=(4.6, 4.4)); _unit(ax, 1.3)
    for th, col in zip(np.linspace(0, np.pi, 7)[:-1], plt.cm.viridis(np.linspace(0, .9, 6))):
        q = np.exp(-2j * th)
        ax.plot(q.real, q.imag, 'o', color=col, ms=8, label=f'θ = {th / np.pi:.2f}π')
    ax.legend(fontsize=7, loc='lower left'); ax.set_title('(f(z+h) − f(z))/h for f = z̄, h = re^(iθ)', fontsize=9)
    save('T09-x1')


@fig('T09-x2')
def _():
    ax = plt.gca(); n = np.arange(1, 41); z = 0.9
    from math import lgamma
    ax.semilogy(n, (2 * z) ** n, color=C1, label='(a) |2^n z^n|')
    ax.semilogy(n, z ** n / n ** 2, color=C3, label='(b) |z^n / n²|')
    ax.semilogy(n, np.exp(np.array([lgamma(k + 1) for k in n]) + n * np.log(z)), color=C2, label='(c) |n! z^n|')
    ax.set_xlabel('n'); ax.legend(fontsize=8); ax.set_title('size of the n-th term at z = 0.9', fontsize=9)
    save('T09-x2')


@fig('T09-x3')
def _():
    fig_, ax = plt.subplots(figsize=(4.2, 4)); 
    ax.annotate('', xy=(1, 1), xytext=(0, 0), arrowprops=dict(arrowstyle='->', color=C1, lw=2))
    ax.annotate('', xy=(1, 0), xytext=(0, 0), arrowprops=dict(arrowstyle='->', color=C2, lw=2))
    ax.annotate('', xy=(1, 1), xytext=(1, 0), arrowprops=dict(arrowstyle='->', color=C2, lw=2))
    ax.text(.3, .5, '(a)', color=C1); ax.text(1.05, .45, '(b)', color=C2)
    ax.plot([0, 1, 1], [0, 0, 1], 'ko', ms=4); ax.text(-.12, -.12, '0'); ax.text(1.02, -.12, '1'); ax.text(1.02, 1.05, '1+i')
    ax.set_xlim(-.3, 1.4); ax.set_ylim(-.3, 1.3); ax.set_aspect('equal'); ax.set_title('∫ z² dz = (−2 + 2i)/3 on both', fontsize=9)
    save('T09-x3')


@fig('T09-x4')
def _():
    fig_, (a1, a2) = plt.subplots(1, 2, figsize=(6.6, 3.2)); th = np.linspace(0, 2 * np.pi, 200)
    for R, col in ((1.5, C3), (2, C1), (3, C4)):
        a1.plot(R * np.cos(th), R * np.sin(th), color=col, label=f'R = {R}')
    a1.plot([0, 0], [1, -1], 'kx', ms=8); a1.text(.15, 1, 'i'); a1.text(.15, -1.1, '−i')
    a1.set_aspect('equal'); a1.legend(fontsize=7, loc='upper left', bbox_to_anchor=(1.0, 1.0)); a1.set_title('poles ±i inside', fontsize=9)
    R = np.linspace(1.2, 20, 200); a2.plot(R, 2 * np.pi * R / (R ** 2 - 1), color=C2, label='ML bound')
    a2.axhline(0, color=C1, label='actual value 0'); a2.set_xlabel('R'); a2.legend(fontsize=8); a2.set_ylim(-.5, 8)
    save('T09-x4')


@fig('T10-e1')
def _():
    fig_, ax = plt.subplots(figsize=(4.8, 4.4)); th = np.linspace(0, 2 * np.pi, 200)
    ax.plot(.6 * np.cos(th), .6 * np.sin(th), color=C3, label='R = 0.6: integral 0')
    ax.plot(1.7 * np.cos(th), 1.7 * np.sin(th), color=C1, label='R = 1.7: 2πi(−i/2 + i/2) = 0')
    ax.plot([0, 0], [1, -1], 'x', color=C2, ms=10, mew=2)
    ax.text(.12, 1.05, 'Res = −i/2', fontsize=9, color=C2); ax.text(.12, -1.2, 'Res = i/2', fontsize=9, color=C2)
    ax.axhline(0, color=GR, lw=.5); ax.axvline(0, color=GR, lw=.5); ax.set_aspect('equal'); ax.set_xlim(-2.2, 2.2); ax.set_ylim(-2.2, 2.4)
    ax.legend(fontsize=8, loc='upper left'); ax.set_title('1/(z² + 1)', fontsize=9)
    save('T10-e1')


@fig('T10-e2')
def _():
    fig_, ax = plt.subplots(figsize=(5.6, 3.2)); R = 2.5; th = np.linspace(0, np.pi, 200)
    ax.plot([-R, R], [0, 0], color=C1, lw=2, label='[−R, R]: → ∫ dx/(1+x²)')
    ax.plot(R * np.cos(th), R * np.sin(th), color=C4, lw=2, label='C_R: ≤ πR/(R²−1) → 0')
    ax.annotate('', xy=(R * np.cos(1.3), R * np.sin(1.3)), xytext=(R * np.cos(1.1), R * np.sin(1.1)), arrowprops=dict(arrowstyle='->', color=C4, lw=1.5))
    ax.annotate('', xy=(.6, 0), xytext=(0, 0), arrowprops=dict(arrowstyle='->', color=C1, lw=1.5))
    ax.plot([0, 0], [1, -1], 'x', color=C2, ms=10, mew=2); ax.text(.12, 1.05, 'i (inside)', fontsize=9); ax.text(.12, -1.2, '−i (outside)', fontsize=9)
    ax.set_aspect('equal'); ax.set_xlim(-3, 3); ax.set_ylim(-1.6, 2.9); ax.legend(fontsize=7, loc='upper right')
    save('T10-e2')


@fig('T10-e3')
def _():
    ax = plt.gca(); import mpmath as mpm
    Ts = np.linspace(2, 80, 70)
    def I(y, T):
        return float(mpm.re(mpm.quad(lambda t: mpm.power(y, 1 + 1j * t) / (1 + 1j * t), mpm.linspace(-T, T, int(T) + 1)) / (2 * mpm.pi)))
    ax.plot(Ts, [I(2, T) for T in Ts], color=C1, label='y = 2')
    ax.plot(Ts, [I(.5, T) for T in Ts], color=C2, label='y = ½')
    ax.axhline(1, color=C1, ls=':', lw=.8); ax.axhline(0, color=C2, ls=':', lw=.8)
    ax.set_xlabel('T'); ax.legend(fontsize=8); ax.set_title('(1/2πi) ∫ from 1−iT to 1+iT of y^s/s ds', fontsize=9)
    save('T10-e3')


@fig('T10-e4')
def _():
    fig_, (a1, a2) = plt.subplots(1, 2, figsize=(6.6, 3.3)); th = np.linspace(0, 2 * np.pi, 400); z = np.exp(1j * th)
    r = np.roots([1, 0, 1, 1]); _unit(a1, 1.5)
    a1.plot(r.real, r.imag, 'o', color=C2); a1.set_title('roots of z³ + z + 1', fontsize=9)
    w = z ** 3 + z + 1
    a2.plot(w.real, w.imag, color=C1); a2.plot(0, 0, 'k+', ms=10)
    a2.annotate('', xy=(w[60].real, w[60].imag), xytext=(w[50].real, w[50].imag), arrowprops=dict(arrowstyle='->', color=C1, lw=1.5))
    a2.set_aspect('equal'); a2.set_title('image of |z| = 1: winds once around 0', fontsize=9)
    save('T10-e4')


@fig('T10-x1')
def _():
    fig_, ax = plt.subplots(figsize=(5, 4.4)); N = 3; h = N + .5
    ax.plot([-h, h, h, -h, -h], [-h, -h, h, h, -h], color=C1, label='square, side 2N+1 (N = 3)')
    n = np.arange(-4, 5); ax.plot(n[n != 0], 0 * n[n != 0], 'x', color=C2, ms=8, mew=2, label='Res = 1/n²')
    ax.plot(0, 0, 'x', color=C4, ms=10, mew=2, label='Res = −π²/3')
    ax.set_aspect('equal'); ax.set_xlim(-4.6, 4.6); ax.set_ylim(-4.2, 5.2); ax.legend(fontsize=8, loc='upper center', ncol=2)
    ax.set_title('π cot(πz) / z²', fontsize=9)
    save('T10-x1')


@fig('T10-x2')
def _():
    fig_, ax = plt.subplots(figsize=(4.8, 4.4)); th = np.linspace(0, 2 * np.pi, 200)
    ax.plot(.5 * np.cos(th), .5 * np.sin(th), color=C1, label='|z| = ½: 2πi')
    ax.plot(2 * np.cos(th), 2 * np.sin(th), color=C3, label='|z| = 2: 0')
    ax.plot([0, 1], [0, 0], 'x', color=C2, ms=10, mew=2); ax.text(-.15, -.3, 'Res 1', fontsize=8); ax.text(.9, -.3, 'Res −1', fontsize=8)
    ax.axhline(0, color=GR, lw=.5); ax.axvline(0, color=GR, lw=.5); ax.set_aspect('equal'); ax.set_xlim(-2.4, 2.4); ax.set_ylim(-2.4, 2.8)
    ax.legend(fontsize=8, loc='upper left'); ax.set_title('1/(z(1 − z))', fontsize=9)
    save('T10-x2')


@fig('T10-x3')
def _():
    ax = plt.gca(); x = np.linspace(.02, 1, 20000)
    ax.plot(x, np.sin(np.pi / x), color=C1, lw=.6)
    n = np.arange(1, 50); ax.plot(1 / n, 0 * n, '.', color=C2, ms=4, label='zeros 1/n')
    ax.set_xlabel('x'); ax.legend(fontsize=8); ax.set_title('sin(π/x)', fontsize=9)
    save('T10-x3')


@fig('T10-x4')
def _():
    ax = plt.gca(); T = np.linspace(0, 100, 400)
    ax.plot(T, np.arctan(T) / np.pi, color=C1); ax.axhline(.5, color=C2, ls='--', label='½')
    ax.plot([1, 10, 100], np.arctan([1, 10, 100]) / np.pi, 'o', color=C1, ms=4)
    ax.set_xlabel('T'); ax.legend(fontsize=8); ax.set_title('(1/2πi) ∫ ds/s on [1 − iT, 1 + iT] = arctan(T)/π', fontsize=9)
    save('T10-x4')


@fig('T11-e1')
def _():
    ax = plt.gca(); from scipy.special import gamma as G
    for a, b in ((-3.98, -3.02), (-2.98, -2.02), (-1.98, -1.02), (-.98, -.02), (.02, 5.2)):
        x = np.linspace(a, b, 400); ax.plot(x, G(x), color=C1)
    n = np.arange(1, 6); ax.plot(n, G(n), 'o', color=C2, label='Γ(n) = (n−1)!')
    ax.plot(.5, np.sqrt(np.pi), 's', color=C3, label='Γ(½) = √π')
    for k in range(0, 4):
        ax.axvline(-k, color=GR, ls=':', lw=.8)
    ax.set_ylim(-8, 26); ax.axhline(0, color=GR, lw=.5); ax.set_xlabel('x'); ax.legend(fontsize=8); ax.set_title('Γ(x)', fontsize=9)
    save('T11-e1')


@fig('T11-e2')
def _():
    ax = plt.gca(); x = np.linspace(-2, 2, 400); f = np.exp(-np.pi * x ** 2)
    ax.fill_between(x, f, where=np.abs(x) <= 1, color=C1, alpha=.15, label='|x| ≤ 1: 0.988')
    ax.fill_between(x, f, where=np.abs(x) <= .5, color=C1, alpha=.35, label='|x| ≤ ½: 0.790')
    ax.plot(x, f, color=C1, lw=2, label='e^(−πx²)')
    xi = np.linspace(-2, 2, 25); fh = [np.trapezoid(f * np.cos(2 * np.pi * x * t), x) for t in xi]
    ax.plot(xi, fh, 'o', color=C2, ms=4, label='its Fourier transform (numerical)')
    ax.set_xlabel('x, ξ'); ax.legend(fontsize=7); ax.set_title('the Gaussian is its own Fourier transform', fontsize=9)
    save('T11-e2')


@fig('T11-e3')
def _():
    ax = plt.gca(); n = np.arange(-40, 41)
    th = lambda x: np.exp(-np.pi * np.outer(x, n ** 2)).sum(axis=1)
    x = np.linspace(.05, 3, 300); ax.plot(x, th(x), color=C1, label='ϑ(x)')
    xs = np.linspace(.05, 3, 30); ax.plot(xs, th(1 / xs) / np.sqrt(xs), 'o', ms=4, color=C2, label='x^(−½) ϑ(1/x)')
    ax.plot(x, 1 / np.sqrt(x), ':', color=GR, label='1/√x')
    ax.set_ylim(0, 5); ax.set_xlabel('x'); ax.legend(fontsize=8); ax.set_title('ϑ(1/x) = √x ϑ(x)', fontsize=9)
    save('T11-e3')


@fig('T11-e4')
def _():
    ax = plt.gca(); import mpmath as mpm
    xi = lambda s: float(mpm.pi ** (-s / 2) * mpm.gamma(s / 2) * mpm.zeta(s))
    for a, b in ((-1.5, -.04), (.04, .96), (1.04, 2.5)):
        x = np.linspace(a, b, 120); ax.plot(x, [xi(t) for t in x], color=C1)
    ax.axvline(.5, color=C2, ls='--', lw=.8, label='σ = ½'); ax.axvline(0, color=GR, ls=':'); ax.axvline(1, color=GR, ls=':')
    ax.set_ylim(-12, 12); ax.axhline(0, color=GR, lw=.5); ax.set_xlabel('σ'); ax.legend(fontsize=8); ax.set_title('ξ(σ) = ξ(1 − σ)', fontsize=9)
    save('T11-e4')


@fig('T11-x1')
def _():
    ax = plt.gca(); from scipy.special import rgamma
    x = np.linspace(-4.5, 5, 600); ax.plot(x, rgamma(x), color=C1, label='1/Γ(x)')
    ax.plot(-np.arange(0, 5), 0 * np.arange(5), 'o', color=C2, label='zeros 0, −1, −2, …')
    ax.axhline(0, color=GR, lw=.5); ax.set_ylim(-3, 3); ax.set_xlabel('x'); ax.legend(fontsize=8); ax.set_title('1/Γ is entire', fontsize=9)
    save('T11-x1')


@fig('T11-x2')
def _():
    ax = plt.gca(); N = np.arange(0, 101); n = np.arange(-100, 101)
    S = [np.sum(1 / (1 + n[np.abs(n) <= k] ** 2)) for k in N]
    ax.plot(N, S, color=C1, label='Σ_{|n|≤N} 1/(1 + n²)')
    ax.axhline(np.pi / np.tanh(np.pi), color=C2, ls='--', label='π coth π ≈ 3.1533')
    ax.axhline(np.pi, color=C3, ls=':', label='k = 0 term alone: π')
    ax.set_xlabel('N'); ax.legend(fontsize=8); ax.set_ylim(.9, 3.3); ax.set_title('Poisson: Σ f(n) = Σ f̂(k)', fontsize=9)
    save('T11-x2')


@fig('T11-x3')
def _():
    ax = plt.gca(); x = np.linspace(1e-6, 15, 400); y = x / np.expm1(x)
    ax.fill_between(x, y, color=C1, alpha=.25); ax.plot(x, y, color=C1, label='x/(e^x − 1)')
    ax.set_xlabel('x'); ax.legend(fontsize=8); ax.set_title('area = Γ(2)ζ(2) = π²/6', fontsize=9)
    save('T11-x3')


@fig('T11-x4')
def _():
    ax = plt.gca(); import mpmath as mpm
    x = np.linspace(-4, .8, 300); ax.plot(x, [float(mpm.zeta(t)) for t in x], color=C1, label='ζ(σ)')
    ax.plot(-1, -1 / 12, 'o', color=C2, label='ζ(−1) = −1/12'); ax.plot([-2, -4], [0, 0], 's', color=C3, label='trivial zeros')
    ax.plot(0, -.5, 'o', color=C4, label='ζ(0) = −½')
    ax.axhline(0, color=GR, lw=.5); ax.set_ylim(-4, 1); ax.set_xlabel('σ'); ax.legend(fontsize=8); ax.set_title('analytic continuation of ζ', fontsize=9)
    save('T11-x4')


@fig('T12-e1')
def _():
    ax = plt.gca(); th = np.linspace(0, 2 * np.pi, 600); z = np.exp(1j * th)
    L = np.log(np.abs((z - .5) * (z - 3)))
    ax.plot(th, L, color=C1, label='log |f(e^(iθ))|'); ax.axhline(np.log(3), color=C2, ls='--', label='mean = log 3 = 1.099')
    ax.axhline(np.log(1.5), color=C3, ls=':', label='log |f(0)| = 0.405')
    ax.set_xlabel('θ'); ax.legend(fontsize=8); ax.set_title('Jensen: 0.405 = 1.099 − log 2', fontsize=9)
    save('T12-e1')


@fig('T12-e2')
def _():
    ax = plt.gca(); R = np.logspace(.5, 8, 300)
    ax.semilogx(R, np.log(R ** 2) / np.log(R), color=C2, label='e^(z²): 2')
    ax.semilogx(R, np.log(np.sqrt(R) + np.log1p(np.exp(-2 * np.sqrt(R))) - np.log(2)) / np.log(R), color=C1, label='cos √z → ½')
    ax.semilogx(R, np.log(np.log(R ** 5 + 1)) / np.log(R), color=C3, label='z⁵ + 1 → 0')
    ax.set_xlabel('R'); ax.set_ylabel('log log M(R) / log R'); ax.legend(fontsize=8); ax.set_title('order of growth', fontsize=9)
    save('T12-e2')


@fig('T12-e3')
def _():
    ax = plt.gca(); x = np.linspace(-3.5, 3.5, 500)
    ax.plot(x, np.sin(np.pi * x), color='k', lw=2, label='sin πx')
    for N, col in ((1, C4), (3, C3), (10, C2)):
        P = np.pi * x * np.prod([1 - x ** 2 / n ** 2 for n in range(1, N + 1)], axis=0)
        ax.plot(x, P, color=col, ls='--', label=f'N = {N}')
    ax.set_ylim(-2.5, 2.5); ax.axhline(0, color=GR, lw=.5); ax.legend(fontsize=8); ax.set_xlabel('x'); ax.set_title('πx ∏_{n≤N} (1 − x²/n²)', fontsize=9)
    save('T12-e3')


@fig('T12-e4')
def _():
    import mpmath as mpm
    g = np.array([float(mpm.zetazero(k).imag) for k in range(1, 101)])
    fig_, (a1, a2) = plt.subplots(1, 2, figsize=(6.6, 3.2))
    a1.plot(g, np.cumsum(1 / g), 'o-', ms=2, color=C1, label='Σ 1/γ')
    T = np.linspace(14, 240, 200); a1.plot(T, np.log(T / (2 * np.pi)) ** 2 / (4 * np.pi), color=C2, ls='--', label='(1/4π) log²(T/2π)')
    a1.set_xlabel('T'); a1.legend(fontsize=7); a1.set_title('diverges', fontsize=9)
    a2.plot(g, np.cumsum(1 / g ** 2), 'o-', ms=2, color=C1, label='Σ 1/γ²'); a2.axhline(.0231, color=C2, ls='--', label='limit ≈ 0.0231')
    a2.set_xlabel('T'); a2.legend(fontsize=7); a2.set_title('converges', fontsize=9)
    save('T12-e4')


@fig('T12-x1')
def _():
    ax = plt.gca(); R = np.linspace(1, 50, 300)
    ax.plot(R, 1 / R, color=C1, label='Cauchy bound for |a₃|: C·R²/R³ (C = 1)')
    ax.set_xlabel('R'); ax.legend(fontsize=8); ax.set_ylim(0, 1.05); ax.set_title('the bound → 0, so a₃ = 0', fontsize=9)
    save('T12-x1')


@fig('T12-x2')
def _():
    fig_, ax = plt.subplots(figsize=(4.6, 4.6)); k = np.arange(-4, 5)
    ax.plot(np.log(2) + 0 * k, 2 * np.pi * k, 'x', color=C2, ms=8, mew=2, label='zeros log 2 + 2πik')
    th = np.linspace(0, 2 * np.pi, 300)
    for r, col in ((7, C1), (20, C3)):
        ax.plot(r * np.cos(th), r * np.sin(th), color=col, label=f'r = {r}: {int(np.sum(np.abs(np.log(2) + 2j * np.pi * np.arange(-10, 11)) <= r))} zeros')
    ax.set_aspect('equal'); ax.legend(fontsize=7, loc='upper left'); ax.set_xlim(-22, 22); ax.set_ylim(-22, 27)
    save('T12-x2')


@fig('T12-x3')
def _():
    ax = plt.gca(); N = np.arange(1, 101); z = 1 / 3
    P = np.cumprod(1 - 4 * z ** 2 / (2 * N - 1) ** 2)
    ax.plot(N, P, 'o-', ms=2, color=C1, label='partial products at z = ⅓'); ax.axhline(.5, color=C2, ls='--', label='cos(π/3) = ½')
    ax.set_xscale('log'); ax.set_xlabel('N'); ax.legend(fontsize=8); ax.set_title('cos πz = ∏ (1 − 4z²/(2n − 1)²)', fontsize=9)
    save('T12-x3')


@fig('T12-x4')
def _():
    ax = plt.gca(); x = np.linspace(-2.9, 2.9, 3000); x = x[np.min(np.abs(x[:, None] - np.arange(-3, 4)), axis=1) > .03]
    S = 1 / x + sum(2 * x / (x ** 2 - n ** 2) for n in range(1, 21))
    ax.plot(x, np.pi / np.tan(np.pi * x), '.', ms=1, color=C1, label='π cot πx')
    ax.plot(x, S, '.', ms=.6, color=C2, label='1/x + Σ_{n≤20} 2x/(x² − n²)')
    ax.set_ylim(-10, 10); ax.axhline(0, color=GR, lw=.5); ax.set_xlabel('x'); ax.legend(fontsize=8, markerscale=8)
    save('T12-x4')


def _periodic_flow(g0, ts):
    from scipy.integrate import solve_ivp
    g0 = np.array(g0); L = g0.sum(); x0 = np.concatenate([[0], np.cumsum(g0)[:-1]])
    def f(t, x):
        d = x[:, None] - x[None, :]; np.fill_diagonal(d, 1.0)
        c = 1 / np.tan(np.pi * d / L); np.fill_diagonal(c, 0)
        return (2 * np.pi / L) * c.sum(1)
    sol = solve_ivp(f, [0, ts[-1]], x0, t_eval=ts, rtol=1e-10, atol=1e-12)
    return sol.t, sol.y, L


@fig('T13-e1')
def _():
    ax = plt.gca(); from scipy.special import erf
    x = np.linspace(-4, 4, 400)
    ax.plot(x, (x > 0).astype(float), color='k', lw=1, label='t = 0')
    for t, col in ((.01, C1), (.1, C3), (1, C2)):
        ax.plot(x, .5 * (1 + erf(x / (2 * np.sqrt(t)))), color=col, label=f't = {t}')
    ax.set_xlabel('x'); ax.legend(fontsize=8); ax.set_title('heat flow smooths a step', fontsize=9)
    save('T13-e1')


@fig('T13-e2')
def _():
    fig_, ax = plt.subplots(figsize=(4.8, 4.2)); t = np.linspace(0, .5, 100); t2 = np.linspace(.5, 1.5, 100)
    ax.plot(0 * t, np.sqrt(1 - 2 * t), color=C1, lw=2); ax.plot(0 * t, -np.sqrt(1 - 2 * t), color=C1, lw=2, label='t < ½: ±i√(1 − 2t)')
    ax.plot(np.sqrt(2 * t2 - 1), 0 * t2, color=C2, lw=2); ax.plot(-np.sqrt(2 * t2 - 1), 0 * t2, color=C2, lw=2, label='t > ½: ±√(2t − 1)')
    ax.plot([0, 0], [1, -1], 'o', color=C1); ax.plot(0, 0, 'k*', ms=10, label='collision at t = ½')
    ax.annotate('', xy=(0, .5), xytext=(0, .85), arrowprops=dict(arrowstyle='->', color=C1, lw=1.5))
    ax.annotate('', xy=(1.2, 0), xytext=(.8, 0), arrowprops=dict(arrowstyle='->', color=C2, lw=1.5))
    ax.set_aspect('equal'); ax.set_xlim(-1.6, 1.6); ax.set_ylim(-1.3, 1.5); ax.legend(fontsize=7, loc='upper right')
    ax.set_xlabel('Re z'); ax.set_ylabel('Im z'); ax.set_title('zeros of z² + 1 − 2t', fontsize=9)
    save('T13-e2')


@fig('T13-e3')
def _():
    ax = plt.gca(); t = np.linspace(-.5, 1.5, 300)
    ax.plot(t, np.sqrt(3 + 6 * t), color=C1, label='√(3 + 6t)'); ax.plot(t, -np.sqrt(3 + 6 * t), color=C1)
    ax.plot(t, 0 * t, color=C2, label='0 (stays)')
    ax.set_xlabel('t'); ax.set_ylabel('zero'); ax.legend(fontsize=8); ax.set_title('zeros of z³ − (3 + 6t)z', fontsize=9)
    save('T13-e3')


@fig('T13-e4')
def _():
    ts = np.linspace(0, .3, 151); t, X, L = _periodic_flow([.4, 1.6, .7, 1.3, .5, 1.5, 1., 1.], ts)
    fig_, (a1, a2) = plt.subplots(1, 2, figsize=(6.6, 3.3))
    for k in range(X.shape[0]):
        a1.plot(X[k], t, color=C1, lw=1)
    a1.set_xlabel('position (period 8)'); a1.set_ylabel('t'); a1.set_title('zero trajectories', fontsize=9)
    G = np.diff(np.vstack([X, X[:1] + L]), axis=0)
    a2.plot(t, G.std(axis=0), color=C2); a2.set_xlabel('t'); a2.set_title('std of gaps → 0', fontsize=9)
    save('T13-e4')


@fig('T13-x1')
def _():
    ax = plt.gca(); x = np.linspace(-5, 5, 400)
    for t, col in ((.05, C1), (.25, C3), (1, C2)):
        ax.plot(x, np.exp(-x ** 2 / (4 * t)) / np.sqrt(4 * np.pi * t), color=col, label=f't = {t}')
    ax.set_xlabel('x'); ax.legend(fontsize=8); ax.set_title('heat kernel K_t(x), area 1', fontsize=9)
    save('T13-x1')


@fig('T13-x2')
def _():
    fig_, (a1, a2) = plt.subplots(1, 2, figsize=(6.6, 3.2)); u = np.linspace(0, 1.2, 300)
    n = np.arange(1, 6)[:, None]
    P = ((2 * np.pi ** 2 * n ** 4 * np.exp(9 * u) - 3 * np.pi * n ** 2 * np.exp(5 * u)) * np.exp(-np.pi * n ** 2 * np.exp(4 * u))).sum(0)
    a1.plot(u[u <= .6], P[u <= .6], color=C1); a1.set_xlabel('u'); a1.set_title('Φ(u)', fontsize=9)
    lp = np.log(2 * np.pi ** 2) + 9 * u - np.pi * np.exp(4 * u)
    a2.plot(u, lp, color=C1, label='log Φ(u) ≈ log 2π² + 9u − πe^(4u)'); a2.plot(u, -np.pi * np.exp(4 * u), color=C2, ls='--', label='−π e^(4u)')
    a2.set_xlabel('u'); a2.legend(fontsize=7); a2.set_title('super-exponential decay', fontsize=9)
    save('T13-x2')


@fig('T13-x3')
def _():
    fig_, ax = plt.subplots(figsize=(4.8, 4.2)); t = np.linspace(0, .5, 100); t2 = np.linspace(.5, 1.5, 100)
    ax.plot(np.sqrt(1 - 2 * t), 0 * t, color=C1, lw=2); ax.plot(-np.sqrt(1 - 2 * t), 0 * t, color=C1, lw=2, label='t < ½: ±√(1 − 2t)')
    ax.plot(0 * t2, np.sqrt(2 * t2 - 1), color=C2, lw=2); ax.plot(0 * t2, -np.sqrt(2 * t2 - 1), color=C2, lw=2, label='t > ½: ±i√(2t − 1)')
    ax.plot([1, -1], [0, 0], 'o', color=C1); ax.plot(0, 0, 'k*', ms=10)
    ax.set_aspect('equal'); ax.set_xlim(-1.5, 1.5); ax.set_ylim(-1.5, 1.6); ax.legend(fontsize=7, loc='upper right')
    ax.set_xlabel('Re z'); ax.set_ylabel('Im z'); ax.set_title('forward heat flow: z² − 1 + 2t', fontsize=9)
    save('T13-x3')


@fig('T13-x4')
def _():
    ax = plt.gca()
    for d0, col in ((.1, C1), (.2, C3), (.4, C2)):
        t = np.linspace(-d0 ** 2 / 8, .02, 300); ax.plot(t, np.sqrt(np.maximum(d0 ** 2 + 8 * t, 0)), color=col, label=f'δ₀ = {d0}: collide at t = {-d0 ** 2 / 8:.5f}')
    ax.axvline(0, color=GR, lw=.6); ax.set_xlabel('t'); ax.set_ylabel('δ(t)'); ax.legend(fontsize=7); ax.set_title('a close pair, backwards in time', fontsize=9)
    save('T13-x4')


def _H0(x):
    import mpmath as mpm
    s = mpm.mpf(.5) + 1j * mpm.mpf(x) / 2
    return float(mpm.re(s * (s - 1) / 2 * mpm.pi ** (-s / 2) * mpm.gamma(s / 2) * mpm.zeta(s))) / 8


def _zz():
    return np.load(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'zeta_zeros_1000.npy'))


@fig('18-1')
def _():
    ax = plt.gca(); x = np.linspace(0, 70, 700)
    y = np.array([_H0(t) for t in x]) * np.exp(np.pi * x / 8)
    ax.plot(x, y, color=C1); ax.axhline(0, color=GR, lw=.6)
    z = 2 * _zz()[:5]; ax.plot(z, 0 * z, 'o', color=C2, ms=5, label='2γ (zeta zeros)')
    ax.set_xlabel('x'); ax.legend(fontsize=8); ax.set_title('H₀(x)·e^(πx/8)', fontsize=9)
    save('18-1')


@fig('18-2')
def _():
    ax = plt.gca(); t = np.array([-.4, -.2, 0, .2, .4])
    X = np.array([[28.5017, 42.3473, 50.2555], [28.3855, 42.1954, 50.1387], [28.2695, 42.0441, 50.0217], [28.1536, 41.8934, 49.9044], [28.038, 41.7433, 49.7868]])
    for k, col in zip(range(3), (C1, C3, C2)):
        ax.plot(X[:, k], t, 'o-', color=col, label=f'x_{k + 1}(t)')
    ax.set_xlabel('x'); ax.set_ylabel('t'); ax.legend(fontsize=8); ax.set_title('first zeros of H_t', fontsize=9)
    save('18-2')


@fig('18-3')
def _():
    ax = plt.gca(); g = 2 * _zz(); T = np.linspace(20, g[-1], 400)
    ax.step(g, np.arange(1, len(g) + 1), where='post', color=C1, label='N₀(T): zeros of H₀ in [0, T]')
    ax.plot(T, T / (4 * np.pi) * np.log(T / (4 * np.pi)) - T / (4 * np.pi), color=C2, ls='--', label='(T/4π) log(T/4π) − T/4π')
    ax.set_xlabel('T'); ax.legend(fontsize=8); ax.set_title('counting zeros', fontsize=9)
    save('18-3')


@fig('18-4')
def _():
    ax = plt.gca(); g = _zz(); gaps = np.diff(g) * np.log(g[:-1] / (2 * np.pi)) / (2 * np.pi)
    ax.hist(gaps, bins=40, density=True, color=C1, alpha=.8, label='normalized gaps of ζ zeros')
    ax.axvline(1, color=C2, lw=2, label='arithmetic progression: all gaps = 1')
    s = np.linspace(0, 3, 300); ax.plot(s, 32 / np.pi ** 2 * s ** 2 * np.exp(-4 * s ** 2 / np.pi), color='k', ls=':', label='GUE (Wigner surmise)')
    ax.set_xlabel('normalized gap'); ax.legend(fontsize=7); ax.set_title('zeta zeros are not in equilibrium', fontsize=9)
    save('18-4')


@fig('18-5')
def _():
    ax = plt.gca(); x = np.linspace(-70, 70, 1001)
    y = np.array([_H0(abs(t)) for t in x]) * np.exp(np.pi * np.abs(x) / 8)
    ax.plot(x, y, color=C1); ax.axhline(0, color=GR, lw=.6); ax.axvline(0, color=GR, lw=.6)
    z = 2 * _zz()[:5]; ax.plot(np.concatenate([z, -z]), 0 * np.concatenate([z, z]), 'o', color=C2, ms=4)
    ax.set_xlabel('x'); ax.set_title('H₀ is even: zeros at ±2γ', fontsize=9)
    save('18-5')


@fig('18-6')
def _():
    fig_, ax = plt.subplots(figsize=(6.6, 3.2))
    yrs = [1988, 1991, 1991, 1992, 1993, 1994, 2000, 2011]; lb = [-50, -5, -.0991, -.385, -5.895e-9, -4.379e-6, -2.63e-9, -1.15e-11]
    ax.semilogy(yrs, -np.array(lb), 'o', color=C1, label='|lower bound| (Lehmer pairs)')
    ax.semilogy([1950, 2019, 2021], [.5, .22, .2], 's', color=C2, label='upper bounds: ½, 0.22, 0.2')
    ax.axvline(2018, color=C3, ls='--', label='2018: Λ ≥ 0 (Rodgers–Tao)')
    ax.set_xlabel('year'); ax.legend(fontsize=7, loc='lower left'); ax.set_title('bounds on Λ', fontsize=9)
    save('18-6')


@fig('18-7')
def _():
    fig_, ax = plt.subplots(figsize=(6.6, 3.0)); ax.axis('off'); ax.set_xlim(0, 10); ax.set_ylim(0, 4.4)
    box = dict(boxstyle='round,pad=0.35', fc='#eef3fb', ec=C1)
    def B(x, y, t, ec=C1):
        ax.text(x, y, t, ha='center', va='center', fontsize=8, bbox=dict(boxstyle='round,pad=0.35', fc='white', ec=ec))
    B(1.1, 2.2, 'assume\nΛ < 0', C2)
    B(3.6, 3.5, 'RH holds\n(t = 0)'); B(6.4, 3.5, 'Montgomery\n(assumes RH)'); B(8.9, 3.5, 'many small\ngaps')
    B(3.6, .9, 'real zeros\nfor Λ < t ≤ 0'); B(6.4, .9, 'flow + energy\n→ equilibrium'); B(8.9, .9, 'gaps ≈ average\n(no small gaps)')
    B(8.9, 2.2, 'CONTRADICTION', C2)
    for (a, b), (c, d) in [((1.7, 2.5), (2.9, 3.4)), ((1.7, 1.9), (2.9, 1.0)), ((4.3, 3.5), (5.6, 3.5)), ((7.2, 3.5), (8.1, 3.5)),
                           ((4.3, .9), (5.5, .9)), ((7.3, .9), (8.0, .9)), ((8.9, 3.0), (8.9, 2.5)), ((8.9, 1.4), (8.9, 1.9))]:
        ax.annotate('', xy=(c, d), xytext=(a, b), arrowprops=dict(arrowstyle='->', color=GR, lw=1.3))
    save('18-7')


@fig('18-8')
def _():
    fig_, ax = plt.subplots(figsize=(5.4, 3.8)); p0 = np.poly1d(np.poly([1, -1, 3, 3.1]))
    ts = np.linspace(-.003, .002, 300); P = []
    for t in ts:
        r = np.roots((p0 - t * p0.deriv(2) + t * t / 2 * p0.deriv(4)).coeffs); P.append(r[r.real > 2])
    P = np.array(P)
    sc = ax.scatter(P.real.ravel(), P.imag.ravel(), c=np.repeat(ts, 2), cmap='coolwarm', s=6)
    plt.colorbar(sc, ax=ax, label='t')
    ax.plot([3, 3.1], [0, 0], 'ko', ms=5); ax.text(3.0, .004, 't = 0', fontsize=8)
    ax.axhline(0, color=GR, lw=.6); ax.set_xlabel('Re z'); ax.set_ylabel('Im z')
    ax.set_title('the pair 3, 3.1 collides at t ≈ −0.00125 and leaves the real axis', fontsize=9)
    save('18-8')


# ---------- tools lesson T14: rings, ideals, field extensions ----------
def _lattice(ax, R=4, d=-1, color=GR, s=10):
    import itertools
    pts = [(a, b) for a in range(-R, R + 1) for b in range(-R, R + 1)]
    sq = math.sqrt(abs(d))
    ax.scatter([a for a, b in pts], [b * sq for a, b in pts], s=s, color=color, zorder=2)
    ax.axhline(0, color=GR, lw=.5); ax.axvline(0, color=GR, lw=.5); ax.set_aspect('equal')


@fig('T14-e1')
def _():
    fig_, ax = plt.subplots(figsize=(4.2, 4.2)); _lattice(ax, 3)
    t = np.linspace(0, 2 * np.pi, 200); ax.plot(np.cos(t), np.sin(t), color=C2, lw=.8, ls='--')
    for z, lab in [(1, '1'), (-1, '−1'), (1j, 'i'), (-1j, '−i')]:
        ax.plot(z.real, z.imag, 'o', color=C2, ms=8, zorder=3); ax.text(z.real + .15, z.imag + .15, lab, color=C2)
    ax.set_title('Z[i]: units have norm a² + b² = 1', fontsize=9)
    save('T14-e1')


@fig('T14-e2')
def _():
    fig_, ax = plt.subplots(figsize=(4.6, 4.6)); cols = [C1, C3, C4, C2, '#9467bd']
    for a in range(-5, 6):
        for b in range(-5, 6):
            r = (a - 2 * b) % 5
            ax.plot(a, b, 'o', color=cols[r], ms=7 if r == 0 else 4, zorder=3 if r == 0 else 2)
    v1, v2 = np.array([2, 1]), np.array([-1, 2])
    ax.add_patch(plt.Polygon([[0, 0], v1, v1 + v2, v2], fc=C1, alpha=.12, ec=C1))
    ax.text(2.1, 1.1, '2+i'); ax.text(-1.4, 2.2, 'i(2+i)')
    ax.set_aspect('equal'); ax.axhline(0, color=GR, lw=.5); ax.axvline(0, color=GR, lw=.5)
    ax.set_title('ideal (2+i): big blue points; 5 colours = 5 classes', fontsize=9)
    save('T14-e2')


@fig('T14-e3')
def _():
    fig_, ax = plt.subplots(figsize=(5.0, 3.4)); ax.axis('off'); ax.set_xlim(0, 10); ax.set_ylim(0, 6)
    def B(x, y, t): ax.text(x, y, t, ha='center', va='center', fontsize=10, bbox=dict(boxstyle='round,pad=0.3', fc='white', ec=C1))
    B(5, 5.3, 'Q(√2, √3)'); B(2, 3, 'Q(√2)'); B(5, 3, 'Q(√6)'); B(8, 3, 'Q(√3)'); B(5, .7, 'Q')
    for x in (2, 5, 8):
        ax.plot([x, 5], [3.35, 4.95], color=GR); ax.plot([x, 5], [2.65, 1.05], color=GR)
        ax.text((x + 5) / 2 - .3, 4.2, '2', fontsize=8, color=C2); ax.text((x + 5) / 2 - .3, 1.8, '2', fontsize=8, color=C2)
    ax.text(9.2, 5.3, 'degree 4', fontsize=8, color=C2)
    save('T14-e3')


@fig('T14-e4')
def _():
    fig_, ax = plt.subplots(figsize=(4.2, 4.2))
    t = np.linspace(0, 2 * np.pi, 200); ax.plot(np.cos(t), np.sin(t), color=GR, lw=.6)
    z = [np.exp(2j * np.pi * k / 5) for k in range(5)]
    for k in range(5):
        ax.plot(z[k].real, z[k].imag, 'o', color=C1 if k else GR, ms=8); ax.text(1.12 * z[k].real - .08, 1.12 * z[k].imag, f'ζ^{k}' if k > 1 else ('ζ' if k else '1'))
    order = [1, 2, 4, 3, 1]
    for a, b in zip(order, order[1:]):
        ax.annotate('', xy=(z[b].real, z[b].imag), xytext=(z[a].real, z[a].imag), arrowprops=dict(arrowstyle='->', color=C2, connectionstyle='arc3,rad=0.15'))
    ax.set_aspect('equal'); ax.axis('off'); ax.set_title('σ₂: ζ ↦ ζ²  (order 4)', fontsize=9)
    save('T14-e4')


@fig('T14-1')
def _():
    ax = plt.gca(); a = np.linspace(-12, 12, 800)
    for s, c in [(1, C1), (-1, C3)]:
        b2 = (a ** 2 - s) / 2; m = b2 >= 0
        ax.plot(a[m], np.sqrt(b2[m]), color=c, lw=.8); ax.plot(a[m], -np.sqrt(b2[m]), color=c, lw=.8)
    u = 1 + math.sqrt(2); pts = []
    for k in range(-4, 5):
        x = u ** k; xb = (-1 / u) ** k; A, B_ = (x + xb) / 2, (x - xb) / (2 * math.sqrt(2))
        for sg in (1, -1): pts.append((sg * A, sg * B_))
    ax.plot([p[0] for p in pts], [p[1] for p in pts], 'o', color=C2, ms=4)
    ax.set_xlim(-12, 12); ax.set_ylim(-9, 9); ax.set_xlabel('a'); ax.set_ylabel('b')
    ax.set_title('a² − 2b² = 1 (blue), = −1 (green); units ±(1+√2)^k in red', fontsize=9)
    save('T14-1')


@fig('T14-2')
def _():
    fig_, ax = plt.subplots(figsize=(4.4, 4.0))
    for a in range(-1, 6):
        for b in range(-2, 3):
            ax.plot(a, b, '.', color=GR)
    w = (47 - 1j) / 13; ax.plot(w.real, w.imag, '*', color=C2, ms=12); ax.text(w.real + .1, w.imag + .25, 'α/β ≈ 3.62−0.08i', color=C2, fontsize=8)
    ax.plot(4, 0, 'o', color=C1, ms=8); ax.text(4.1, -.4, 'q = 4', color=C1, fontsize=8)
    ax.add_patch(plt.Circle((4, 0), .707, fill=False, ec=C1, ls='--'))
    ax.set_aspect('equal'); ax.set_title('rounding to the nearest lattice point: |α/β − q| ≤ 1/√2', fontsize=8)
    save('T14-2')


@fig('T14-3')
def _():
    fig_, axs = plt.subplots(1, 2, figsize=(6.6, 3.2))
    def table(ax, n, title):
        els = [(a, b) for a in range(n) for b in range(n)]
        M = np.zeros((len(els), len(els)))
        for i, (a, b) in enumerate(els):
            for j, (c, d) in enumerate(els):
                M[i, j] = 1 if ((a * c - b * d) % n, (a * d + b * c) % n) == (0, 0) else (2 if ((a * c - b * d) % n, (a * d + b * c) % n) == (1, 0) else 0)
        ax.imshow(M, cmap=matplotlib.colors.ListedColormap(['white', C2, C3]))
        ax.set_title(title, fontsize=8); ax.set_xticks([]); ax.set_yticks([])
    table(axs[0], 3, 'Z[i]/(3): green = product 1, red = 0')
    table(axs[1], 5, 'Z[i]/(5): red off the edges = zero divisors')
    save('T14-3')


@fig('T14-4')
def _():
    ax = plt.gca(); x = np.linspace(-.5, 3.2, 400); ax.plot(x, x ** 3 - 3 * x ** 2 + 3 * x - 3, color=C1)
    r = 1 + 2 ** (1 / 3); ax.plot(r, 0, 'o', color=C2); ax.text(r + .05, .6, '1 + ∛2', color=C2)
    ax.axhline(0, color=GR, lw=.6); ax.set_xlabel('x'); ax.set_title('x³ − 3x² + 3x − 3 = (x − 1)³ − 2', fontsize=9)
    save('T14-4')


@fig('T14-5')
def _():
    fig_, ax = plt.subplots(figsize=(6.4, 3.2)); ax.axis('off'); ax.set_xlim(0, 12); ax.set_ylim(0, 6)
    def B(x, y, t, c=C1): ax.text(x, y, t, ha='center', va='center', fontsize=8, bbox=dict(boxstyle='round,pad=0.3', fc='white', ec=c))
    B(3, 5.3, '{1}', C2); B(1, 3, '{1, σ}', C2); B(3, 3, '{1, στ}', C2); B(5, 3, '{1, τ}', C2); B(3, .7, 'G = {1, σ, τ, στ}', C2)
    B(9, .7, 'Q(√2, √3)'); B(7, 3, 'Q(√2)'); B(9, 3, 'Q(√6)'); B(11, 3, 'Q(√3)'); B(9, 5.3, 'Q')
    for x in (1, 3, 5):
        ax.plot([x, 3], [3.35, 4.95], color=GR); ax.plot([x, 3], [2.65, 1.05], color=GR)
    for x in (7, 9, 11):
        ax.plot([x, 9], [3.35, 4.95], color=GR); ax.plot([x, 9], [2.65, 1.05], color=GR)
    ax.annotate('', xy=(6.3, 3), xytext=(5.7, 3), arrowprops=dict(arrowstyle='<->', color=C3))
    ax.text(6, 3.5, 'fixed field', fontsize=7, ha='center', color=C3)
    save('T14-5')


@fig('T14-6')
def _():
    ax = plt.gca(); vals = sorted({a * a + 5 * b * b for a in range(0, 8) for b in range(0, 4)})
    vals = [v for v in vals if v <= 30]
    ax.bar(range(0, 31), [1 if v in vals else 0 for v in range(0, 31)], color=[C1 if v in vals else C2 for v in range(31)])
    for v in (2, 3): ax.text(v, .1, '✗', ha='center', color=C2, fontsize=12)
    ax.set_xlabel('n'); ax.set_yticks([]); ax.set_title('which n ≤ 30 are norms a² + 5b²? (blue = yes)', fontsize=9)
    save('T14-6')


# ---------- lesson 19: algebraic number theory ----------
def _hform(D):
    """reduced primitive forms (a,b,c) of discriminant D<0"""
    out = []; a = 1
    while 3 * a * a <= -D:
        for b in range(-a + 1, a + 1):
            if (b * b - D) % (4 * a) == 0:
                c = (b * b - D) // (4 * a)
                if c < a or gcd(gcd(a, abs(b)), c) != 1 or (b < 0 and a == c):
                    continue
                out.append((a, b, c))
        a += 1
    return out


def _sqfree(n):
    return all(n % (p * p) for p in range(2, int(n ** .5) + 1))


@fig('19-e1')
def _():
    fig_, ax = plt.subplots(figsize=(5.4, 3.6)); s5 = math.sqrt(5)
    for a in range(-4, 5):
        for b in range(-2, 3):
            ax.plot(a, b * s5, 'o', color=C1 if a * a + 5 * b * b in (4, 6, 9) else GR, ms=5)
    t = np.linspace(0, 2 * np.pi, 300)
    for n, c in [(2, C2), (3, C4), (6, C3)]:
        ax.plot(np.sqrt(n) * np.cos(t), np.sqrt(n) * np.sin(t), color=c, lw=1, label=f'a² + 5b² = {n}')
    for z, lab in [((2, 0), '2'), ((-3, 0), '3'), ((1, s5), '1+√−5'), ((1, -s5), '1−√−5')]:
        ax.text(z[0] + .1, z[1] + .25, lab, fontsize=8)
    ax.set_aspect('equal'); ax.legend(fontsize=7, loc='upper right'); ax.set_title('no lattice point has norm 2 or 3', fontsize=9)
    save('19-e1')


@fig('19-e2')
def _():
    fig_, axs = plt.subplots(1, 3, figsize=(7.2, 2.8))
    bases = [((1, 0), (0, 1), 'Z[i]'), ((1, 0), (.5, math.sqrt(3) / 2), 'Z[ω],  ω = (1+√−3)/2'), ((1, 0), (0, math.sqrt(5)), 'Z[√−5]')]
    for ax, (u, v, t) in zip(axs, bases):
        P = [(a * u[0] + b * v[0], a * u[1] + b * v[1]) for a in range(-4, 5) for b in range(-4, 5)]
        P = [p for p in P if abs(p[0]) <= 2.6 and abs(p[1]) <= 2.6]
        ax.plot([p[0] for p in P], [p[1] for p in P], 'o', color=C1, ms=4)
        ax.add_patch(plt.Polygon([[0, 0], u, (u[0] + v[0], u[1] + v[1]), v], fc=C4, alpha=.3))
        ax.set_aspect('equal'); ax.set_xlim(-2.7, 2.7); ax.set_ylim(-2.7, 2.7); ax.set_title(t, fontsize=8); ax.set_xticks([]); ax.set_yticks([])
    save('19-e2')


@fig('19-e3')
def _():
    fig_, ax = plt.subplots(figsize=(5.0, 3.8)); s5 = math.sqrt(5)
    for a in range(-5, 6):
        for b in range(-2, 3):
            inP = (a - b) % 2 == 0          # a + b√−5 ∈ (2, 1+√−5)  ⇔  a ≡ b (mod 2)
            ax.plot(a, b * s5, 'o', color=C1 if inP else GR, ms=7 if inP else 3)
    ax.add_patch(plt.Polygon([[0, 0], [2, 0], [3, s5], [1, s5]], fc=C1, alpha=.15, ec=C1))
    ax.text(2.1, -.6, '2'); ax.text(1.1, s5 + .3, '1+√−5')
    ax.set_aspect('equal'); ax.set_title('p₂ = {a + b√−5 : a ≡ b (mod 2)}: index 2', fontsize=9)
    save('19-e3')


@fig('19-e4')
def _():
    fig_, ax = plt.subplots(figsize=(6.6, 3.0))
    sq20 = {1, 3, 7, 9}
    ps = [p for p in PR if p < 200]
    for p in ps:
        if p in (2, 5): c, y = C2, 0
        elif p % 20 in sq20: c, y = C1, 1
        else: c, y = GR, -1
        ax.plot(p, y, 'o', color=c, ms=5)
    ax.set_yticks([-1, 0, 1]); ax.set_yticklabels(['inert', 'ramified', 'split'])
    ax.set_xlabel('p'); ax.set_title('Q(√−5): split ⇔ p ≡ 1, 3, 7, 9 (mod 20)', fontsize=9)
    save('19-e4')


@fig('19-e5')
def _():
    fig_, ax = plt.subplots(figsize=(4.4, 4.4)); s5 = math.sqrt(5)
    for a in range(-4, 5):
        for b in range(-2, 3):
            ax.plot(a, b * s5, 'o', color=C1, ms=4)
    ax.add_patch(plt.Polygon([[0, 0], [1, 0], [1, s5], [0, s5]], fc=C4, alpha=.35))
    from matplotlib.patches import Ellipse
    ax.add_patch(Ellipse((0, 0), 2 * 2.3, 2 * 2.9, fc='none', ec=C2, lw=1.5))
    ax.text(-1.5, 3.1, 'area > 4 · area of cell', color=C2, fontsize=8)
    ax.set_aspect('equal'); ax.set_xlim(-4, 4); ax.set_ylim(-4.6, 4.6); ax.set_title('Minkowski: big symmetric convex set ∋ lattice point ≠ 0', fontsize=8)
    save('19-e5')


@fig('19-e6')
def _():
    ax = plt.gca(); ds = [d for d in range(1, 401) if _sqfree(d)]
    hs = [len(_hform(-d if (-d) % 4 == 1 else -4 * d)) for d in ds]
    ax.plot(ds, hs, '.', color=C1, ms=3)
    ones = [d for d, h in zip(ds, hs) if h == 1]
    ax.plot(ones, [1] * len(ones), 'o', color=C2, ms=5)
    for d in ones:
        if d >= 19: ax.text(d, 2.2, str(d), fontsize=7, ha='center', color=C2)
    x = np.linspace(1, 400, 200); ax.plot(x, np.sqrt(4 * x) / np.pi, color=GR, ls='--', lw=.8, label='~ √|Δ| / π')
    ax.set_xlabel('d'); ax.set_ylabel('h(Q(√−d))'); ax.legend(fontsize=7); ax.set_title('class numbers; h = 1 only for 9 fields', fontsize=9)
    save('19-e6')


def _chi_m23():
    sq = set((k * k) % 23 for k in range(1, 23))
    return np.array([0] + [1 if r in sq else -1 for r in range(1, 23)])


@fig('19-e7')
def _():
    ax = plt.gca(); n = np.arange(1, 3001); c = _chi_m23()[n % 23]
    ax.plot(n, np.cumsum(c / n), color=C1, lw=.8)
    ax.axhline(3 * np.pi / np.sqrt(23), color=C2, ls='--', label='2π·3 / (2√23) ≈ 1.9652')
    ax.set_xlabel('N'); ax.set_ylim(1.3, 2.4); ax.legend(fontsize=8); ax.set_title('Σ_{n≤N} χ₋₂₃(n)/n', fontsize=9)
    save('19-e7')


@fig('19-1')
def _():
    ax = plt.gca(); ax.bar(['N(p₂)', 'N(p₃)', 'N(p₂)·N(p₃)', 'N(1+√−5)'], [2, 3, 6, 6], color=[C1, C4, C3, C2])
    ax.set_title('norms multiply', fontsize=9)
    save('19-1')


@fig('19-2')
def _():
    fig_, ax = plt.subplots(figsize=(4.6, 4.6))
    for a in range(-8, 9):
        for b in range(-8, 9):
            n = a * a + b * b
            g = (isp(n)) or (b == 0 and isp(abs(a)) and abs(a) % 4 == 3) or (a == 0 and isp(abs(b)) and abs(b) % 4 == 3)
            if g: ax.plot(a, b, 's', color=C2 if (a == 0 or b == 0) else C1, ms=4)
    ax.set_aspect('equal'); ax.set_title('Gaussian primes |a|, |b| ≤ 8', fontsize=9); ax.axhline(0, color=GR, lw=.4); ax.axvline(0, color=GR, lw=.4)
    save('19-2')


@fig('19-3')
def _():
    ax = plt.gca(); D = -47; F = _hform(D)
    b = np.linspace(-1, 1, 200); ax.fill_between(b, np.abs(b), 1.5, color=C4, alpha=.15)
    ax.plot(b, np.abs(b), color=GR, lw=.8)
    for (a_, b_, c_) in F:
        ax.plot(b_ / a_, a_ / math.sqrt(-D) * 2, 'o', color=C1)
        ax.text(b_ / a_ + .03, a_ / math.sqrt(-D) * 2 + .04, f'({a_},{b_},{c_})', fontsize=7)
    ax.set_xlabel('b / a'); ax.set_ylabel('scaled a'); ax.set_title('the 5 reduced forms of discriminant −47', fontsize=9)
    save('19-3')


@fig('19-4')
def _():
    ax = plt.gca(); n = np.arange(0, 46); v = n * n + n + 41
    ax.bar(n, v, color=[C3 if isp(int(x)) else C2 for x in v])
    ax.set_xlabel('n'); ax.set_title('n² + n + 41: green = prime', fontsize=9)
    save('19-4')


def _fund_unit_log(d):
    """log of the fundamental unit of Q(sqrt d), via the continued fraction of sqrt(d)"""
    a0 = int(math.isqrt(d)); m, dd, a = 0, 1, a0; p0, p1, q0, q1 = 1, a0, 0, 1
    for _ in range(2000):
        v = p1 * p1 - d * q1 * q1
        if d % 4 == 1 and abs(d) > 5:
            pass
        if v in (1, -1):
            best = math.log(p1 + q1 * math.sqrt(d))
            if d % 4 == 1:   # a smaller unit (x + y sqrt d)/2 with x, y odd may exist
                for y in range(1, q1 + 1, 2):
                    xs = [math.isqrt(d * y * y + s_) for s_ in (-4, 4) if d * y * y + s_ > 0 and math.isqrt(d * y * y + s_) ** 2 == d * y * y + s_]
                    if xs:
                        return math.log((min(xs) + y * math.sqrt(d)) / 2)
            return best
        m = dd * a - m; dd = (d - m * m) // dd; a = (a0 + m) // dd
        p0, p1 = p1, a * p1 + p0; q0, q1 = q1, a * q1 + q0
    return float('nan')


@fig('19-5')
def _():
    ax = plt.gca(); ds = [d for d in range(2, 101) if _sqfree(d)]
    L = [_fund_unit_log(d) for d in ds]
    ax.bar(ds, L, color=[C2 if d in (13, 19, 94) else C1 for d in ds])
    ax.set_xlabel('d'); ax.set_ylabel('log ε_d'); ax.set_title('size of the fundamental unit (red: d = 13, 19, 94)', fontsize=9)
    save('19-5')


@fig('19-6')
def _():
    ax = plt.gca(); ps = [p for p in PR if p < 120 and p != 5]
    f = []
    for p in ps:
        k, x = 1, p % 5
        while x != 1: x = x * p % 5; k += 1
        f.append(k)
    ax.scatter(ps, f, c=[{1: C3, 2: C4, 4: C1}[k] for k in f], s=18)
    ax.plot([5], [1], 'x', color=C2, ms=9); ax.text(6, 1.2, 'p = 5: e = 4', color=C2, fontsize=8)
    ax.set_yticks([1, 2, 4]); ax.set_xlabel('p'); ax.set_ylabel('f = order of p mod 5'); ax.set_title('Q(ζ₅): g = 4/f', fontsize=9)
    save('19-6')


# ---------- lesson 19a: class field theory ----------
def _roots_mod(f, p):
    return sum(1 for x in range(p) if f(x) % p == 0)


def _leg(a, p):
    a %= p
    if a == 0: return 0
    return 1 if pow(a, (p - 1) // 2, p) == 1 else -1


@fig('19a-e1')
def _():
    ax = plt.gca(); ps = [p for p in PR if 5 < p < 100000]
    cnt = [sum(1 for p in ps if p % 5 == r) for r in (1, 2, 3, 4)]
    ax.bar(['1', '2', '3', '4'], cnt, color=[C3, C1, C1, C1])
    for i, c in enumerate(cnt): ax.text(i, c + 30, str(c), ha='center', fontsize=8)
    ax.set_xlabel('p mod 5  (Frob_p = σ_p in Gal(Q(ζ₅)/Q))'); ax.set_ylabel('# primes < 10⁵')
    ax.set_title('Artin map for Q(ζ₅): green = splits completely', fontsize=9)
    save('19a-e1')


@fig('19a-e2')
def _():
    ax = plt.gca(); ps = [p for p in PR if 2 < p < 400 and p != 5]
    f1 = lambda p: any(x * x + 5 * y * y == p for x in range(21) for y in range(10))
    f2 = lambda p: any(2 * x * x + 2 * x * y + 3 * y * y == p for x in range(-20, 21) for y in range(-20, 21))
    for p in ps:
        c = C3 if f1(p) else (C4 if f2(p) else GR)
        ax.scatter(p, p % 20, color=c, s=14)
    ax.set_yticks([1, 3, 7, 9, 11, 13, 17, 19]); ax.set_xlabel('p'); ax.set_ylabel('p mod 20')
    ax.set_title('green: p = x²+5y²,  orange: p = 2x²+2xy+3y²,  grey: neither', fontsize=9)
    save('19a-e2')


@fig('19a-e3')
def _():
    ax = plt.gca(); ps = [p for p in PR if p < 300 and p != 7]
    f = lambda x: x ** 3 + x * x - 2 * x - 1
    r = [_roots_mod(f, p) for p in ps]
    ax.scatter(ps, [p % 7 for p in ps], c=[C3 if k == 3 else GR for k in r], s=16)
    ax.set_yticks(range(7)); ax.set_xlabel('p'); ax.set_ylabel('p mod 7')
    ax.set_title('x³+x²−2x−1 has 3 roots mod p (green) iff p ≡ ±1 (mod 7)', fontsize=9)
    save('19a-e3')


@fig('19a-e4')
def _():
    ax = plt.gca(); ps = [p for p in PR if p < 600 and p != 23]
    f = lambda x: x ** 3 - x - 1
    rep = lambda p: any(x * x + x * y + 6 * y * y == p for x in range(-60, 61) for y in range(0, 30))
    for p in ps:
        k = _roots_mod(f, p)
        ax.scatter(p, k, color=C3 if rep(p) else (C1 if k == 1 else GR), s=14)
    ax.set_yticks([0, 1, 3]); ax.set_xlabel('p'); ax.set_ylabel('# roots of x³−x−1 mod p')
    ax.set_title('green: p = x²+xy+6y² (splits completely in the Hilbert class field of Q(√−23))', fontsize=8)
    save('19a-e4')


def _hilb(a, b, p):
    def v(n):
        k = 0
        while n % p == 0: n //= p; k += 1
        return k
    al, be = v(a), v(b); u, w = a // p ** al, b // p ** be
    if p != 2:
        return (-1) ** (al * be * ((p - 1) // 2)) * _leg(u, p) ** be * _leg(w, p) ** al
    e = lambda x: ((x - 1) // 2) % 2
    om = lambda x: ((x * x - 1) // 8) % 2
    return (-1) ** (e(u) * e(w) + al * om(w) + be * om(u))


@fig('19a-e5')
def _():
    vals = [-1, 2, 3, 5, 6, -3, 7]
    fig_, axs = plt.subplots(1, 3, figsize=(7.2, 2.8))
    for ax, p in zip(axs, (2, 3, 5)):
        M = np.array([[_hilb(a, b, p) for b in vals] for a in vals])
        ax.imshow(M, cmap='RdYlGn', vmin=-1, vmax=1)
        ax.set_xticks(range(len(vals))); ax.set_xticklabels(vals, fontsize=7)
        ax.set_yticks(range(len(vals))); ax.set_yticklabels(vals, fontsize=7)
        ax.set_title(f'(a, b)_{p}', fontsize=9)
    save('19a-e5')


@fig('19a-e6')
def _():
    ax = plt.gca(); w = cmath.exp(2j * pi / 3)
    t = np.linspace(0, 2 * pi, 200); ax.plot(np.cos(t), np.sin(t), color=GR, lw=0.8)
    for p in [p for p in PR if p % 3 == 1 and p < 400]:
        g = next(g for g in range(2, p) if all(pow(g, (p - 1) // q, p) != 1 for q in set(_pf(p - 1))))
        ind = {pow(g, k, p): k for k in range(p - 1)}
        chi = lambda a: 0 if a % p == 0 else w ** (ind[a % p] % 3)
        J = sum(chi(a) * chi(1 - a) for a in range(p)) / sqrt(p)
        ax.plot(J.real, J.imag, 'o', color=C1, ms=3)
    ax.set_aspect('equal'); ax.set_title('Jacobi sums J(χ,χ)/√p for cubic χ, p ≡ 1 (mod 3), p < 400', fontsize=9)
    save('19a-e6')


def _pf(n):
    out, d = [], 2
    while d * d <= n:
        while n % d == 0: out.append(d); n //= d
        d += 1
    if n > 1: out.append(n)
    return out


@fig('19a-1')
def _():
    ax = plt.gca(); ps = [p for p in PR if 2 < p < 400]
    ax.scatter(ps, [p % 8 for p in ps], c=[C3 if p % 8 in (1, 7) else C2 for p in ps], s=14)
    ax.set_yticks([1, 3, 5, 7]); ax.set_xlabel('p'); ax.set_ylabel('p mod 8')
    ax.set_title('Q(√2) ⊂ Q(ζ₈): p splits (green) iff p ≡ ±1 (mod 8)', fontsize=9)
    save('19a-1')


@fig('19a-2')
def _():
    ax = plt.gca(); places = ['∞', '2', '3', '5', '7', '11']
    pairs = [(-1, -1), (2, 3), (3, 5), (-1, 3)]
    for i, (a, b) in enumerate(pairs):
        row = [(-1 if (a < 0 and b < 0) else 1)] + [_hilb(a, b, p) for p in (2, 3, 5, 7, 11)]
        for j, s in enumerate(row):
            ax.add_patch(plt.Rectangle((j, -i), 0.9, 0.9, color=C3 if s == 1 else C2))
            ax.text(j + 0.45, -i + 0.45, '+' if s == 1 else '−', ha='center', va='center', color='w')
    ax.set_xlim(-0.2, 6); ax.set_ylim(-3.2, 1); ax.axis('off')
    for j, pl in enumerate(places): ax.text(j + 0.45, 1.0, pl, ha='center', fontsize=9)
    for i, (a, b) in enumerate(pairs): ax.text(-0.15, -i + 0.45, f'({a},{b})', ha='right', va='center', fontsize=9)
    ax.set_title('Hilbert symbols: an even number of − in each row (product formula)', fontsize=9)
    save('19a-2')


@fig('19a-3')
def _():
    ax = plt.gca(); ps = [p for p in PR if p % 3 == 1 and p < 400]
    cube = lambda p: pow(2, (p - 1) // 3, p) == 1
    rep = lambda p: any(x * x + 27 * y * y == p for x in range(0, 21) for y in range(0, 4))
    ax.scatter(ps, [1 if cube(p) else 0 for p in ps], c=[C3 if rep(p) else GR for p in ps], s=16)
    ax.set_yticks([0, 1]); ax.set_yticklabels(['2 not a cube', '2 a cube'])
    ax.set_xlabel('p ≡ 1 (mod 3)'); ax.set_title('green: p = x² + 27y²  (Gauss)', fontsize=9)
    save('19a-3')


@fig('19a-4')
def _():
    ax = plt.gca(); ps = [p for p in PR if 2 < p < 400 and p != 5]
    split = [p for p in ps if _leg(-5, p) == 1 and _leg(-1, p) == 1]
    ax.scatter(ps, [p % 20 for p in ps], c=[C3 if p in split else GR for p in ps], s=14)
    ax.set_yticks([1, 3, 7, 9, 11, 13, 17, 19]); ax.set_xlabel('p'); ax.set_ylabel('p mod 20')
    ax.set_title('splits completely in Q(√−5, i): (−5/p) = (−1/p) = 1  ⇔  p ≡ 1, 9 (mod 20)', fontsize=8)
    save('19a-4')


@fig('19a-5')
def _():
    ax = plt.gca(); reps = [1, 3, 5, 7, 2, 6, 10, 14]
    for i, d in enumerate(reps):
        ram = d not in (1, 5)
        ax.add_patch(plt.Circle((i % 4, -(i // 4)), 0.35, color=GR if d == 1 else (C2 if ram else C3)))
        ax.text(i % 4, -(i // 4), str(d), ha='center', va='center', color='w')
    ax.set_xlim(-0.6, 3.6); ax.set_ylim(-1.6, 0.6); ax.set_aspect('equal'); ax.axis('off')
    ax.set_title('Q₂*/(Q₂*)²: 8 classes; green = unramified Q₂(√5), red = 6 ramified', fontsize=9)
    save('19a-5')



@fig('19a-6')
def _():
    ax = plt.gca(); p = 5
    for a, c in zip((1, 2, 3, 4), (GR, C1, C2, C3)):
        ks = range(0, 7)
        vals = [pow(a, p ** k, p ** 7) / p ** 7 for k in ks]
        ax.plot(list(ks), vals, 'o-', color=c, label=f'a = {a}', ms=4)
    ax.set_xlabel('k'); ax.set_ylabel('a^(5^k) mod 5⁷  (scaled to [0,1))')
    ax.legend(fontsize=8); ax.set_title('Teichmüller lift ω(a) = lim a^(5^k) in ℤ₅', fontsize=9)
    save('19a-6')



# ---------- lesson 20: elliptic curves ----------
def _ec_ap_short(f, p):
    """a_p = -sum_x (f(x)/p) for y^2 = f(x), p odd, via a table of squares."""
    x = np.arange(p, dtype=np.int64)
    v = f(x) % p
    sq = np.zeros(p, dtype=np.int8); sq[(x * x) % p] = 1
    chi = np.where(v == 0, 0, np.where(sq[v] == 1, 1, -1))
    return -int(chi.sum())


def _f11a(x):
    # (2y+1)^2 = 4x^3 - 4x^2 - 40x - 79  for  y^2 + y = x^3 - x^2 - 10x - 20
    return 4 * x ** 3 - 4 * x ** 2 - 40 * x - 79


def _real_branch(ax, a, b, xmin, xmax, color=C1):
    xs = np.linspace(xmin, xmax, 4000); v = xs ** 3 + a * xs + b
    m = v >= 0; xs, v = xs[m], np.sqrt(v[m])
    brk = np.where(np.diff(xs) > (xmax - xmin) / 3000)[0] + 1
    for seg in np.split(np.arange(len(xs)), brk):
        ax.plot(xs[seg], v[seg], color=color); ax.plot(xs[seg], -v[seg], color=color)


@fig('20-e1')
def _():
    ax = plt.gca(); _real_branch(ax, 0, -2, 1.2, 6.2)
    P = (3, 5); l = 27 / 10; x2, y2 = 129 / 100, 383 / 1000
    xs = np.linspace(0.8, 5.5, 50); ax.plot(xs, 5 + l * (xs - 3), color=C4, lw=1)
    ax.plot(*P, 'o', color=C2); ax.text(3.1, 4.4, 'P = (3, 5)', fontsize=8)
    ax.plot(x2, y2, 'o', color=C4); ax.text(1.35, 1.0, '−2P (third intersection)', fontsize=8)
    ax.plot(x2, -y2, 'o', color=C3); ax.text(1.35, -1.8, '2P = (129/100, −383/1000)', fontsize=8)
    ax.plot([x2, x2], [-y2, y2], ':', color=GR)
    ax.set_title('y² = x³ − 2: tangent at P meets the curve again at −2P', fontsize=9)
    ax.set_xlim(0.8, 6.2); ax.set_ylim(-14, 14)
    save('20-e1')


@fig('20-e2')
def _():
    ax = plt.gca(); _real_branch(ax, 0, 1, -1.0, 3.2)
    pts = {'O': None, 'P = (2, 3)': (2, 3), '2P = (0, 1)': (0, 1), '3P = (−1, 0)': (-1, 0),
           '4P = (0, −1)': (0, -1), '5P = (2, −3)': (2, -3)}
    for k, (lab, Q) in enumerate(pts.items()):
        if Q: ax.plot(*Q, 'o', color=C2); ax.text(Q[0] + 0.08, Q[1] + 0.25, lab, fontsize=8)
    ax.set_title('y² = x³ + 1: the torsion group is cyclic of order 6', fontsize=9)
    save('20-e2')


@fig('20-e3')
def _():
    fig_, axs = plt.subplots(1, 2, figsize=(7.2, 3.0))
    ax = axs[0]; _real_branch(ax, -36, 0, -6.0, 9.0)
    ax.plot(-3, 9, 'o', color=C2); ax.text(-2.8, 10, '(−3, 9)', fontsize=8)
    ax.plot(25 / 4, -35 / 8, 'o', color=C3); ax.text(6.4, -6, '(25/4, −35/8)', fontsize=8)
    ax.set_title('y² = x³ − 36x', fontsize=9)
    ax = axs[1]
    for (a, b, c), col in (((3, 4, 5), C2), ((0.7, 120 / 7, 1201 / 70), C3)):
        ax.plot([0, a, 0, 0], [0, 0, b, 0], color=col)
    ax.text(1.0, 1.0, '3, 4, 5', color=C2, fontsize=8); ax.text(0.9, 9, '7/10, 120/7, 1201/70', color=C3, fontsize=8)
    ax.set_aspect('equal'); ax.set_title('two right triangles of area 6', fontsize=9)
    save('20-e3')


@fig('20-e4')
def _():
    ax = plt.gca(); ps = [p for p in PR if 2 < p < 3000 and p != 11]
    ap = [_ec_ap_short(_f11a, p) for p in ps]
    ax.scatter(ps, ap, s=4, color=C1)
    xs = np.linspace(3, 3000, 300); ax.plot(xs, 2 * np.sqrt(xs), color=C2); ax.plot(xs, -2 * np.sqrt(xs), color=C2)
    ax.set_xlabel('p'); ax.set_ylabel('a_p = p + 1 − #E(F_p)')
    ax.set_title('Hasse: |a_p| ≤ 2√p  (curve 11a: y² + y = x³ − x² − 10x − 20)', fontsize=9)
    save('20-e4')


@fig('20-e5')
def _():
    ax = plt.gca(); ps = [p for p in PR if 2 < p < 400]
    ap = [_ec_ap_short(lambda x: x ** 3 - x, p) for p in ps]
    ax.scatter(ps, ap, s=10, c=[C2 if p % 4 == 3 else C3 for p in ps])
    xs = np.linspace(3, 400, 200); ax.plot(xs, 2 * np.sqrt(xs), color=GR, lw=0.8); ax.plot(xs, -2 * np.sqrt(xs), color=GR, lw=0.8)
    ax.set_xlabel('p'); ax.set_ylabel('a_p')
    ax.set_title('y² = x³ − x (CM by ℤ[i]): a_p = 0 for p ≡ 3 (mod 4) (red), ±2a when p = a² + b² (green)', fontsize=8)
    save('20-e5')


@fig('20-e6')
def _():
    fig_, axs = plt.subplots(1, 2, figsize=(7.2, 3.0)); ps = [p for p in PR if 2 < p < 20000 and p != 11]
    for ax, f, name in ((axs[0], _f11a, '11a (no CM)'), (axs[1], lambda x: x ** 3 - x, 'y² = x³ − x (CM)')):
        th = [math.acos(max(-1, min(1, _ec_ap_short(f, p) / (2 * sqrt(p))))) for p in ps if not (name.startswith('y') and p == 2)]
        ax.hist(th, bins=30, density=True, color=C1, alpha=0.7)
        t = np.linspace(0, pi, 200); ax.plot(t, 2 / pi * np.sin(t) ** 2, color=C2)
        ax.set_xlabel('θ_p,  a_p = 2√p cos θ_p'); ax.set_title(name + ', p < 20000', fontsize=9)
    save('20-e6')


@fig('20-e7')
def _():
    ax = plt.gca(); ks = range(1, 41)
    def first_k(m):
        f = 1
        for k in ks:
            f *= k
            if f % m == 0: return k
    k1, k2 = first_k(640), first_k(777)
    ax.plot(list(ks), [1 if math.factorial(k) % 640 == 0 else 0 for k in ks], 'o-', color=C3, ms=3, label='640 | k!  (mod 599)')
    ax.plot(list(ks), [1.1 if math.factorial(k) % 777 == 0 else 0.1 for k in ks], 's-', color=C1, ms=3, label='777 | k!  (mod 761)')
    ax.axvline(k1, color=C3, ls=':'); ax.axvline(k2, color=C1, ls=':')
    ax.set_yticks([]); ax.set_xlabel('k'); ax.legend(fontsize=8)
    ax.set_title(f'ECM on 455839 = 599·761: k!·P vanishes mod 599 from k = {k1}, mod 761 only from k = {k2}', fontsize=8)
    save('20-e7')


@fig('20-1')
def _():
    ax = plt.gca(); _real_branch(ax, -36, 0, -6.0, 26.0)
    for (x, y), lab in (((-3, 9), 'P'), ((25 / 4, -35 / 8), '2P')):
        ax.plot(x, y, 'o', color=C2); ax.text(x + 0.4, y + 3, lab, fontsize=9)
    ax.set_title('2P on y² = x³ − 36x is not integral ⇒ P has infinite order (Nagell–Lutz)', fontsize=9)
    save('20-1')


@fig('20-2')
def _():
    ax = plt.gca(); _real_branch(ax, -1, 0, -1.2, 2.6)
    for Q in ((-1, 0), (0, 0), (1, 0)): ax.plot(*Q, 'o', color=C2)
    ax.set_title('y² = x³ − x: E(ℚ)_tors = {O, (−1,0), (0,0), (1,0)} ≅ ℤ/2 × ℤ/2', fontsize=9)
    save('20-2')


@fig('20-3')
def _():
    fig_, axs = plt.subplots(1, 2, figsize=(7.0, 3.2))
    for ax, p in zip(axs, (7, 13)):
        pts = [(x, y) for x in range(p) for y in range(p) if (y * y - x ** 3 + 2) % p == 0]
        ax.scatter([q[0] for q in pts], [q[1] for q in pts], color=C1, s=20)
        ax.set_xlim(-0.5, p - 0.5); ax.set_ylim(-0.5, p - 0.5); ax.set_aspect('equal')
        ax.set_title(f'y² = x³ − 2 over F_{p}: {len(pts)} + O = {len(pts) + 1} points', fontsize=9)
    save('20-3')


@fig('20-4')
def _():
    ax = plt.gca(); ps = [p for p in PR if p % 4 == 1 and p < 400]
    ap = [_ec_ap_short(lambda x: x ** 3 - x, p) for p in ps]
    a = [next(u for u in range(1, 30, 2) if any(u * u + v * v == p for v in range(0, 30, 2))) for p in ps]
    ax.scatter(ps, [abs(t) for t in ap], color=C1, s=14, label='|a_p|')
    ax.scatter(ps, [2 * u for u in a], marker='x', color=C2, s=20, label='2a  (p = a² + b², a odd)')
    ax.legend(fontsize=8); ax.set_xlabel('p ≡ 1 (mod 4)'); ax.set_title('y² = x³ − x: |a_p| = 2a', fontsize=9)
    save('20-4')


@fig('20-5')
def _():
    ax = plt.gca(); ns = [n for n in range(1, 60) if all(n % (k * k) for k in range(2, 8))]
    from itertools import product
    def cnt(A, B, C, n):
        L = int(math.isqrt(n)) + 1
        return sum(1 for x, y, z in product(range(-L, L + 1), repeat=3) if A * x * x + B * y * y + C * z * z == n)
    col = []
    for n in ns:
        if n % 2: A, B = cnt(2, 1, 32, n), cnt(2, 1, 8, n)
        else: A, B = cnt(4, 1, 32, n // 2), cnt(4, 1, 8, n // 2)
        col.append(C3 if B == 2 * A else GR)
    ax.bar(ns, [1] * len(ns), color=col); ax.set_yticks([]); ax.set_xlabel('square-free n')
    ax.set_title("Tunnell's criterion: green = predicted congruent (proved, assuming BSD)", fontsize=9)
    save('20-5')


@fig('20-6')
def _():
    ax = plt.gca(); n = 455839
    ax.bar(['599', '761'], [640, 777], color=[C3, C1])
    ax.text(0, 660, '640 = 2⁷·5', ha='center', fontsize=9); ax.text(1, 797, '777 = 3·7·37', ha='center', fontsize=9)
    ax.set_ylabel('#E(F_p)'); ax.set_ylim(0, 900)
    ax.set_title('y² = x³ + 5x − 5: smooth group order mod 599, not mod 761', fontsize=9)
    save('20-6')



# ---------- lesson 21: modular forms ----------
def _sigma(n, k):
    return sum(d ** k for d in range(1, n + 1) if n % d == 0)


_TAU_CACHE = {}


def _tau_list(N):
    if N in _TAU_CACHE: return _TAU_CACHE[N]
    # Delta = q * prod (1 - q^n)^24 via Euler's pentagonal series cubed: prod(1-q^n)^3 = sum (-1)^m (2m+1) q^{m(m+1)/2}
    c3 = [0] * N
    m = 0
    while m * (m + 1) // 2 < N:
        c3[m * (m + 1) // 2] = (-1) ** m * (2 * m + 1); m += 1
    def mul(a, b):
        out = [0] * N
        nz = [(i, x) for i, x in enumerate(a) if x]
        for j, y in enumerate(b):
            if y:
                for i, x in nz:
                    if i + j >= N: break
                    out[i + j] += x * y
        return out
    c6 = mul(c3, c3); c12 = mul(c6, c6); c24 = mul(c12, c12)
    tau = [0] + c24[:N - 1]
    _TAU_CACHE[N] = tau
    return tau


def _fd_boundary(ax, color='k'):
    t = np.linspace(pi / 3, 2 * pi / 3, 100)
    ax.plot(np.cos(t), np.sin(t), color=color); ax.plot([-0.5, -0.5], [np.sqrt(3) / 2, 2.6], color=color)
    ax.plot([0.5, 0.5], [np.sqrt(3) / 2, 2.6], color=color)


@fig('21-e1')
def _():
    ax = plt.gca()
    # images of the fundamental domain under a few matrices
    base_t = np.linspace(pi / 3, 2 * pi / 3, 60)
    arc = np.cos(base_t) + 1j * np.sin(base_t)
    left = -0.5 + 1j * np.linspace(np.sqrt(3) / 2, 6, 60); right = 0.5 + 1j * np.linspace(6, np.sqrt(3) / 2, 60)
    F = np.concatenate([arc[::-1], left, right])
    mats = [(1, n, 0, 1) for n in range(-3, 3)] + [(n, -1, 1, 0) for n in range(-2, 3)] + [(1, 0, n, 1) for n in (-2, 2, 3, -3)]
    for a, b, c, d in mats:
        Z = (a * F + b) / (c * F + d)
        ax.fill(Z.real, Z.imag, color=C1 if (a, b, c, d) == (1, 0, 0, 1) else '#cfe2f3', ec='#7f9fbf', lw=0.6, alpha=0.9)
    path = [0.3 + 0.1j, -3 + 1j, 1j]
    ax.annotate('', xy=(-3, 1), xytext=(0.3, 0.1), arrowprops=dict(arrowstyle='->', color=C2))
    ax.annotate('', xy=(0, 1), xytext=(-3, 1), arrowprops=dict(arrowstyle='->', color=C4))
    for z, lab in zip(path, ['τ = (3+i)/10', 'S: −1/τ = −3+i', 'T³: i']):
        ax.plot(z.real, z.imag, 'o', color=C2, ms=4); ax.text(z.real + 0.05, z.imag + 0.08, lab, fontsize=8)
    ax.set_xlim(-3.4, 2.2); ax.set_ylim(0, 2.2); ax.set_aspect('equal')
    ax.set_title('fundamental domain of SL₂(ℤ) (dark) and some of its images', fontsize=9)
    save('21-e1')


@fig('21-e2')
def _():
    ax = plt.gca(); N = 40
    xs = np.linspace(-1.5, 1.5, 300); ys = np.linspace(0.15, 1.6, 150)
    X, Y = np.meshgrid(xs, ys); Q = np.exp(2j * pi * (X + 1j * Y))
    tau = _tau_list(N)
    D = sum(tau[n] * Q ** n for n in range(1, N))
    V = np.log10(np.abs(D) * Y ** 6 + 1e-300)
    im = ax.imshow(V, extent=(xs[0], xs[-1], ys[0], ys[-1]), origin='lower', cmap='viridis', vmin=-8, vmax=-1.3, aspect='auto')
    _fd_boundary(ax, 'w'); plt.colorbar(im, ax=ax, fraction=0.03); ax.set_ylim(ys[0], ys[-1])
    ax.set_title('log₁₀( y⁶ |Δ(x + iy)| ): invariant under τ ↦ τ + 1 and τ ↦ −1/τ', fontsize=9)
    save('21-e2')


@fig('21-e3')
def _():
    ax = plt.gca(); ps = [p for p in PR if p < 1500]
    tau = _tau_list(1500)
    x = [tau[p] / (2 * p ** 5.5) for p in ps]
    ax.hist([math.acos(t) for t in x], bins=25, density=True, color=C1, alpha=0.7)
    t = np.linspace(0, pi, 200); ax.plot(t, 2 / pi * np.sin(t) ** 2, color=C2)
    ax.set_xlabel('θ_p,  τ(p) = 2p^(11/2) cos θ_p'); ax.set_title('Ramanujan τ(p), p < 1500: Deligne bound and Sato–Tate', fontsize=9)
    save('21-e3')


@fig('21-e4')
def _():
    ax = plt.gca(); ds = [3, 4, 7, 8, 11, 19, 43, 67, 163]
    js = {3: 0, 4: 1728, 7: -3375, 8: 8000, 11: -32768, 19: -884736, 43: -884736000, 67: -147197952000, 163: -262537412640768000}
    err = [abs(math.exp(pi * sqrt(d)) - (abs(js[d]) + 744)) if d % 4 == 3 and d > 3 else None for d in ds]
    pts = [(d, e) for d, e in zip(ds, err) if e]
    ax.semilogy([p[0] for p in pts], [p[1] for p in pts], 'o-', color=C1)
    for d, e in pts: ax.text(d + 2, e, f'{e:.2g}', fontsize=8)
    ax.set_xlabel('d (class number 1)'); ax.set_ylabel('|e^(π√d) − (|j| + 744)|')
    ax.set_title('e^(π√d) is almost an integer: j((1+√−d)/2) is an integer', fontsize=9)
    save('21-e4')


@fig('21-e5')
def _():
    ax = plt.gca(); ns = range(1, 200)
    r4 = [8 * sum(d for d in range(1, n + 1) if n % d == 0 and d % 4) for n in ns]
    ax.scatter(list(ns), [r / n for r, n in zip(r4, ns)], s=8, c=[C2 if n % 2 == 0 else C1 for n in ns])
    ax.set_xlabel('n'); ax.set_ylabel('r₄(n) / n'); ax.set_title('Jacobi: r₄(n) = 8 Σ_{d | n, 4 ∤ d} d  (red: n even)', fontsize=9)
    save('21-e5')


@fig('21-e6')
def _():
    ax = plt.gca(); N = 400; p = [1] + [0] * N
    for k in range(1, N + 1):
        for n in range(k, N + 1): p[n] += p[n - k]
    ns = np.arange(1, N + 1)
    hr = np.exp(pi * np.sqrt(2 * ns / 3)) / (4 * ns * sqrt(3))
    ax.plot(ns, np.array(p[1:], dtype=float) / hr, color=C1)
    ax.axhline(1, color=GR, ls=':'); ax.set_xlabel('n'); ax.set_ylabel('p(n) / HR(n)')
    ax.set_title('partitions vs Hardy–Ramanujan e^(π√(2n/3)) / (4n√3)', fontsize=9)
    save('21-e6')


@fig('21-1')
def _():
    ax = plt.gca(); ns = range(1, 30)
    lhs = [_sigma(n, 7) for n in ns]
    rhs = [_sigma(n, 3) + 120 * sum(_sigma(m, 3) * _sigma(n - m, 3) for m in range(1, n)) for n in ns]
    ax.semilogy(list(ns), lhs, 'o', color=C1, label='σ₇(n)'); ax.semilogy(list(ns), rhs, 'x', color=C2, label='σ₃(n) + 120 Σ σ₃(m)σ₃(n−m)')
    ax.legend(fontsize=8); ax.set_xlabel('n'); ax.set_title('E₄² = E₈ as an identity of divisor sums', fontsize=9)
    save('21-1')


@fig('21-2')
def _():
    ax = plt.gca(); tau = _tau_list(30); ns = range(1, 30)
    ax.bar(list(ns), [np.sign(tau[n]) * math.log10(abs(tau[n])) for n in ns], color=[C1 if tau[n] > 0 else C2 for n in ns])
    ax.set_xlabel('n'); ax.set_ylabel('sign · log₁₀|τ(n)|'); ax.set_title('Ramanujan τ(n) for n < 30', fontsize=9)
    save('21-2')


@fig('21-3')
def _():
    ax = plt.gca(); tau = _tau_list(60); ns = range(1, 60)
    ax.scatter(list(ns), [(tau[n] - _sigma(n, 11)) % 691 for n in ns], color=C3, s=12)
    ax.set_ylim(-20, 690); ax.set_xlabel('n'); ax.set_ylabel('(τ(n) − σ₁₁(n)) mod 691')
    ax.set_title('Ramanujan: τ(n) ≡ σ₁₁(n) (mod 691) – always 0', fontsize=9)
    save('21-3')


@fig('21-4')
def _():
    ax = plt.gca(); from itertools import product as _prod
    ns = list(range(1, 31))
    direct = [sum(1 for v in _prod(range(-6, 7), repeat=4) if sum(t * t for t in v) == n) for n in ns]
    formula = [8 * sum(d for d in range(1, n + 1) if n % d == 0 and d % 4) for n in ns]
    ax.bar(ns, direct, color=C1, alpha=0.6, label='direct count')
    ax.plot(ns, formula, 'x', color=C2, label='8 Σ_{4∤d|n} d')
    ax.plot([12], [96], 'o', mfc='none', mec='k', ms=10)
    ax.legend(fontsize=8); ax.set_xlabel('n'); ax.set_ylabel('r₄(n)'); ax.set_title('r₄(n): direct count vs Jacobi (n = 12 circled)', fontsize=9)
    save('21-4')


@fig('21-5')
def _():
    ax = plt.gca(); _fd_boundary(ax)
    z0 = 0.5 + 1j / (2 * sqrt(3)); z1 = -1 / z0; z2 = z1 + 1
    for z, lab in ((z0, 'τ = 1/2 + i/(2√3)'), (z1, '−1/τ'), (z2, 'ρ = e^(2πi/3)')):
        ax.plot(z.real, z.imag, 'o', color=C2, ms=4); ax.text(z.real + 0.05, z.imag + 0.05, lab, fontsize=8)
    ax.annotate('', xy=(z1.real, z1.imag), xytext=(z0.real, z0.imag), arrowprops=dict(arrowstyle='->', color=C2))
    ax.annotate('', xy=(z2.real, z2.imag), xytext=(z1.real, z1.imag), arrowprops=dict(arrowstyle='->', color=C4))
    ax.set_xlim(-1.8, 1.2); ax.set_ylim(0, 1.6); ax.set_aspect('equal'); ax.set_title('reducing τ to the fundamental domain', fontsize=9)
    save('21-5')


@fig('21-6')
def _():
    ax = plt.gca(); N = 60; p = [1] + [0] * N
    for k in range(1, N + 1):
        for n in range(k, N + 1): p[n] += p[n - k]
    ns = list(range(N + 1))
    ax.scatter(ns, [p[n] % 5 for n in ns], c=[C3 if n % 5 == 4 else GR for n in ns], s=14)
    ax.set_xlabel('n'); ax.set_ylabel('p(n) mod 5'); ax.set_title('Ramanujan: p(5n + 4) ≡ 0 (mod 5)  (green)', fontsize=9)
    save('21-6')


if __name__ == '__main__':
    import sys
    keys = sys.argv[1:] or sorted(FIGS)
    for k in keys:
        FIGS[k]()
    print('drew', len(keys), 'figures into', OUT)

