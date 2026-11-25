# פונקציית Z

<img src="https://commons.wikimedia.org/wiki/Special:FilePath/Z_function_in_the_complex_plane%2C_-5%2C_5.svg" alt="פונקציית Z במישור המרוכב, בשיטת צביעת תחום." width="320">

<img src="https://commons.wikimedia.org/wiki/Special:FilePath/Z_function_in_the_complex_plane%2C_-40_--_40.svg" alt="פונקציית Z במישור המרוכב, בתחום רחב יותר." width="320">

ב[מתמטיקה](https://he.wikipedia.org/wiki/%D7%9E%D7%AA%D7%9E%D7%98%D7%99%D7%A7%D7%94), **פונקציית Z** (ב[אנגלית](https://he.wikipedia.org/wiki/%D7%90%D7%A0%D7%92%D7%9C%D7%99%D7%AA): Z function) היא [פונקציה](https://he.wikipedia.org/wiki/%D7%A4%D7%95%D7%A0%D7%A7%D7%A6%D7%99%D7%94) המשמשת לחקר [פונקציית זטא של רימן](https://he.wikipedia.org/wiki/%D7%A4%D7%95%D7%A0%D7%A7%D7%A6%D7%99%D7%99%D7%AA_%D7%96%D7%98%D7%90_%D7%A9%D7%9C_%D7%A8%D7%99%D7%9E%D7%9F) לאורך הישר הקריטי, שבו החלק הממשי של הארגומנט הוא חצי. היא נקראת גם **פונקציית Z של רימן-זיגל**, **פונקציית הזטא של רימן-זיגל**, **פונקציית הארדי** ו**פונקציית Z של הארדי**, על שם [גודפרי הרולד הארדי](https://he.wikipedia.org/wiki/%D7%92%D7%95%D7%93%D7%A4%D7%A8%D7%99_%D7%94%D7%A8%D7%95%D7%9C%D7%93_%D7%94%D7%90%D7%A8%D7%93%D7%99). אפשר להגדיר אותה בעזרת פונקציית התטא של רימן-זיגל $`\theta(t)`$ ופונקציית זטא של רימן:



```math
Z(t) = e^{i \theta(t)} \zeta(\tfrac{1}{2} + it).
```



מהמשוואה הפונקציונלית של פונקציית זטא של רימן נובע שפונקציית Z [ממשית](https://he.wikipedia.org/wiki/%D7%9E%D7%A1%D7%A4%D7%A8_%D7%9E%D7%9E%D7%A9%D7%99) עבור ערכים ממשיים של $`t`$. היא [פונקציה זוגית](https://he.wikipedia.org/wiki/%D7%A4%D7%95%D7%A0%D7%A7%D7%A6%D7%99%D7%95%D7%AA_%D7%96%D7%95%D7%92%D7%99%D7%95%D7%AA_%D7%95%D7%90%D7%99-%D7%96%D7%95%D7%92%D7%99%D7%95%D7%AA), ו[אנליטית](https://he.wikipedia.org/wiki/%D7%A4%D7%95%D7%A0%D7%A7%D7%A6%D7%99%D7%94_%D7%90%D7%A0%D7%9C%D7%99%D7%98%D7%99%D7%AA) ממשית עבור ערכים ממשיים. מאחר שפונקציית התטא של רימן-זיגל ופונקציית זטא של רימן [הולומורפיות](https://he.wikipedia.org/wiki/%D7%A4%D7%95%D7%A0%D7%A7%D7%A6%D7%99%D7%94_%D7%94%D7%95%D7%9C%D7%95%D7%9E%D7%95%D7%A8%D7%A4%D7%99%D7%AA) ברצועה הקריטית, שבה החלק המדומה של $`t`$ נמצא בין $`-1/2`$ ל-$`1/2`$, גם פונקציית Z הולומורפית ברצועה זו. יתרה מזו, האפסים הממשיים של $`Z(t)`$ הם בדיוק האפסים של פונקציית זטא על הישר הקריטי, ואפסים מרוכבים של פונקציית Z ברצועה הקריטית שלה מתאימים לאפסים של פונקציית זטא של רימן שאינם על הישר הקריטי.

## נוסחת רימן-זיגל

את חישוב הערך $`Z(t)`$ עבור $`t`$ ממשי, ולכן גם של פונקציית זטא על הישר הקריטי, מזרזת מאוד נוסחת רימן-זיגל:



```math
Z(t) = 2 \sum_{n^2 < t/2\pi} n^{-1/2}\cos(\theta(t)-t \log n) +R(t),
```

 כאשר לאיבר השגיאה $`R(t)`$ יש ביטוי אסימפטוטי מסובך במונחי הפונקציה



```math
\Psi(z) = \frac{\cos 2\pi(z^2-z-1/16)}{\cos 2\pi z}
```

 ונגזרותיה. אם $`u = (\tfrac t {2\pi})^{1/4}`$, ‏$`N=\lfloor u^2 \rfloor`$ ו-$`p = u^2 - N`$, אז



```math
R(t) \sim (-1)^{N-1} \left( \Psi(p)u^{-1} - \frac{1}{96 \pi^2}\Psi^{(3)}(p)u^{-3} + \cdots\right),
```

 כאשר שלוש הנקודות מציינות שאפשר להמשיך לאיברים מסדר גבוה יותר, המסובכים יותר ויותר.

ידועים טורים יעילים נוספים ל-$`Z(t)`$, ובפרט כמה טורים המשתמשים ב[פונקציית גמא הלא שלמה](https://he.wikipedia.org/wiki/%D7%A4%D7%95%D7%A0%D7%A7%D7%A6%D7%99%D7%99%D7%AA_%D7%92%D7%9E%D7%90_%D7%94%D7%9C%D7%90_%D7%A9%D7%9C%D7%9E%D7%94). אם



```math
Q(a, z) = \frac{\Gamma(a,z)}{\Gamma(a)} = \frac 1 {\Gamma(a)} \int_z^\infty u^{a-1} e^{-u} \, du,
```

 אז דוגמה נאה במיוחד היא



```math
Z(t) =2 \Re \left(e^{i \theta(t)} \left(\sum_{n=1}^\infty Q\left(\frac{s}{2},\pi i n^2 \right) - \frac{\pi^{s/2} e^{\pi i s/4} } {s \Gamma\left(\frac{s}{2}\right)} \right) \right).
```



## התנהגות פונקציית Z

ממשפט הישר הקריטי נובע שצפיפות האפסים הממשיים של פונקציית Z היא



```math
\frac{c}{2\pi} \log \frac{t}{2\pi}
```

 עבור קבוע $`c > 5/12`$[^1]. לכן מספר האפסים בקטע בגודל נתון גדל לאט. אם [השערת רימן](https://he.wikipedia.org/wiki/%D7%94%D7%A9%D7%A2%D7%A8%D7%AA_%D7%A8%D7%99%D7%9E%D7%9F) נכונה, כל האפסים ברצועה הקריטית הם אפסים ממשיים, והקבוע $`c`$ שווה ל-1. משערים גם שכל האפסים האלה פשוטים.

### משפט אומגה

בגלל האפסים שלה, פונקציית Z מתנהגת באופן תנודתי. היא גם גדלה לאט, הן בממוצע והן בערכי השיא. לדוגמה, גם בלי השערת רימן מתקיים "משפט האומגה"



```math
Z(t) = \Omega\left( \exp\left(\frac{3}{4}\sqrt{\frac{\log t}{\log \log t} }\right) \right),
```

 כאשר הסימון פירושו שהמנה של $`Z(t)`$ בפונקציה שבתוך $`\Omega`$ אינה שואפת לאפס כאשר $`t`$ גדל.

### גידול ממוצע

גם הגידול הממוצע של פונקציית Z נחקר רבות. את [שורש ממוצע הריבועים](https://he.wikipedia.org/wiki/%D7%A9%D7%95%D7%A8%D7%A9_%D7%9E%D7%9E%D7%95%D7%A6%D7%A2_%D7%94%D7%A8%D7%99%D7%91%D7%95%D7%A2%D7%99%D7%9D) אפשר לקבל מ-



```math
\frac{1}{T} \int_0^T Z(t)^2 dt \sim \log T
```

 או מ-



```math
\frac{1}{T} \int_T^{2T} Z(t)^2 dt \sim \log T,
```

 ומכאן ששורש ממוצע הריבועים של $`Z(t)`$ גדל כמו $`\sqrt{\log t}`$. אפשר לשפר הערכה זו ל-



```math
\frac{1}{T} \int_0^T Z(t)^2 dt = \log T + (2\gamma - 2 \log(2 \pi) -1) + O(T^{-15/22}).
```

 אם מגדילים את המעריך, מקבלים ממוצע התלוי יותר בערכי השיא של $`Z`$. עבור חזקה רביעית:



```math
\frac{1}{T} \int_0^T Z(t)^4 dt \sim \frac{1}{2\pi^2}(\log T)^4,
```

 ומכאן שהשורש הרביעי של ממוצע החזקה הרביעית גדל כמו $`\tfrac{1}{2^{1/4} \sqrt{\pi} } \log t`$.

### השערת לינדלף

*ערך מורחב: [השערת לינדלף](%D7%94%D7%A9%D7%A2%D7%A8%D7%AA%20%D7%9C%D7%99%D7%A0%D7%93%D7%9C%D7%A3.md)* חזקות זוגיות גבוהות יותר נחקרו רבות, אך ידוע פחות על הממוצעים המתאימים. משערים, וזה נובע מהשערת רימן, ש-



```math
\frac{1}{T} \int_0^T Z(t)^{2k} \, dt = o(T^\varepsilon)
```

 לכל $`\varepsilon`$ חיובי. כאן הסימון $`o`$ הקטן פירושו שהמנה של האגף השמאלי באגף הימני *כן* שואפת לאפס; כלומר, $`o`$ הקטן הוא השלילה של $`\Omega`$. השערה זו נקראת [השערת לינדלף](%D7%94%D7%A9%D7%A2%D7%A8%D7%AA%20%D7%9C%D7%99%D7%A0%D7%93%D7%9C%D7%A3.md), והיא חלשה יותר מהשערת רימן. בדרך כלל מנסחים אותה בצורה השקולה



```math
Z(t) = o(t^\varepsilon);
```

 בשתי הצורות היא קובעת שקצב הגידול של ערכי השיא אינו יכול להיות גבוה מדי. החסם הידוע הטוב ביותר על קצב גידול זה אינו חזק: ידוע רק שהוא מתקיים עבור $`\varepsilon`$ הגדול מכ-0.155 (ראו בערך השערת לינדלף). יהיה מפתיע מאוד לגלות שפונקציית Z גדלה בקצב הקרוב לכך. [ליטלווד](https://he.wikipedia.org/wiki/%D7%92%27%D7%95%D7%9F_%D7%90%D7%93%D7%A0%D7%96%D7%95%D7%A8_%D7%9C%D7%99%D7%98%D7%9C%D7%95%D7%95%D7%93) הוכיח שבהנחת השערת רימן



```math
Z(t) = o\left(\exp\left(\frac{10 \log t}{\log \log t}\right)\right),
```

 וזה נראה סביר הרבה יותר.

## ראו גם

- [פונקציית זטא של רימן](https://he.wikipedia.org/wiki/%D7%A4%D7%95%D7%A0%D7%A7%D7%A6%D7%99%D7%99%D7%AA_%D7%96%D7%98%D7%90_%D7%A9%D7%9C_%D7%A8%D7%99%D7%9E%D7%9F)
- [השערת לינדלף](%D7%94%D7%A9%D7%A2%D7%A8%D7%AA%20%D7%9C%D7%99%D7%A0%D7%93%D7%9C%D7%A3.md)
- [השערת רימן](https://he.wikipedia.org/wiki/%D7%94%D7%A9%D7%A2%D7%A8%D7%AA_%D7%A8%D7%99%D7%9E%D7%9F)

## לקריאה נוספת

- H. M. Edwards, *Riemann's zeta function*, Pure and Applied Mathematics 58, Academic Press, New York-London, 1974
- Aleksandar Ivić, *The theory of Hardy's Z-function*, Cambridge Tracts in Mathematics 196, Cambridge University Press, 2013
- R. B. Paris, D. Kaminski, *Asymptotics and Mellin-Barnes Integrals*, Encyclopedia of Mathematics and Its Applications 85, Cambridge University Press, 2001
- K. Ramachandra, *Lectures on the mean-value and Omega-theorems for the Riemann Zeta-function*, Tata Institute of Fundamental Research, Springer-Verlag, 1996
- E. C. Titchmarsh, *The Theory of the Riemann Zeta-Function*, 2nd ed., ed. D. R. Heath-Brown, Oxford University Press, 1986

## קישורים חיצוניים

- (באנגלית) [Riemann–Siegel Functions](https://mathworld.wolfram.com/Riemann-SiegelFunctions.html), באתר MathWorld
- (באנגלית) [Riemann-Siegel function Z](http://functions.wolfram.com/ZetaFunctionsandPolylogarithms/RiemannSiegelZ/), Wolfram Research

## הערות שוליים



[^1]: Kyle Pratt, Nicolas Robles, Alexandru Zaharescu, Dirk Zeindler, *More than five-twelfths of the zeros of ζ are on the critical line*, 2018, [arXiv:1802.10521](https://arxiv.org/abs/1802.10521)


---
קטגוריות: פונקציות זטא · תורת המספרים האנליטית


---
<sub>מבוסס על הערך [Z function](https://en.wikipedia.org/wiki/Z_function) בוויקיפדיה האנגלית ([היסטוריית העריכות ומחברים](https://en.wikipedia.org/w/index.php?title=Z_function&action=history)). התוכן מופץ ברישיון [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/), ואפשר להעתיק אותו בחזרה לוויקיפדיה. [קוד הוויקי של הדף](../wiki/%D7%A4%D7%95%D7%A0%D7%A7%D7%A6%D7%99%D7%99%D7%AA%20Z.wiki)</sub>
