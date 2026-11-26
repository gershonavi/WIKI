# פונקציית L אוטומורפית

ב[מתמטיקה](https://he.wikipedia.org/wiki/%D7%9E%D7%AA%D7%9E%D7%98%D7%99%D7%A7%D7%94), **פונקציית L אוטומורפית** היא פונקציה $`L(s,\pi,r)`$ של משתנה [מרוכב](https://he.wikipedia.org/wiki/%D7%9E%D7%A1%D7%A4%D7%A8_%D7%9E%D7%A8%D7%95%D7%9B%D7%91) $`s`$, המתאימה להצגה אוטומורפית $`\pi`$ של חבורה רדוקטיבית $`G`$ מעל שדה גלובלי, ולהצגה מרוכבת סופית-ממדית $`r`$ של [החבורה הדואלית של לנגלנדס](%D7%94%D7%97%D7%91%D7%95%D7%A8%D7%94%20%D7%94%D7%93%D7%95%D7%90%D7%9C%D7%99%D7%AA%20%D7%A9%D7%9C%20%D7%9C%D7%A0%D7%92%D7%9C%D7%A0%D7%93%D7%A1.md) $`{}^LG`$ של $`G`$. פונקציות L אוטומורפיות מכלילות את [טורי ה-L של דיריכלה](https://he.wikipedia.org/wiki/%D7%A4%D7%95%D7%A0%D7%A7%D7%A6%D7%99%D7%99%D7%AA_L_%D7%A9%D7%9C_%D7%93%D7%99%D7%A8%D7%99%D7%9B%D7%9C%D7%94) של [קרקטר דיריכלה](https://he.wikipedia.org/wiki/%D7%A7%D7%A8%D7%A7%D7%98%D7%A8_%D7%93%D7%99%D7%A8%D7%99%D7%9B%D7%9C%D7%94) ואת [התמרת מלין](%D7%94%D7%AA%D7%9E%D7%A8%D7%AA%20%D7%9E%D7%9C%D7%99%D7%9F.md) של [תבנית מודולרית](https://he.wikipedia.org/wiki/%D7%AA%D7%91%D7%A0%D7%99%D7%AA_%D7%9E%D7%95%D7%93%D7%95%D7%9C%D7%A8%D7%99%D7%AA). הן הוצגו על ידי [רוברט לנגלנדס](https://he.wikipedia.org/wiki/%D7%A8%D7%95%D7%91%D7%A8%D7%98_%D7%9C%D7%A0%D7%92%D7%9C%D7%A0%D7%93%D7%A1).[^1]

ארמן בורל,[^2] וכן ג'יימס ארתור וסטיבן גלברט,[^3] כתבו סקירות על פונקציות L אוטומורפיות.

## תכונות

פונקציות L אוטומורפיות תוכננו כך שיהיו להן התכונות הבאות (שהוכחו בחלק מהמקרים, אבל עדיין השערתיות באחרים).

ראשית, פונקציית ה-L $`L(s, \pi, r)`$ צריכה להיות מכפלה (על המקומות $`v`$ של השדה $`F`$) של פונקציות L מקומיות:



```math
L(s, \pi, r) = \prod_v L(s, \pi_v, r_v).
```



כאן ההצגה האוטומורפית $`\pi = \otimes\pi_v`$ היא [מכפלה טנזורית](https://he.wikipedia.org/wiki/%D7%9E%D7%9B%D7%A4%D7%9C%D7%94_%D7%98%D7%A0%D7%96%D7%95%D7%A8%D7%99%D7%AA) של ההצגות $`\pi_v`$ של החבורות המקומיות. במקום לא מסועף $`v`$, ההצגה $`\pi_v`$ מתאימה (לפי איזומורפיזם סאטאקה) למחלקת צמידות $`A_v`$ בחבורה הדואלית, והגורם המקומי הוא $`L(s, \pi_v, r_v) = \det\left(1 - r(A_v)\,q_v^{-s}\right)^{-1}`$, כאשר $`q_v`$ הוא גודל שדה השאריות – הכללה ישירה של גורם אוילר $`(1 - p^{-s})^{-1}`$.

מצפים שלפונקציית ה-L תהיה [המשכה אנליטית](https://he.wikipedia.org/wiki/%D7%94%D7%9E%D7%A9%D7%9B%D7%94_%D7%90%D7%A0%D7%9C%D7%99%D7%98%D7%99%D7%AA) ל[פונקציה מרומורפית](https://he.wikipedia.org/wiki/%D7%A4%D7%95%D7%A0%D7%A7%D7%A6%D7%99%D7%94_%D7%9E%D7%A8%D7%95%D7%9E%D7%95%D7%A8%D7%A4%D7%99%D7%AA) לכל $`s`$ מרוכב, ושהיא תקיים [משוואת פונקציה](%D7%9E%D7%A9%D7%95%D7%95%D7%90%D7%AA%20%D7%94%D7%A4%D7%95%D7%A0%D7%A7%D7%A6%D7%99%D7%94%20%28%D7%A4%D7%95%D7%A0%D7%A7%D7%A6%D7%99%D7%99%D7%AA%20L%29.md)



```math
L(s, \pi, r) = \epsilon(s, \pi, r)\, L(1 - s, \pi, r^\vee),
```



כאשר הגורם $`\epsilon(s, \pi, r)`$ הוא מכפלה של "קבועים מקומיים"



```math
\epsilon(s, \pi, r) = \prod_v \epsilon(s, \pi_v, r_v, \psi_v),
```



שכמעט כולם שווים ל-1 (ראו [הקבוע המקומי של לנגלנדס–דלין](%D7%94%D7%A7%D7%91%D7%95%D7%A2%20%D7%94%D7%9E%D7%A7%D7%95%D7%9E%D7%99%20%D7%A9%D7%9C%20%D7%9C%D7%A0%D7%92%D7%9C%D7%A0%D7%93%D7%A1%E2%80%93%D7%93%D7%9C%D7%99%D7%9F.md)).

## החבורות הליניאריות הכלליות

רוז'ה גודמן ואֵרווה ז'אקה[^4] בנו פונקציות L אוטומורפיות עבור [החבורות הליניאריות הכלליות](https://he.wikipedia.org/wiki/%D7%94%D7%97%D7%91%D7%95%D7%A8%D7%94_%D7%94%D7%9C%D7%99%D7%A0%D7%99%D7%90%D7%A8%D7%99%D7%AA_%D7%94%D7%9B%D7%9C%D7%9C%D7%99%D7%AA) עם $`r`$ ההצגה הסטנדרטית (מה שנקרא [פונקציות L סטנדרטיות](%D7%A4%D7%95%D7%A0%D7%A7%D7%A6%D7%99%D7%99%D7%AA%20L%20%D7%A1%D7%98%D7%A0%D7%93%D7%A8%D7%98%D7%99%D7%AA.md)), ואימתו את ההמשכה האנליטית ואת משוואת הפונקציה שלהן בעזרת הכללה של השיטה שהציג ג'ון טייט ב[עבודת הדוקטורט שלו](%D7%A2%D7%91%D7%95%D7%93%D7%AA%20%D7%94%D7%93%D7%95%D7%A7%D7%98%D7%95%D7%A8%D7%98%20%D7%A9%D7%9C%20%D7%98%D7%99%D7%99%D7%98.md). בכל מקום בתוכנית לנגלנדס מופיעות מכפלות [רנקין–סלברג](%D7%A9%D7%99%D7%98%D7%AA%20%D7%A8%D7%A0%D7%A7%D7%99%D7%9F%E2%80%93%D7%A1%D7%9C%D7%91%D7%A8%D7%92.md) של הצגות של חבורות ליניאריות כלליות. לפונקציות ה-L של רנקין–סלברג המתקבלות יש מספר תכונות אנליטיות, ומשוואת הפונקציה שלהן הוכחה לראשונה בשיטת לנגלנדס–שהידי.

באופן כללי, השערות הפונקטוריאליות של לנגלנדס גוררות שפונקציות L אוטומורפיות של חבורה רדוקטיבית קשירה שוות למכפלות של פונקציות L אוטומורפיות של חבורות ליניאריות כלליות. הוכחה של הפונקטוריאליות של לנגלנדס תוביל גם להבנה מלאה של התכונות האנליטיות של פונקציות L אוטומורפיות.

## ראו גם

- [השערת רימן הגדולה](%D7%94%D7%A9%D7%A2%D7%A8%D7%AA%20%D7%A8%D7%99%D7%9E%D7%9F%20%D7%94%D7%92%D7%93%D7%95%D7%9C%D7%94.md)
- [השערת רמנוג'אן–פטרסון](%D7%94%D7%A9%D7%A2%D7%A8%D7%AA%20%D7%A8%D7%9E%D7%A0%D7%95%D7%92%27%D7%90%D7%9F%E2%80%93%D7%A4%D7%98%D7%A8%D7%A1%D7%95%D7%9F.md)

## לקריאה נוספת

- J. W. Cogdell, H. H. Kim, M. R. Murty, *Lectures on Automorphic L-functions*, Fields Institute Monographs **20**, AMS, 2004
- S. Gelbart, I. Piatetski-Shapiro, S. Rallis, *Explicit Constructions of Automorphic L-Functions*, Lecture Notes in Mathematics **1254**, Springer, 1987
- H. Jacquet, I. I. Piatetski-Shapiro, J. A. Shalika, *Rankin–Selberg convolutions*, American Journal of Mathematics **105** (1983), no. 2, pp. 367–464
- F. Shahidi, *On certain L-functions*, American Journal of Mathematics **103** (1981), no. 2, pp. 297–355

## הערות שוליים



[^1]: R. P. Langlands, *Problems in the theory of automorphic forms* (1970); *Euler Products* (1971); *Letter to André Weil, January 1967* (פורסם 2015)

[^2]: A. Borel, *Automorphic L-functions*, in: Automorphic Forms, Representations and L-functions, Proc. Sympos. Pure Math. **33**, part 2, AMS, 1979, pp. 27–61

[^3]: J. Arthur, S. Gelbart, *Lectures on automorphic L-functions*, in: L-functions and Arithmetic (Durham, 1989), London Math. Soc. Lecture Note Series **153**, Cambridge University Press, 1991, pp. 1–59

[^4]: R. Godement, H. Jacquet, *Zeta Functions of Simple Algebras*, Lecture Notes in Mathematics **260**, Springer, 1972


---
**בקורס:** [שיעור 23: תבניות אוטומורפיות ותוכנית לנגלנדס](../course/23-%D7%AA%D7%95%D7%9B%D7%A0%D7%99%D7%AA-%D7%9C%D7%A0%D7%92%D7%9C%D7%A0%D7%93%D7%A1.md)


---
קטגוריות: [תבניות אוטומורפיות](../categories/%D7%AA%D7%91%D7%A0%D7%99%D7%95%D7%AA%20%D7%90%D7%95%D7%98%D7%95%D7%9E%D7%95%D7%A8%D7%A4%D7%99%D7%95%D7%AA.md) · [תוכנית לנגלנדס](../categories/%D7%AA%D7%95%D7%9B%D7%A0%D7%99%D7%AA%20%D7%9C%D7%A0%D7%92%D7%9C%D7%A0%D7%93%D7%A1.md) · [פונקציות זטא](../categories/%D7%A4%D7%95%D7%A0%D7%A7%D7%A6%D7%99%D7%95%D7%AA%20%D7%96%D7%98%D7%90.md)


---
<sub>מבוסס על הערך [Automorphic L-function](https://en.wikipedia.org/wiki/Automorphic_L-function) בוויקיפדיה האנגלית ([היסטוריית העריכות ומחברים](https://en.wikipedia.org/w/index.php?title=Automorphic_L-function&action=history)). התוכן מופץ ברישיון [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/), ואפשר להעתיק אותו בחזרה לוויקיפדיה. [קוד הוויקי של הדף](../wiki/%D7%A4%D7%95%D7%A0%D7%A7%D7%A6%D7%99%D7%99%D7%AA%20L%20%D7%90%D7%95%D7%98%D7%95%D7%9E%D7%95%D7%A8%D7%A4%D7%99%D7%AA.wiki)</sub>
