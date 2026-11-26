# ערכים מיוחדים של פונקציות L

ב[מתמטיקה](https://he.wikipedia.org/wiki/%D7%9E%D7%AA%D7%9E%D7%98%D7%99%D7%A7%D7%94), חקר **הערכים המיוחדים של פונקציות L** הוא תת-תחום של [תורת המספרים](https://he.wikipedia.org/wiki/%D7%AA%D7%95%D7%A8%D7%AA_%D7%94%D7%9E%D7%A1%D7%A4%D7%A8%D7%99%D7%9D) שמוקדש להכללת נוסחאות כמו נוסחת לייבניץ עבור $`\pi`$:



```math
1 - \frac{1}{3} + \frac{1}{5} - \frac{1}{7} + \frac{1}{9} - \cdots = \frac{\pi}{4},
```



מתוך ההבנה שאגף שמאל שווה ל-$`L(1)`$, כאשר $`L(s)`$ היא [פונקציית L של דיריכלה](https://he.wikipedia.org/wiki/%D7%A4%D7%95%D7%A0%D7%A7%D7%A6%D7%99%D7%99%D7%AA_L_%D7%A9%D7%9C_%D7%93%D7%99%D7%A8%D7%99%D7%9B%D7%9C%D7%94) של הקרקטר הריבועי שמתאים לשדה המספרים הרציונליים של גאוס $`\mathbb Q(i)`$. אגף ימין נובע אז מנוסחת מספר המחלקות: עבור שדה ריבועי מדומה עם דיסקרימיננטה $`d`$, מספר מחלקות $`h`$ ו-$`w`$ שורשי יחידה,



```math
L(1, \chi_d) = \frac{2\pi h}{w\sqrt{|d|} },
```



ועבור $`\mathbb Q(i)`$, שבו $`h = 1`$, $`w = 4`$ (השורשים $`\pm1, \pm i`$) ו-$`d = -4`$, מקבלים $`\frac{2\pi}{4\cdot 2} = \frac{\pi}{4}`$. (בערך האנגלי נאמר שהגורם $`\tfrac14`$ מופיע "כי לשדה של גאוס מספר מחלקות 1 והוא מכיל ארבעה שורשי יחידה"; הנוסחה המלאה מראה שגם הדיסקרימיננטה והגורם $`2\pi`$ משתתפים.)

## השערות

יש שתי משפחות של השערות, שמנוסחות עבור מחלקות כלליות של [פונקציות L](https://he.wikipedia.org/wiki/%D7%A4%D7%95%D7%A0%D7%A7%D7%A6%D7%99%D7%99%D7%AA_L) (המסגרת הכללית ביותר היא של פונקציות L המתאימות למוטיבים של צ'או מעל [שדות מספרים](https://he.wikipedia.org/wiki/%D7%A9%D7%93%D7%94_%D7%9E%D7%A1%D7%A4%D7%A8%D7%99%D7%9D)). החלוקה לשתיים משקפת את השאלות:

- (א) במה להחליף את $`\pi`$ שבנוסחת לייבניץ – באיזה מספר "טרנסצנדנטי" אחר (בלי קשר לשאלה אם [תורת המספרים הטרנסצנדנטיים](%D7%AA%D7%95%D7%A8%D7%AA%20%D7%94%D7%9E%D7%A1%D7%A4%D7%A8%D7%99%D7%9D%20%D7%94%D7%98%D7%A8%D7%A0%D7%A1%D7%A6%D7%A0%D7%93%D7%A0%D7%98%D7%99%D7%99%D7%9D.md) יכולה כיום להוכיח שהוא טרנסצנדנטי); ו
- (ב) איך להכליל את הגורם הרציונלי שבנוסחה (מספר המחלקות חלקי מספר שורשי היחידה), על ידי בנייה אלגברית של מספר רציונלי שייצג את היחס בין הערך של פונקציית ה-L לבין הגורם ה"טרנסצנדנטי".

הסברים משלימים ניתנים לגבי הערכים השלמים $`n`$ שעבורם אפשר לצפות לנוסחאות מהסוג הזה עבור $`L(n)`$. (דוגמה קלאסית: $`\zeta(2n) \in \pi^{2n}\mathbb Q`$ לכל $`n \ge 1`$, ואילו על $`\zeta(3), \zeta(5), \ldots`$ לא ידועה נוסחה כזו.)

ההשערות מסוג (א) נקראות **השערות בלינסון**, על שם אלכסנדר בלינסון.[^1][^2] הרעיון הוא להפשיט מהרגולטור של שדה מספרים ל"רגולטור גבוה" (רגולטור בלינסון), דטרמיננטה שנבנית על מרחב וקטורי ממשי שבא מתורת K האלגברית.

ההשערות מסוג (ב) נקראות **השערות בלוך–קאטו לערכים מיוחדים** (על שם ספנסר בלוך וקזויה קאטו; מעגל הרעיונות הזה שונה מ"השערת בלוך–קאטו" של תורת K, שמרחיבה את השערת מילנור, ושהוכחתה הוכרזה ב-2009). הן נקראות גם **השערת מספרי טמגאווה**, שם שבא מ[השערת בירץ' וסווינרטון-דייר](https://he.wikipedia.org/wiki/%D7%94%D7%A9%D7%A2%D7%A8%D7%AA_%D7%91%D7%99%D7%A8%D7%A5%27_%D7%95%D7%A1%D7%95%D7%95%D7%99%D7%A0%D7%A8%D7%98%D7%95%D7%9F-%D7%93%D7%99%D7%99%D7%A8) ומהניסוח שלה כמקבילה, עבור [עקומים אליפטיים](https://he.wikipedia.org/wiki/%D7%A2%D7%A7%D7%95%D7%9D_%D7%90%D7%9C%D7%99%D7%A4%D7%98%D7%99), לבעיית מספרי טמגאווה של חבורות אלגבריות ליניאריות.[^3] בהרחבה נוספת נוסחה **השערת מספרי טמגאווה האקוויווריאנטית** (ETNC), כדי לחזק את הקשר בין הרעיונות האלה לבין תורת איוואסאווה ו"ההשערה הראשית" שלה.

### המצב הנוכחי

כל ההשערות האלה ידועות כנכונות רק במקרים מיוחדים.

## ראו גם

- [השערת ברומר–סטארק](%D7%94%D7%A9%D7%A2%D7%A8%D7%AA%20%D7%91%D7%A8%D7%95%D7%9E%D7%A8%E2%80%93%D7%A1%D7%98%D7%90%D7%A8%D7%A7.md)
- [משפט בראואר-זיגל](%D7%9E%D7%A9%D7%A4%D7%98%20%D7%91%D7%A8%D7%90%D7%95%D7%90%D7%A8-%D7%96%D7%99%D7%92%D7%9C.md)

## לקריאה נוספת

- G. Kings, *The Bloch–Kato conjecture on special values of L-functions. A survey of known results*, Journal de Théorie des Nombres de Bordeaux **15** (2003), no. 1, pp. 179–198
- R. J. Mathar, *Table of Dirichlet L-series and prime zeta modulo functions for small moduli*, arXiv:1008.2547 (2010)
- Encyclopedia of Mathematics: "Beilinson conjectures"; "K-functor in algebraic geometry"

## קישורים חיצוניים

- [L-Funktionen und die Vermutungen von Deligne und Beilinson](http://www.mpg.de/459553/L-Funktionen_gesamt.pdf) (בגרמנית)

## הערות שוליים



[^1]: P. Schneider, [Introduction to the Beilinson Conjectures](http://wwwmath.uni-muenster.de/u/pschnei/publ/beilinson-volume/Schneider.pdf)

[^2]: J. Nekovář, [Beilinson's Conjectures](http://webusers.imj-prg.fr/~jan.nekovar/pu/mot.pdf)

[^3]: M. Flach, [The Tamagawa Number Conjecture](http://www.dpmms.cam.ac.uk/Seminars/Kuwait/abstracts/L56.pdf)


---
**בקורס:** [שיעור 13: קרקטרים של דיריכלה ופונקציות L](../course/13-%D7%A7%D7%A8%D7%A7%D7%98%D7%A8%D7%99%D7%9D-%D7%95%D7%A4%D7%95%D7%A0%D7%A7%D7%A6%D7%99%D7%95%D7%AA-L.md)


---
קטגוריות: [פונקציות זטא](../categories/%D7%A4%D7%95%D7%A0%D7%A7%D7%A6%D7%99%D7%95%D7%AA%20%D7%96%D7%98%D7%90.md)


---
<sub>מבוסס על הערך [Special values of L-functions](https://en.wikipedia.org/wiki/Special_values_of_L-functions) בוויקיפדיה האנגלית ([היסטוריית העריכות ומחברים](https://en.wikipedia.org/w/index.php?title=Special_values_of_L-functions&action=history)). התוכן מופץ ברישיון [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/), ואפשר להעתיק אותו בחזרה לוויקיפדיה. [קוד הוויקי של הדף](../wiki/%D7%A2%D7%A8%D7%9B%D7%99%D7%9D%20%D7%9E%D7%99%D7%95%D7%97%D7%93%D7%99%D7%9D%20%D7%A9%D7%9C%20%D7%A4%D7%95%D7%A0%D7%A7%D7%A6%D7%99%D7%95%D7%AA%20L.wiki)</sub>
