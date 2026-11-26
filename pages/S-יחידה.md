# S-יחידה

ב[מתמטיקה](https://he.wikipedia.org/wiki/%D7%9E%D7%AA%D7%9E%D7%98%D7%99%D7%A7%D7%94), בתחום [תורת המספרים האלגברית](https://he.wikipedia.org/wiki/%D7%AA%D7%95%D7%A8%D7%AA_%D7%94%D7%9E%D7%A1%D7%A4%D7%A8%D7%99%D7%9D_%D7%94%D7%90%D7%9C%D7%92%D7%91%D7%A8%D7%99%D7%AA), **S-יחידה** היא הכללה של המושג [יחידה](https://he.wikipedia.org/wiki/%D7%94%D7%A4%D7%99%D7%9A_%28%D7%9E%D7%AA%D7%9E%D7%98%D7%99%D7%A7%D7%94%29) של [חוג השלמים](https://he.wikipedia.org/wiki/%D7%97%D7%95%D7%92_%D7%94%D7%A9%D7%9C%D7%9E%D7%99%D7%9D) של שדה. רבות מהתוצאות שנכונות ליחידות נכונות גם ל-S-יחידות.

## הגדרה

יהי $`K`$ [שדה מספרים](https://he.wikipedia.org/wiki/%D7%A9%D7%93%D7%94_%D7%9E%D7%A1%D7%A4%D7%A8%D7%99%D7%9D) עם חוג שלמים $`R`$, ותהי $`S`$ קבוצה סופית של [אידיאלים ראשוניים](https://he.wikipedia.org/wiki/%D7%90%D7%99%D7%93%D7%99%D7%90%D7%9C_%D7%A8%D7%90%D7%A9%D7%95%D7%A0%D7%99) של $`R`$. איבר $`x`$ של $`K`$ הוא **S-יחידה** אם ה[אידיאל השבור](%D7%90%D7%99%D7%93%D7%99%D7%90%D7%9C%20%D7%A9%D7%91%D7%95%D7%A8.md) הראשי $`(x)`$ הוא מכפלה של ראשוניים מ-$`S`$ (בחזקות חיוביות או שליליות). בחוג השלמים הרגילים $`\mathbb Z`$ אפשר לקחת את $`S`$ כקבוצה סופית של [מספרים ראשוניים](https://he.wikipedia.org/wiki/%D7%9E%D7%A1%D7%A4%D7%A8_%D7%A8%D7%90%D7%A9%D7%95%D7%A0%D7%99), ולהגדיר S-יחידה כ[מספר רציונלי](https://he.wikipedia.org/wiki/%D7%9E%D7%A1%D7%A4%D7%A8_%D7%A8%D7%A6%D7%99%D7%95%D7%A0%D7%9C%D7%99) שהמונה והמכנה שלו מתחלקים רק בראשוניים מ-$`S`$.

**דוגמאות.**

- ב-$`\mathbb Q`$ עם $`S = \{2, 3\}`$, ה-S-יחידות הן המספרים $`\pm 2^a 3^b`$ עם $`a, b \in \mathbb Z`$, למשל $`-\tfrac{8}{9}`$, $`\tfrac{3}{2}`$, $`6`$. אלה בדיוק האיברים ההפיכים של החוג $`\mathbb Z[\tfrac16]`$.
- ב-$`K = \mathbb Q(\sqrt2)`$ עם $`S = \{(\sqrt2)\}`$ (הראשוני היחיד מעל 2, $`2 = (\sqrt2)^2`$), ה-S-יחידות הן $`\pm(1+\sqrt2)^m(\sqrt2)^n`$ עם $`m, n \in \mathbb Z`$.

## תכונות

ה-S-יחידות יוצרות [חבורה](https://he.wikipedia.org/wiki/%D7%97%D7%91%D7%95%D7%A8%D7%94_%28%D7%9E%D7%91%D7%A0%D7%94_%D7%90%D7%9C%D7%92%D7%91%D7%A8%D7%99%29) כפלית שמכילה את היחידות של $`R`$.

[משפט היחידות של דיריכלה](https://he.wikipedia.org/wiki/%D7%9E%D7%A9%D7%A4%D7%98_%D7%94%D7%99%D7%97%D7%99%D7%93%D7%95%D7%AA_%D7%A9%D7%9C_%D7%93%D7%99%D7%A8%D7%99%D7%9B%D7%9C%D7%94) נכון גם ל-S-יחידות: חבורת ה-S-יחידות [נוצרת סופית](https://he.wikipedia.org/wiki/%D7%97%D7%91%D7%95%D7%A8%D7%94_%D7%90%D7%91%D7%9C%D7%99%D7%AA_%D7%A0%D7%95%D7%A6%D7%A8%D7%AA_%D7%A1%D7%95%D7%A4%D7%99%D7%AA), וה[דרגה](https://he.wikipedia.org/wiki/%D7%93%D7%A8%D7%92%D7%94_%D7%A9%D7%9C_%D7%97%D7%91%D7%95%D7%A8%D7%94_%D7%90%D7%91%D7%9C%D7%99%D7%AA) שלה (המספר המקסימלי של איברים בלתי תלויים כפלית) היא $`r + s`$, כאשר $`r`$ הדרגה של חבורת היחידות ו-$`s = |S|`$. הסיבה: לכל $`\mathfrak p \in S`$ ההעתקה $`x \mapsto v_{\mathfrak p}(x)`$ נותנת הומומורפיזם לחבורה $`\mathbb Z^s`$, שהגרעין שלו הוא חבורת היחידות; והתמונה שלו מאינדקס סופי, כי לכל $`\mathfrak p`$ החזקה $`\mathfrak p^h`$ (כאשר $`h`$ [מספר המחלקות](https://he.wikipedia.org/wiki/%D7%9E%D7%A1%D7%A4%D7%A8_%D7%94%D7%9E%D7%97%D7%9C%D7%A7%D7%95%D7%AA)) ראשית.

בדוגמאות שלמעלה: ב-$`\mathbb Q`$, $`r = 0`$ ו-$`s = 2`$, והחבורה $`\{\pm 2^a3^b\} \cong \{\pm1\}\times\mathbb Z^2`$ מדרגה 2. ב-$`\mathbb Q(\sqrt2)`$, $`r = 1`$ ו-$`s = 1`$, והדרגה היא 2, עם יוצרים $`1+\sqrt2`$ ו-$`\sqrt2`$.

## משוואת ה-S-יחידות

**משוואת ה-S-יחידות** היא ה[משוואה דיופנטית](https://he.wikipedia.org/wiki/%D7%9E%D7%A9%D7%95%D7%95%D7%90%D7%94_%D7%93%D7%99%D7%95%D7%A4%D7%A0%D7%98%D7%99%D7%AA)



```math
u + v = 1,
```

 כאשר $`u`$ ו-$`v`$ מוגבלים להיות S-יחידות של $`K`$ (או, באופן כללי יותר, איברים של תת-חבורה נוצרת סופית של החבורה הכפלית של שדה כלשהו ממאפיין 0). מספר הפתרונות של המשוואה סופי,[^1] ואפשר למצוא את הפתרונות באופן אפקטיבי בעזרת הערכות על [צורות לינאריות בלוגריתמים](https://he.wikipedia.org/wiki/%D7%A6%D7%95%D7%A8%D7%94_%D7%9C%D7%99%D7%A0%D7%90%D7%A8%D7%99%D7%AA_%D7%91%D7%9C%D7%95%D7%92%D7%A8%D7%99%D7%AA%D7%9E%D7%99%D7%9D), כפי שפותחו ב[תורת המספרים הטרנסצנדנטיים](%D7%AA%D7%95%D7%A8%D7%AA%20%D7%94%D7%9E%D7%A1%D7%A4%D7%A8%D7%99%D7%9D%20%D7%94%D7%98%D7%A8%D7%A0%D7%A1%D7%A6%D7%A0%D7%93%D7%A0%D7%98%D7%99%D7%99%D7%9D.md). מגוון רחב של משוואות דיופנטיות ניתן, עקרונית, לרדוקציה לצורה כלשהי של משוואת ה-S-יחידות. דוגמה בולטת היא [משפט זיגל](%D7%9E%D7%A9%D7%A4%D7%98%20%D7%96%D7%99%D7%92%D7%9C%20%D7%A2%D7%9C%20%D7%A0%D7%A7%D7%95%D7%93%D7%95%D7%AA%20%D7%A9%D7%9C%D7%9E%D7%95%D7%AA.md) על נקודות שלמות על [עקומים אליפטיים](https://he.wikipedia.org/wiki/%D7%A2%D7%A7%D7%95%D7%9D_%D7%90%D7%9C%D7%99%D7%A4%D7%98%D7%99), ובאופן כללי יותר על עקומים סופר-אליפטיים מהצורה $`y^n = f(x)`$.

**דוגמה מחושבת: $`S = \{2, 3\}`$ מעל $`\mathbb Q`$.** נחפש את כל הפתרונות של $`u + v = 1`$ עם $`u, v \in \{\pm 2^a 3^b\}`$. אחרי הכפלה במכנה משותף זו בעיית מציאת כל השוויונות $`x + y = z`$ בשלמים זרים מהצורה $`\pm 2^a3^b`$. השוויונות היסודיים הם



```math
1 + 1 = 2, \quad 1 + 2 = 3, \quad 1 + 3 = 4, \quad 1 + 8 = 9,
```

 וכל אחד מהם נותן כמה פתרונות של $`u + v = 1`$, לפי איזה מהאיברים מעבירים לאגף ימין ובאיזה מחלקים. למשל מ-$`1 + 8 = 9`$ מתקבלים



```math
\tfrac19 + \tfrac89 = 1, \qquad 9 + (-8) = 1, \qquad \tfrac98 + \left(-\tfrac18\right) = 1
```

 (ועוד שלושה מהחלפת הסדר של $`u`$ ו-$`v`$). בסך הכול יש בדיוק 21 זוגות סדורים $`(u, v)`$; חיפוש ממוחשב על כל המעריכים בטווח $`|a|, |b| \le 40`$ מוצא בדיוק אותם, והגבולות האפקטיביים מבטיחים שאין פתרונות נוספים. הפתרון "הגדול" ביותר, $`9 - 8 = 1`$, הוא המקרה המפורסם של [השערת קטלן](https://he.wikipedia.org/wiki/%D7%94%D7%A9%D7%A2%D7%A8%D7%AA_%D7%A7%D7%98%D7%9C%D7%9F) ($`3^2 - 2^3 = 1`$).

פותר ממוחשב למשוואת ה-S-יחידות זמין בתוכנה [SageMath](https://he.wikipedia.org/wiki/SageMath).

## לקריאה נוספת

- G. Everest, A. van der Poorten, I. Shparlinski, T. Ward, *Recurrence Sequences*, Mathematical Surveys and Monographs **104**, AMS, 2003, pp. 19–22
- S. Lang, *Elliptic Curves: Diophantine Analysis*, Grundlehren **231**, Springer, 1978, pp. 128–153
- S. Lang, *Algebraic Number Theory*, Springer, 1986, Chap. V
- N. Smart, *The Algorithmic Resolution of Diophantine Equations*, LMS Student Texts **41**, Cambridge University Press, 1998, Chap. 9
- J. Neukirch, *Class Field Theory*, Grundlehren **280**, Springer, 1986, pp. 72–73
- A. Baker, G. Wüstholz, *Logarithmic Forms and Diophantine Geometry*, Cambridge University Press, 2007
- E. Bombieri, W. Gubler, *Heights in Diophantine Geometry*, Cambridge University Press, 2006

## הערות שוליים



[^1]: F. Beukers, H. P. Schlickewei, *The equation x+y=1 in finitely generated groups*, Acta Arithmetica **78** (1996), pp. 189–199


---
**בקורס:** [שיעור 19: תורת המספרים האלגברית: שדות מספרים, אידיאלים וחבורת המחלקות](../course/19-%D7%AA%D7%95%D7%A8%D7%AA-%D7%94%D7%9E%D7%A1%D7%A4%D7%A8%D7%99%D7%9D-%D7%94%D7%90%D7%9C%D7%92%D7%91%D7%A8%D7%99%D7%AA.md)


---
קטגוריות: [תורת המספרים האלגברית](../categories/%D7%AA%D7%95%D7%A8%D7%AA%20%D7%94%D7%9E%D7%A1%D7%A4%D7%A8%D7%99%D7%9D%20%D7%94%D7%90%D7%9C%D7%92%D7%91%D7%A8%D7%99%D7%AA.md) · [משוואות דיופנטיות](../categories/%D7%9E%D7%A9%D7%95%D7%95%D7%90%D7%95%D7%AA%20%D7%93%D7%99%D7%95%D7%A4%D7%A0%D7%98%D7%99%D7%95%D7%AA.md)


---
<sub>מבוסס על הערך [S-unit](https://en.wikipedia.org/wiki/S-unit) בוויקיפדיה האנגלית ([היסטוריית העריכות ומחברים](https://en.wikipedia.org/w/index.php?title=S-unit&action=history)). התוכן מופץ ברישיון [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/), ואפשר להעתיק אותו בחזרה לוויקיפדיה. [קוד הוויקי של הדף](../wiki/S-%D7%99%D7%97%D7%99%D7%93%D7%94.wiki)</sub>
