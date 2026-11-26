# פונקציית L סטנדרטית

ב[מתמטיקה](https://he.wikipedia.org/wiki/%D7%9E%D7%AA%D7%9E%D7%98%D7%99%D7%A7%D7%94), המונח **פונקציית L סטנדרטית** מתייחס לסוג מסוים של פונקציית L אוטומורפית שתיאר [רוברט לנגלנדס](https://he.wikipedia.org/wiki/%D7%A8%D7%95%D7%91%D7%A8%D7%98_%D7%9C%D7%A0%D7%92%D7%9C%D7%A0%D7%93%D7%A1).[^1][^2] כאן "סטנדרטית" פירושו שההצגה הסופית-ממדית $`r`$ שבה משתמשים בהגדרת פונקציית ה-L היא ההצגה הסטנדרטית של החבורה הדואלית של לנגלנדס (חבורת ה-L) כחבורת מטריצות.

עבור $`\mathrm{GL}(n)`$, החבורה הדואלית היא שוב $`\mathrm{GL}(n, \mathbb C)`$, וההצגה הסטנדרטית היא הפעולה על $`\mathbb C^n`$. אם להצגה האוטומורפית $`\pi = \bigotimes_v \pi_v`$ יש בראשוני $`p`$ לא מסועף "פרמטרי סטאקה" $`\alpha_{1,p}, \ldots, \alpha_{n,p}`$, אז פונקציית ה-L הסטנדרטית שלה היא



```math
L(s, \pi) = \prod_p \prod_{i=1}^n \left(1 - \alpha_{i,p}\,p^{-s}\right)^{-1}
```



(ועוד גורמים בראשוניים המסועפים ובאינסוף). עבור $`n = 1`$ והצגה טריוויאלית מקבלים את [פונקציית זטא של רימן](https://he.wikipedia.org/wiki/%D7%A4%D7%95%D7%A0%D7%A7%D7%A6%D7%99%D7%99%D7%AA_%D7%96%D7%98%D7%90_%D7%A9%D7%9C_%D7%A8%D7%99%D7%9E%D7%9F); עבור $`n = 1`$ כללי – [פונקציות L של דיריכלה](https://he.wikipedia.org/wiki/%D7%A4%D7%95%D7%A0%D7%A7%D7%A6%D7%99%D7%99%D7%AA_L_%D7%A9%D7%9C_%D7%93%D7%99%D7%A8%D7%99%D7%9B%D7%9C%D7%94) (ושל הקה); ועבור $`n = 2`$ – את פונקציות ה-L של [תבניות מודולריות](https://he.wikipedia.org/wiki/%D7%AA%D7%91%D7%A0%D7%99%D7%AA_%D7%9E%D7%95%D7%93%D7%95%D7%9C%D7%A8%D7%99%D7%AA) עצמיות, כמו פונקציית ה-L של רמנוג'אן (ראו [השערת רמנוג'אן–פטרסון](%D7%94%D7%A9%D7%A2%D7%A8%D7%AA%20%D7%A8%D7%9E%D7%A0%D7%95%D7%92%27%D7%90%D7%9F%E2%80%93%D7%A4%D7%98%D7%A8%D7%A1%D7%95%D7%9F.md)).

## קשר לפונקציות L אחרות

משערים שפונקציות L סטנדרטיות הן הסוג הכללי ביותר של [פונקציות L](https://he.wikipedia.org/wiki/%D7%A4%D7%95%D7%A0%D7%A7%D7%A6%D7%99%D7%99%D7%AA_L). לפי ההשערה, הן כוללות את כל הדוגמאות של פונקציות L, ובפרט צפוי שהן יתלכדו עם **מחלקת סלברג**. יתרה מזו, מקובל להאמין שכל פונקציות ה-L מעל [שדות מספרים](https://he.wikipedia.org/wiki/%D7%A9%D7%93%D7%94_%D7%9E%D7%A1%D7%A4%D7%A8%D7%99%D7%9D) כלשהם הן מקרים של פונקציות L סטנדרטיות עבור [החבורה הליניארית הכללית](https://he.wikipedia.org/wiki/%D7%94%D7%97%D7%91%D7%95%D7%A8%D7%94_%D7%94%D7%9C%D7%99%D7%A0%D7%99%D7%90%D7%A8%D7%99%D7%AA_%D7%94%D7%9B%D7%9C%D7%9C%D7%99%D7%AA) $`\mathrm{GL}(n)`$ מעל המספרים הרציונליים $`\mathbb Q`$. זה הופך אותן לשדה ניסוי שימושי לטענות על פונקציות L, כי לעיתים זה מאפשר להשתמש במבנה שבא מתורת ה[תבניות האוטומורפיות](https://he.wikipedia.org/wiki/%D7%AA%D7%91%D7%A0%D7%99%D7%AA_%D7%90%D7%95%D7%98%D7%95%D7%9E%D7%95%D7%A8%D7%A4%D7%99%D7%AA).

## תכונות אנליטיות

רוז'ה גודמן ואֵרווה ז'אקה הוכיחו שעבור הצגות חודיות של $`\mathrm{GL}(n)`$ פונקציות ה-L האלה הן תמיד [שלמות](https://he.wikipedia.org/wiki/%D7%A4%D7%95%D7%A0%D7%A7%D7%A6%D7%99%D7%94_%D7%A9%D7%9C%D7%9E%D7%94),[^3] פרט ל[פונקציית זטא של רימן](https://he.wikipedia.org/wiki/%D7%A4%D7%95%D7%A0%D7%A7%D7%A6%D7%99%D7%99%D7%AA_%D7%96%D7%98%D7%90_%D7%A9%D7%9C_%D7%A8%D7%99%D7%9E%D7%9F) (והזזות שלה), שמתקבלת עבור $`n = 1`$. ההוכחה שלהם היא הכללה של [עבודת הדוקטורט של טייט](%D7%A2%D7%91%D7%95%D7%93%D7%AA%20%D7%94%D7%93%D7%95%D7%A7%D7%98%D7%95%D7%A8%D7%98%20%D7%A9%D7%9C%20%D7%98%D7%99%D7%99%D7%98.md). הוכחה אחרת ניתנה מאוחר יותר על ידי פרידון שהידי, בשיטת לנגלנדס–שהידי. לדיון רחב יותר ראו את הספר של גלברט ושהידי.[^4]

## ראו גם

- [פונקציית זטא](https://he.wikipedia.org/wiki/%D7%A4%D7%95%D7%A0%D7%A7%D7%A6%D7%99%D7%99%D7%AA_%D7%96%D7%98%D7%90)
- [שיטת רנקין–סלברג](%D7%A9%D7%99%D7%98%D7%AA%20%D7%A8%D7%A0%D7%A7%D7%99%D7%9F%E2%80%93%D7%A1%D7%9C%D7%91%D7%A8%D7%92.md)

## הערות שוליים



[^1]: R. P. Langlands, [L-functions and automorphic representations](http://publications.ias.edu/sites/default/files/lfunct-ps.pdf), Proceedings of the International Congress of Mathematicians (Helsinki, 1978)

[^2]: A. Borel, *Automorphic L-functions*, in: Automorphic Forms, Representations and L-functions (Corvallis, 1977), Part 2, Proc. Sympos. Pure Math. **33**, AMS, 1979, pp. 27–61

[^3]: R. Godement, H. Jacquet, *Zeta Functions of Simple Algebras*, Lecture Notes in Mathematics **260**, Springer, 1972

[^4]: S. Gelbart, F. Shahidi, *Analytic Properties of Automorphic L-functions*, Perspectives in Mathematics **6**, Academic Press, 1988


---
**בקורס:** [שיעור 23: תבניות אוטומורפיות ותוכנית לנגלנדס](../course/23-%D7%AA%D7%95%D7%9B%D7%A0%D7%99%D7%AA-%D7%9C%D7%A0%D7%92%D7%9C%D7%A0%D7%93%D7%A1.md)


---
קטגוריות: [פונקציות זטא](../categories/%D7%A4%D7%95%D7%A0%D7%A7%D7%A6%D7%99%D7%95%D7%AA%20%D7%96%D7%98%D7%90.md)


---
<sub>מבוסס על הערך [Standard L-function](https://en.wikipedia.org/wiki/Standard_L-function) בוויקיפדיה האנגלית ([היסטוריית העריכות ומחברים](https://en.wikipedia.org/w/index.php?title=Standard_L-function&action=history)). התוכן מופץ ברישיון [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/), ואפשר להעתיק אותו בחזרה לוויקיפדיה. [קוד הוויקי של הדף](../wiki/%D7%A4%D7%95%D7%A0%D7%A7%D7%A6%D7%99%D7%99%D7%AA%20L%20%D7%A1%D7%98%D7%A0%D7%93%D7%A8%D7%98%D7%99%D7%AA.wiki)</sub>
