# הוכחה ש-e אי-רציונלי

ה[מספר $`e`$](https://he.wikipedia.org/wiki/e_%28%D7%A7%D7%91%D7%95%D7%A2_%D7%9E%D7%AA%D7%9E%D7%98%D7%99%29) הוצג על ידי [יעקב ברנולי](https://he.wikipedia.org/wiki/%D7%99%D7%A2%D7%A7%D7%91_%D7%91%D7%A8%D7%A0%D7%95%D7%9C%D7%99) ב-1683. יותר מחצי מאה אחר כך הוכיח [לאונרד אוילר](https://he.wikipedia.org/wiki/%D7%9C%D7%90%D7%95%D7%A0%D7%A8%D7%93_%D7%90%D7%95%D7%99%D7%9C%D7%A8), שהיה תלמידו של יוהאן ברנולי, אחיו הצעיר של יעקב, ש-$`e`$ הוא [אי-רציונלי](https://he.wikipedia.org/wiki/%D7%9E%D7%A1%D7%A4%D7%A8_%D7%90%D7%99-%D7%A8%D7%A6%D7%99%D7%95%D7%A0%D7%9C%D7%99), כלומר אי אפשר לכתוב אותו כמנה של שני שלמים.

## ההוכחה של אוילר

אוילר כתב את ההוכחה הראשונה לאי-הרציונליות של $`e`$ ב-1737 (אבל הטקסט פורסם רק שבע שנים אחר כך).[^1][^2] הוא חישב את הייצוג של $`e`$ כ[שבר משולב](https://he.wikipedia.org/wiki/%D7%A9%D7%91%D7%A8_%D7%9E%D7%A9%D7%95%D7%9C%D7%91) פשוט:



```math
e = [2; 1, 2, 1, 1, 4, 1, 1, 6, 1, 1, 8, 1, 1, \ldots, 2n, 1, 1, \ldots].
```

 כיוון שהשבר המשולב הזה אינסופי, ולכל מספר רציונלי יש שבר משולב סופי (זה בדיוק [האלגוריתם של אוקלידס](https://he.wikipedia.org/wiki/%D7%94%D7%90%D7%9C%D7%92%D7%95%D7%A8%D7%99%D7%AA%D7%9D_%D7%A9%D7%9C_%D7%90%D7%95%D7%A7%D7%9C%D7%99%D7%93%D7%A1)), $`e`$ אי-רציונלי. ידועה הוכחה קצרה לשוויון הזה.[^3] כיוון שהשבר המשולב של $`e`$ אינו [מחזורי](https://he.wikipedia.org/wiki/%D7%A9%D7%91%D7%A8_%D7%9E%D7%A9%D7%95%D7%9C%D7%91_%D7%9E%D7%97%D7%96%D7%95%D7%A8%D7%99), זה מוכיח גם ש-$`e`$ אינו שורש של פולינום ריבועי עם מקדמים רציונליים ([משפט לגראנז'](https://he.wikipedia.org/wiki/%D7%9E%D7%A9%D7%A4%D7%98_%D7%9C%D7%92%D7%A8%D7%90%D7%A0%D7%96%27_%D7%A2%D7%9C_%D7%A9%D7%91%D7%A8%D7%99%D7%9D_%D7%9E%D7%A9%D7%95%D7%9C%D7%91%D7%99%D7%9D)); בפרט, $`e^2`$ אי-רציונלי.

**דוגמה.** בחישוב שלנו, 20 האיברים הראשונים של השבר המשולב הם $`2, 1, 2, 1, 1, 4, 1, 1, 6, 1, 1, 8, 1, 1, 10, 1, 1, 12, 1, 1`$, בהתאם לתבנית. המתכנסים הראשונים:



```math
3,\ \frac83,\ \frac{11}4,\ \frac{19}7,\ \frac{87}{32},\ \frac{106}{39},\ \frac{193}{71},\ \frac{1264}{465},\ \frac{1457}{536},\ \frac{2721}{1001},\ \frac{23225}{8544},\ \ldots
```

 למשל $`2721/1001 = 2.7182817\ldots`$, לעומת $`e = 2.7182818\ldots`$.

## ההוכחה של פורייה

ההוכחה המוכרת ביותר היא [הוכחה בדרך השלילה](https://he.wikipedia.org/wiki/%D7%94%D7%95%D7%9B%D7%97%D7%94_%D7%91%D7%93%D7%A8%D7%9A_%D7%94%D7%A9%D7%9C%D7%99%D7%9C%D7%94) של [ז'וזף פורייה](https://he.wikipedia.org/wiki/%D7%96%27%D7%95%D7%96%D7%A3_%D7%A4%D7%95%D7%A8%D7%99%D7%99%D7%94),[^4] שמבוססת על השוויון



```math
e = \sum_{n=0}^\infty\frac1{n!}.
```

 מניחים ש-$`e`$ רציונלי, מהצורה $`a/b`$. הרעיון הוא לנתח את ההפרש המוגדל (נסמן אותו $`x`$) בין הטור של $`e`$ לבין הסכום החלקי ה-$`b`$-י שלו, שהוא קטן ממש מ-$`e`$. כשבוחרים את מקדם ההגדלה להיות ה[עצרת](https://he.wikipedia.org/wiki/%D7%A2%D7%A6%D7%A8%D7%AA) של $`b`$, השבר $`a/b`$ והסכום החלקי הופכים ל[שלמים](https://he.wikipedia.org/wiki/%D7%9E%D7%A1%D7%A4%D7%A8_%D7%A9%D7%9C%D7%9D), ולכן $`x`$ חייב להיות שלם חיובי. אבל ההתכנסות המהירה של הטור גוררת ש-$`x`$ קטן ממש מ-1. מהסתירה הזו נובע ש-$`e`$ אי-רציונלי.

ההוכחה המפורטת: אם $`e`$ [רציונלי](https://he.wikipedia.org/wiki/%D7%9E%D7%A1%D7%A4%D7%A8_%D7%A8%D7%A6%D7%99%D7%95%D7%A0%D7%9C%D7%99), יש שלמים חיוביים $`a`$ ו-$`b`$ כך ש-$`e = a/b`$. נגדיר



```math
x = b!\left(e - \sum_{n=0}^b\frac1{n!}\right).
```

 לפי ההנחה $`e = a/b`$,



```math
x = b!\left(\frac ab - \sum_{n=0}^b\frac1{n!}\right) = a(b - 1)! - \sum_{n=0}^b\frac{b!}{n!}.
```

 האיבר הראשון שלם, וכל שבר בסכום הוא בעצם שלם, כי $`n \le b`$ בכל איבר. לכן, תחת ההנחה ש-$`e`$ רציונלי, $`x`$ שלם.

נוכיח ש-$`0 \lt x \lt 1`$. ראשית, כדי להראות ש-$`x`$ חיובי ממש, נציב את הטור של $`e`$ בהגדרה של $`x`$:



```math
x = b!\left(\sum_{n=0}^\infty\frac1{n!} - \sum_{n=0}^b\frac1{n!}\right) = \sum_{n=b+1}^\infty\frac{b!}{n!} \gt 0,
```

 כי כל האיברים חיוביים ממש. עכשיו נוכיח ש-$`x \lt 1`$. לכל האיברים עם $`n \ge b + 1`$ יש לנו את ההערכה



```math
\frac{b!}{n!} = \frac1{(b + 1)(b + 2)\cdots\big(b + (n - b)\big)} \le \frac1{(b + 1)^{n-b} },
```

 ואי-השוויון חזק לכל $`n \ge b + 2`$. נחליף את אינדקס הסכימה ל-$`k = n - b`$ ונשתמש בנוסחה ל[טור הנדסי](https://he.wikipedia.org/wiki/%D7%98%D7%95%D7%A8_%D7%94%D7%A0%D7%93%D7%A1%D7%99) אינסופי:



```math
x = \sum_{n=b+1}^\infty\frac{b!}{n!} \lt \sum_{k=1}^\infty\frac1{(b + 1)^k} = \frac1{b + 1}\cdot\frac1{1 - \frac1{b+1} } = \frac1b \le 1.
```

 כיוון שאין שלם בין 0 ל-1 (ממש), הגענו לסתירה, ולכן $`e`$ אי-רציונלי. [מ.ש.ל.](https://he.wikipedia.org/wiki/%D7%9E.%D7%A9.%D7%9C.)

### דוגמה מספרית

הערכים האמיתיים של $`x_b = b!\left(e - \sum_{n\le b}1/n!\right)`$, בחישוב שלנו:

| $`b`$         | 1      | 2      | 3      | 4      | 5      | 6        | 7       | 8            |
|-------------|--------|--------|--------|--------|--------|----------|---------|--------------|
| הסכום החלקי | 2      | 5/2    | 8/3    | 65/24  | 163/60 | 1957/720 | 685/252 | 109601/40320 |
| $`x_b`$       | 0.7183 | 0.4366 | 0.3097 | 0.2388 | 0.1938 | 0.1629   | 0.1404  | 0.1233       |
| $`1/b`$       | 1      | 0.5    | 0.3333 | 0.25   | 0.2    | 0.1667   | 0.1429  | 0.125        |

תמיד $`\frac1{b+1} \lt x_b \lt \frac1b`$, כך ש-$`x_b`$ לעולם אינו שלם. כדי לראות את ההוכחה "בפעולה", נניח בטעות ש-$`e = 19/7`$ (קירוב לא רע: $`19/7 = 2.714\ldots`$). עם $`b = 7`$, הביטוי $`7!\left(\frac{19}7 - \sum_{n\le7}\frac1{n!}\right) = 6!\cdot19 - \sum_{n\le7}\frac{7!}{n!} = 13680 - 13700 = -20`$ הוא שלם, כצפוי – אבל הוא שלילי, בעוד ש-$`x_7 \approx 0.1404`$. לכן $`e \ne 19/7`$; ההוכחה הכללית מראה שאותו דבר קורה לכל $`a/b`$.

## הוכחות אחרות

אפשר לקבל הוכחה נוספת[^5] מהקודמת, בעזרת ההבחנה



```math
(b + 1)x = 1 + \frac1{b + 2} + \frac1{(b + 2)(b + 3)} + \cdots \lt 1 + \frac1{b + 1} + \frac1{(b + 1)(b + 2)} + \cdots = 1 + x,
```

 ואי-השוויון הזה שקול לטענה ש-$`bx \lt 1`$. זה כמובן בלתי אפשרי, כי $`b`$ ו-$`x`$ שלמים חיוביים.

הוכחה נוספת[^6][^7] מתקבלת מהעובדה ש-



```math
\frac1e = e^{-1} = \sum_{n=0}^\infty\frac{(-1)^n}{n!}.
```

 נגדיר $`s_n = \sum_{k=0}^n\frac{(-1)^k}{k!}`$. כיוון שזה [טור מתחלף](https://he.wikipedia.org/wiki/%D7%98%D7%95%D7%A8_%D7%9E%D7%AA%D7%97%D7%9C%D7%A3) עם איברים יורדים,



```math
0 \lt e^{-1} - s_{2n-1} \lt \frac1{(2n)!},
```

 ולכן



```math
0 \lt (2n - 1)!\left(e^{-1} - s_{2n-1}\right) \lt \frac1{2n} \le \frac12
```

 לכל שלם חיובי $`n`$. שימו לב ש-$`(2n - 1)!\,s_{2n-1}`$ תמיד שלם. נניח ש-$`e^{-1}`$ רציונלי, $`e^{-1} = p/q`$ עם $`p, q`$ זרים ו-$`q \ne 0`$. אפשר לבחור $`n`$ כך ש-$`(2n - 1)!\,e^{-1}`$ שלם, למשל $`n \ge (q + 1)/2`$. עבור בחירה כזו, ההפרש בין $`(2n - 1)!\,e^{-1}`$ לבין $`(2n - 1)!\,s_{2n-1}`$ צריך להיות שלם – אבל לפי אי-השוויון שלעיל זה בלתי אפשרי. לכן $`e^{-1}`$ אי-רציונלי, ומכאן ש-$`e`$ אי-רציונלי.

## הכללות

ב-1840 פרסם [ז'וזף ליוביל](https://he.wikipedia.org/wiki/%D7%96%27%D7%95%D7%96%D7%A3_%D7%9C%D7%99%D7%95%D7%91%D7%99%D7%9C) הוכחה לכך ש-$`e^2`$ אי-רציונלי,[^8] ואחריה הוכחה ש-$`e^2`$ אינו שורש של פולינום ממעלה שנייה עם מקדמים רציונליים.[^9] העובדה האחרונה גוררת ש-$`e^4`$ אי-רציונלי. ההוכחות שלו דומות להוכחה של פורייה. ב-1891 הסביר [אדולף הורוויץ](https://he.wikipedia.org/wiki/%D7%90%D7%93%D7%95%D7%9C%D7%A3_%D7%94%D7%95%D7%A8%D7%95%D7%95%D7%99%D7%A5) איך אפשר להוכיח באותו קו רעיוני ש-$`e`$ אינו שורש של פולינום ממעלה שלישית עם מקדמים רציונליים, ומכאן ש-$`e^3`$ אי-רציונלי.[^10] באופן כללי יותר, $`e^q`$ אי-רציונלי לכל $`q`$ רציונלי שונה מאפס.[^11]

[שארל הרמיט](https://he.wikipedia.org/wiki/%D7%A9%D7%90%D7%A8%D7%9C_%D7%94%D7%A8%D7%9E%D7%99%D7%98) הוכיח ב-1873 ש-$`e`$ הוא [מספר טרנסצנדנטי](https://he.wikipedia.org/wiki/%D7%9E%D7%A1%D7%A4%D7%A8_%D7%98%D7%A8%D7%A0%D7%A1%D7%A6%D7%A0%D7%93%D7%A0%D7%98%D7%99), כלומר אינו שורש של שום פולינום עם מקדמים רציונליים; וכך גם $`e^\alpha`$ לכל $`\alpha`$ [אלגברי](https://he.wikipedia.org/wiki/%D7%9E%D7%A1%D7%A4%D7%A8_%D7%90%D7%9C%D7%92%D7%91%D7%A8%D7%99) שונה מאפס ([משפט לינדמן–ויירשטראס](https://he.wikipedia.org/wiki/%D7%9E%D7%A9%D7%A4%D7%98_%D7%9C%D7%99%D7%A0%D7%93%D7%9E%D7%9F%E2%80%93%D7%95%D7%99%D7%99%D7%A8%D7%A9%D7%98%D7%A8%D7%90%D7%A1)).[^12][^13]

## ראו גם

- [מספר טרנסצנדנטי](https://he.wikipedia.org/wiki/%D7%9E%D7%A1%D7%A4%D7%A8_%D7%98%D7%A8%D7%A0%D7%A1%D7%A6%D7%A0%D7%93%D7%A0%D7%98%D7%99)
- [משפט לינדמן–ויירשטראס](https://he.wikipedia.org/wiki/%D7%9E%D7%A9%D7%A4%D7%98_%D7%9C%D7%99%D7%A0%D7%93%D7%9E%D7%9F%E2%80%93%D7%95%D7%99%D7%99%D7%A8%D7%A9%D7%98%D7%A8%D7%90%D7%A1)
- [מידת אי-רציונליות](%D7%9E%D7%99%D7%93%D7%AA%20%D7%90%D7%99-%D7%A8%D7%A6%D7%99%D7%95%D7%A0%D7%9C%D7%99%D7%95%D7%AA.md)

## הערות שוליים



[^1]: <span dir="ltr">L. Euler, De fractionibus continuis dissertatio, Commentarii Academiae Scientiarum Petropolitanae 9 (1744), pp. 98–137; English translation: An essay on continued fractions, Mathematical Systems Theory 18 (1985), pp. 295–398.</span>

[^2]: <span dir="ltr">C. E. Sandifer, How Euler Did It, MAA, 2007, Chapter 32: Who proved e is irrational?, pp. 185–190.</span>

[^3]: <span dir="ltr">H. Cohn, A short proof of the simple continued fraction expansion of e, American Mathematical Monthly 113 (2006), pp. 57–62.</span>

[^4]: <span dir="ltr">J. de Stainville, Mélanges d'Analyse Algébrique et de Géométrie, Veuve Courcier, 1815, pp. 340–341.</span>

[^5]: <span dir="ltr">A. R. G. MacDivitt, Y. Yanagisawa, An elementary proof that e is irrational, The Mathematical Gazette 71 (1987), p. 217.</span>

[^6]: <span dir="ltr">L. L. Penesi, Elementary proof that e is irrational, American Mathematical Monthly 60 (1953), p. 474.</span>

[^7]: <span dir="ltr">T. Apostol, Mathematical Analysis, 2nd ed., Addison-Wesley, 1974.</span>

[^8]: <span dir="ltr">J. Liouville, Sur l'irrationalité du nombre e = 2,718…, J. Math. Pures Appl. 5 (1840), p. 192.</span>

[^9]: <span dir="ltr">J. Liouville, Addition à la note sur l'irrationnalité du nombre e, J. Math. Pures Appl. 5 (1840), pp. 193–194.</span>

[^10]: <span dir="ltr">A. Hurwitz, Über die Kettenbruchentwicklung der Zahl e (1891), in: Mathematische Werke, vol. 2, Birkhäuser, 1933, pp. 129–133.</span>

[^11]: <span dir="ltr">M. Aigner, G. M. Ziegler, Proofs from THE BOOK, 4th ed., Springer, pp. 27–36.</span>

[^12]: <span dir="ltr">C. Hermite, Sur la fonction exponentielle, Comptes rendus de l'Académie des Sciences de Paris 77 (1873), pp. 18–24.</span>

[^13]: בערך האנגלי הניסוח מייחס להרמיט גם את הטענה על $`e^\alpha`$ לכל $`\alpha`$ אלגברי. הרמיט הוכיח את הטרנסצנדנטיות של $`e`$; המקרה הכללי הוא [משפט לינדמן–ויירשטראס](https://he.wikipedia.org/wiki/%D7%9E%D7%A9%D7%A4%D7%98_%D7%9C%D7%99%D7%A0%D7%93%D7%9E%D7%9F%E2%80%93%D7%95%D7%99%D7%99%D7%A8%D7%A9%D7%98%D7%A8%D7%90%D7%A1) (לינדמן 1882, ויירשטראס 1885).


---
**בקורס:** [שיעור 8: משוואות דיופנטיות וסכומי ריבועים](../course/08-%D7%9E%D7%A9%D7%95%D7%95%D7%90%D7%95%D7%AA-%D7%93%D7%99%D7%95%D7%A4%D7%A0%D7%98%D7%99%D7%95%D7%AA.md)


---
קטגוריות: [קירובים דיופנטיים](../categories/%D7%A7%D7%99%D7%A8%D7%95%D7%91%D7%99%D7%9D%20%D7%93%D7%99%D7%95%D7%A4%D7%A0%D7%98%D7%99%D7%99%D7%9D.md) · [הוכחות](../categories/%D7%94%D7%95%D7%9B%D7%97%D7%95%D7%AA.md) · [מספרים אי-רציונליים](../categories/%D7%9E%D7%A1%D7%A4%D7%A8%D7%99%D7%9D%20%D7%90%D7%99-%D7%A8%D7%A6%D7%99%D7%95%D7%A0%D7%9C%D7%99%D7%99%D7%9D.md)


---
<sub>מבוסס על הערך [Proof that e is irrational](https://en.wikipedia.org/wiki/Proof_that_e_is_irrational) בוויקיפדיה האנגלית ([היסטוריית העריכות ומחברים](https://en.wikipedia.org/w/index.php?title=Proof_that_e_is_irrational&action=history)). התוכן מופץ ברישיון [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/), ואפשר להעתיק אותו בחזרה לוויקיפדיה. [קוד הוויקי של הדף](../wiki/%D7%94%D7%95%D7%9B%D7%97%D7%94%20%D7%A9-e%20%D7%90%D7%99-%D7%A8%D7%A6%D7%99%D7%95%D7%A0%D7%9C%D7%99.wiki)</sub>
