# נוסחאות מפורשות לפונקציות L

ב[מתמטיקה](https://he.wikipedia.org/wiki/%D7%9E%D7%AA%D7%9E%D7%98%D7%99%D7%A7%D7%94), ובפרט ב[תורת המספרים האנליטית](%D7%AA%D7%95%D7%A8%D7%AA%20%D7%94%D7%9E%D7%A1%D7%A4%D7%A8%D7%99%D7%9D%20%D7%94%D7%90%D7%A0%D7%9C%D7%99%D7%98%D7%99%D7%AA.md), **הנוסחאות המפורשות לפונקציות L** הן קשרים בין סכומים על פני האפסים המרוכבים של [פונקציית L](https://he.wikipedia.org/wiki/%D7%A4%D7%95%D7%A0%D7%A7%D7%A6%D7%99%D7%99%D7%AA_L) לבין סכומים על פני חזקות של [מספרים ראשוניים](https://he.wikipedia.org/wiki/%D7%9E%D7%A1%D7%A4%D7%A8_%D7%A8%D7%90%D7%A9%D7%95%D7%A0%D7%99). הנוסחה הראשונה מסוג זה הוצגה על ידי [ברנהרד רימן](https://he.wikipedia.org/wiki/%D7%91%D7%A8%D7%A0%D7%94%D7%A8%D7%93_%D7%A8%D7%99%D7%9E%D7%9F) בשנת 1859 עבור [פונקציית זטא של רימן](https://he.wikipedia.org/wiki/%D7%A4%D7%95%D7%A0%D7%A7%D7%A6%D7%99%D7%99%D7%AA_%D7%96%D7%98%D7%90_%D7%A9%D7%9C_%D7%A8%D7%99%D7%9E%D7%9F).[^1] נוסחאות מפורשות שימשו גם לקבלת חסמים על הדיסקרימיננטה ועל המוליך של [שדות מספרים](https://he.wikipedia.org/wiki/%D7%A9%D7%93%D7%94_%D7%9E%D7%A1%D7%A4%D7%A8%D7%99%D7%9D).

## הנוסחה המפורשת של רימן

*ערך מורחב: [הנוסחה המפורשת של רימן פון מנגולד](https://he.wikipedia.org/wiki/%D7%94%D7%A0%D7%95%D7%A1%D7%97%D7%94_%D7%94%D7%9E%D7%A4%D7%95%D7%A8%D7%A9%D7%AA_%D7%A9%D7%9C_%D7%A8%D7%99%D7%9E%D7%9F_%D7%A4%D7%95%D7%9F_%D7%9E%D7%A0%D7%92%D7%95%D7%9C%D7%93)* במאמרו משנת 1859, "[על מספר הראשוניים מתחת לגודל נתון](https://he.wikipedia.org/wiki/%D7%A2%D7%9C_%D7%9E%D7%A1%D7%A4%D7%A8_%D7%94%D7%A8%D7%90%D7%A9%D7%95%D7%A0%D7%99%D7%99%D7%9D_%D7%9E%D7%AA%D7%97%D7%AA_%D7%9C%D7%92%D7%95%D7%93%D7%9C_%D7%A0%D7%AA%D7%95%D7%9F)", שרטט רימן נוסחה מפורשת עבור [פונקציית המספרים הראשוניים](https://he.wikipedia.org/wiki/%D7%A4%D7%95%D7%A0%D7%A7%D7%A6%D7%99%D7%99%D7%AA_%D7%94%D7%9E%D7%A1%D7%A4%D7%A8%D7%99%D7%9D_%D7%94%D7%A8%D7%90%D7%A9%D7%95%D7%A0%D7%99%D7%99%D7%9D) המנורמלת $`\pi_0(x)`$. הנוסחה הוכחה במלואה רק בשנת 1895, על ידי הנס פון מנגולד. הפונקציה המנורמלת קשורה לפונקציית המספרים הראשוניים $`\pi(x)`$ על ידי



```math
\pi_0(x) = \frac{1}{2} \lim_{h\to 0} \left[\,\pi(x+h) + \pi(x-h)\,\right],
```



כלומר בנקודות אי-הרציפות היא מקבלת את ה[ממוצע](https://he.wikipedia.org/wiki/%D7%9E%D7%9E%D7%95%D7%A6%D7%A2_%D7%97%D7%A9%D7%91%D7%95%D7%A0%D7%99) של הגבול משמאל והגבול מימין.[^2] רימן ניסח את הנוסחה באמצעות הפונקציה הקשורה



```math
f(x) = \pi_0(x) + \frac{1}{2}\,\pi_0(x^{1/2}) + \frac{1}{3}\,\pi_0(x^{1/3}) + \cdots,
```



שבה חזקה $`p^n`$ של ראשוני נספרת כ-$`1/n`$ של ראשוני. את $`\pi_0`$ ניתן לשחזר מ-$`f`$ באמצעות [פונקציית מביוס](https://he.wikipedia.org/wiki/%D7%A4%D7%95%D7%A0%D7%A7%D7%A6%D7%99%D7%99%D7%AA_%D7%9E%D7%91%D7%99%D7%95%D7%A1) $`\mu(n)`$:[^3]



```math
\pi_0(x) = \sum_n\frac{1}{n}\,\mu(n)\,f(x^{1/n}) = f(x) - \frac{1}{2}\,f(x^{1/2}) - \frac{1}{3}\,f(x^{1/3}) - \frac{1}{5}\,f(x^{1/5}) + \frac{1}{6}\,f(x^{1/6}) - \cdots
```



הנוסחה של רימן היא



```math
f(x) = \mathrm{li}(x) - \sum_\rho \mathrm{li}(x^\rho) - \log(2) + \int_x^\infty \frac{dt}{t\,(t^2-1)\log(t)},
```



כאשר הסכום עובר על האפסים הלא-טריוויאליים $`\rho`$ של פונקציית זטא של רימן. הסכום אינו מתכנס בהחלט, אך ניתן לחשב אותו כאשר מסדרים את האפסים לפי הערך המוחלט של החלק המדומה שלהם. $`\mathrm{li}`$ היא [פונקציית האינטגרל הלוגריתמי](https://he.wikipedia.org/wiki/%D7%A4%D7%95%D7%A0%D7%A7%D7%A6%D7%99%D7%99%D7%AA_%D7%94%D7%90%D7%99%D7%A0%D7%98%D7%92%D7%A8%D7%9C_%D7%94%D7%9C%D7%95%D7%92%D7%A8%D7%99%D7%AA%D7%9E%D7%99), המוגדרת כערך העיקרי של קושי של האינטגרל המתבדר



```math
\mathrm{li}(x) = \int_0^x \frac{dt}{\log(t)}.
```



האיברים $`\mathrm{li}(x^\rho)`$ דורשים הגדרה זהירה, מאחר של-$`\mathrm{li}`$ יש [נקודות הסתעפות](https://he.wikipedia.org/wiki/%D7%A0%D7%A7%D7%95%D7%93%D7%AA_%D7%94%D7%A1%D7%AA%D7%A2%D7%A4%D7%95%D7%AA) ב-0 וב-1; הם מוגדרים באמצעות [המשכה אנליטית](https://he.wikipedia.org/wiki/%D7%94%D7%9E%D7%A9%D7%9B%D7%94_%D7%90%D7%A0%D7%9C%D7%99%D7%98%D7%99%D7%AA) במשתנה המרוכב $`\rho`$ בתחום $`x>1`$, $`\mathrm{Re}(\rho)>0`$. גם האיברים האחרים מתאימים לאפסים: האיבר הדומיננטי $`\mathrm{li}(x)`$ נובע מהקוטב ב-$`s=1`$, הנחשב כאפס מריבוי $`-1`$, והאיברים הקטנים הנותרים נובעים מהאפסים הטריוויאליים. הנוסחה מראה שאפסי פונקציית זטא של רימן שולטים בתנודות של הראשוניים סביב מיקומם ה"צפוי".[^4]

ההוכחה המלאה הראשונה של פון מנגולד, משנת 1895, החלה בהוכחת הנוסחה הבאה עבור [פונקציית צ'בישב](%D7%A4%D7%95%D7%A0%D7%A7%D7%A6%D7%99%D7%99%D7%AA%20%D7%A6%27%D7%91%D7%99%D7%A9%D7%91.md) $`\psi`$:[^5]



```math
\psi_0(x) = \dfrac{1}{2\pi i} \int_{\sigma-i \infty}^{\sigma+i \infty}\left(-\dfrac{\zeta'(s)}{\zeta(s)}\right)\dfrac{x^s}{s}\, ds = x - \sum_\rho\frac{x^\rho}{\rho} - \log(2\pi) -\dfrac{1}{2}\log(1-x^{-2}),
```



כאשר $`\sigma > 1`$, $`\psi(x) = \sum_{p^k \le x} \log p`$ ו-$`\psi_0`$ היא הגרסה המנורמלת שלה (ממוצע הגבולות משני הצדדים). אגף שמאל הוא [התמרת מלין](%D7%94%D7%AA%D7%9E%D7%A8%D7%AA%20%D7%9E%D7%9C%D7%99%D7%9F.md) הפוכה, ואגף ימין מתקבל מ[משפט השאריות](https://he.wikipedia.org/wiki/%D7%9E%D7%A9%D7%A4%D7%98_%D7%94%D7%A9%D7%90%D7%A8%D7%99%D7%95%D7%AA); מנוסחה זו עבר פון מנגולד לנוסחה ששרטט רימן. גם טור זה מתכנס בתנאי, והסכום על האפסים נלקח שוב לפי סדר עולה של החלק המדומה:[^6]



```math
\sum_\rho\frac{x^\rho}{\rho} = \lim_{T \to \infty} \sum_{\rho:\,|\mathrm{Im} \rho| \le T} \frac{x^\rho}{\rho}.
```



## הנוסחה המפורשת של וייל

ישנן כמה דרכים, השונות זו מזו במעט, לנסח את הנוסחה המפורשת. הגרסה של [אנדרה וייל](https://he.wikipedia.org/wiki/%D7%90%D7%A0%D7%93%D7%A8%D7%94_%D7%95%D7%99%D7%99%D7%9C) קובעת כי[^7]



```math
\Phi(1)+\Phi(0)-\sum_\rho\Phi(\rho) = \sum_{p,m} \frac{\log(p)}{p^{m/2} } \Big( F(\log(p^m)) + F(-\log(p^m)) \Big) - \frac{1}{2\pi} \int_{-\infty}^\infty \varphi(t)\Psi(t)\,dt,
```



כאשר:

- $`\rho`$ עובר על האפסים הלא-טריוויאליים של פונקציית זטא;
- $`p`$ עובר על הראשוניים החיוביים ו-$`m`$ על השלמים החיוביים;
- $`F`$ היא [פונקציה חלקה](https://he.wikipedia.org/wiki/%D7%A4%D7%95%D7%A0%D7%A7%D7%A6%D7%99%D7%94_%D7%97%D7%9C%D7%A7%D7%94) שכל נגזרותיה דועכות במהירות;
- $`\varphi`$ היא [התמרת פורייה](https://he.wikipedia.org/wiki/%D7%94%D7%AA%D7%9E%D7%A8%D7%AA_%D7%A4%D7%95%D7%A8%D7%99%D7%99%D7%94) של $`F`$: $`\varphi(t) = \int_{-\infty}^\infty F(x)e^{itx}\,dx`$;
- $`\Phi(1/2 + it) = \varphi(t)`$;
- $`\Psi(t) = - \log( \pi ) + \mathrm{Re}(\psi(1/4 + it/2))`$, כאשר $`\psi = \Gamma'/\Gamma`$ היא [פונקציית הדיגמא](https://he.wikipedia.org/wiki/%D7%A4%D7%95%D7%A0%D7%A7%D7%A6%D7%99%D7%99%D7%AA_%D7%93%D7%99%D7%92%D7%9E%D7%90).

באופן גס, הנוסחה המפורשת אומרת שהתמרת פורייה של אפסי פונקציית זטא היא קבוצת חזקות הראשוניים, בתוספת כמה גורמים אלמנטריים. מרגע שמנסחים זאת כך, הנוסחה נובעת מכך שהתמרת פורייה היא [אופרטור אוניטרי](https://he.wikipedia.org/wiki/%D7%90%D7%95%D7%A4%D7%A8%D7%98%D7%95%D7%A8_%D7%90%D7%95%D7%A0%D7%99%D7%98%D7%A8%D7%99), ולכן מכפלה סקלרית במרחב הזמן שווה למכפלה הסקלרית של ההתמרות במרחב התדירות.

האיברים בנוסחה נוצרים באופן הבא:

- האיברים באגף ימין באים מהנגזרת הלוגריתמית של $`\zeta^*(s)= \Gamma(s/2)\pi^{-s/2}\prod_p \frac{1}{1-p^{-s} }`$: האיברים המתאימים לראשוני $`p`$ באים מגורם אוילר של $`p`$ ב[מכפלת אוילר](https://he.wikipedia.org/wiki/%D7%9E%D7%9B%D7%A4%D7%9C%D7%AA_%D7%90%D7%95%D7%99%D7%9C%D7%A8), והאיבר האחרון, הכולל את $`\Psi`$, בא מגורם הגמא (גורם אוילר "באינסוף").
- אגף שמאל הוא סכום על כל האפסים של $`\zeta^*`$, הנספרים עם ריבוי, כך שהקטבים ב-0 וב-1 נספרים כאפסים מסדר $`-1`$.

ניתן להבין את הנוסחה של וייל כך. המטרה היא לכתוב



```math
\frac{d}{du} \left[ \sum_{n \le e^{|u|} } \Lambda(n) + \frac{1}{2} \ln(1-e^{-2|u|})\right] = \sum_{n=1}^\infty \Lambda(n) \left[ \delta(u+\ln n) + \delta(u-\ln n) \right] + \frac{1}{2}\frac{d\ln(1-e^{-2|u|})}{du} = e^u - \sum_\rho e^{\rho u},
```



כאשר $`\Lambda`$ היא [פונקציית פון מנגולד](https://he.wikipedia.org/wiki/%D7%A4%D7%95%D7%A0%D7%A7%D7%A6%D7%99%D7%99%D7%AA_%D7%A4%D7%95%D7%9F_%D7%9E%D7%A0%D7%92%D7%95%D7%9C%D7%93) ו-$`\delta`$ היא [פונקציית דלתא של דיראק](https://he.wikipedia.org/wiki/%D7%A4%D7%95%D7%A0%D7%A7%D7%A6%D7%99%D7%99%D7%AA_%D7%93%D7%9C%D7%AA%D7%90_%D7%A9%D7%9C_%D7%93%D7%99%D7%A8%D7%90%D7%A7). כלומר, התמרת פורייה של האפסים הלא-טריוויאליים שווה לחזקות הראשוניים, בגרסה סימטרית, בתוספת איבר קטן. הסכומים המעורבים אינם מתכנסים, אך ניתן להשתמש בכך שהתמרת פורייה שומרת על מכפלה סקלרית:



```math
\int_{-\infty}^\infty f(u) g^*(u) \, du = \int_{-\infty}^\infty F(t) G^*(t) \, dt,
```



כאשר $`F,G`$ הן התמרות פורייה של $`f,g`$. זהות זו נכונה במקרים רבים גם כאשר $`g`$ היא התפלגות (פונקציה מוכללת). לכן, אם בוחרים



```math
g(u) = \sum_{n=1}^\infty \Lambda(n) \left[ \delta(u+\ln n) + \delta(u-\ln n) \right]
```



ובוחרים בזהירות את הפונקציה $`f`$ ואת התמרת פורייה שלה, מתקבלת הנוסחה שלעיל.

## הכללות

ניתן להחליף את פונקציית זטא של רימן ב[פונקציית L של דיריכלה](https://he.wikipedia.org/wiki/%D7%A4%D7%95%D7%A0%D7%A7%D7%A6%D7%99%D7%99%D7%AA_L_%D7%A9%D7%9C_%D7%93%D7%99%D7%A8%D7%99%D7%9B%D7%9C%D7%94) של [קרקטר דיריכלה](https://he.wikipedia.org/wiki/%D7%A7%D7%A8%D7%A7%D7%98%D7%A8_%D7%93%D7%99%D7%A8%D7%99%D7%9B%D7%9C%D7%94) $`\chi`$. במקרה זה מופיעים בסכום על חזקות הראשוניים גורמים נוספים $`\chi(p^m)`$, והאיברים $`\Phi(1)`$ ו-$`\Phi(0)`$ נעלמים, משום שלטור L אין קטבים.

באופן כללי יותר, ניתן להחליף את פונקציית זטא ואת טורי L ב[פונקציית זטא של דדקינד](https://he.wikipedia.org/wiki/%D7%A4%D7%95%D7%A0%D7%A7%D7%A6%D7%99%D7%99%D7%AA_%D7%96%D7%98%D7%90_%D7%A9%D7%9C_%D7%93%D7%93%D7%A7%D7%99%D7%A0%D7%93) של שדה מספרים אלגבריים או בטור L של הקה. במקרה זה הסכום על הראשוניים מוחלף בסכום על [אידיאלים ראשוניים](https://he.wikipedia.org/wiki/%D7%90%D7%99%D7%93%D7%99%D7%90%D7%9C_%D7%A8%D7%90%D7%A9%D7%95%D7%A0%D7%99).

## שימושים

השימוש המקורי של רימן בנוסחה המפורשת היה לתת נוסחה מדויקת למספר הראשוניים הקטנים ממספר נתון. לשם כך בוחרים $`F(\log y) = y^{1/2}/\log y`$ עבור $`0 \le y \le x`$ ו-0 מחוץ לתחום זה. אז האיבר העיקרי של הסכום באגף ימין הוא מספר הראשוניים הקטנים מ-$`x`$. האיבר העיקרי באגף שמאל הוא $`\Phi(1)`$, שמתברר כי הוא האיבר הדומיננטי ב[משפט המספרים הראשוניים](https://he.wikipedia.org/wiki/%D7%9E%D7%A9%D7%A4%D7%98_%D7%94%D7%9E%D7%A1%D7%A4%D7%A8%D7%99%D7%9D_%D7%94%D7%A8%D7%90%D7%A9%D7%95%D7%A0%D7%99%D7%99%D7%9D), והתיקון העיקרי הוא הסכום על האפסים הלא-טריוויאליים של פונקציית זטא. (יש בכך בעיה טכנית קלה, משום שהפונקציה $`F`$ במקרה זה אינה מקיימת את תנאי החלקות.)

## השערת הילברט-פוליה

לפי [השערת הילברט-פוליה](%D7%94%D7%A9%D7%A2%D7%A8%D7%AA%20%D7%94%D7%99%D7%9C%D7%91%D7%A8%D7%98-%D7%A4%D7%95%D7%9C%D7%99%D7%94.md), האפסים המרוכבים $`\rho`$ אמורים להיות ה[ערכים העצמיים](https://he.wikipedia.org/wiki/%D7%A2%D7%A8%D7%9A_%D7%A2%D7%A6%D7%9E%D7%99) של [אופרטור](https://he.wikipedia.org/wiki/%D7%90%D7%95%D7%A4%D7%A8%D7%98%D7%95%D7%A8) ליניארי מסוים $`T`$. במקרה זה הסכום על האפסים בנוסחה המפורשת ניתן, לפחות באופן פורמלי, כ[עקבה](https://he.wikipedia.org/wiki/%D7%A2%D7%A7%D7%91%D7%94_%28%D7%90%D7%9C%D7%92%D7%91%D7%A8%D7%94%29):



```math
\sum_\rho F(\rho) = \mathrm{Tr}(F(\widehat T )).
```



וייל פיתח בשנת 1952 נוסחאות מפורשות עבור משפחה רחבה של פונקציות L.[^8] הוא הרחיב תחילה את הרעיון לפונקציות זטא מקומיות, וניסח בהקשר זה גרסה של [השערת רימן המוכללת](https://he.wikipedia.org/wiki/%D7%94%D7%A9%D7%A2%D7%A8%D7%AA_%D7%A8%D7%99%D7%9E%D7%9F) כטענת חיוביות על פונקציה מוכללת על [חבורה טופולוגית](https://he.wikipedia.org/wiki/%D7%97%D7%91%D7%95%D7%A8%D7%94_%D7%98%D7%95%D7%A4%D7%95%D7%9C%D7%95%D7%92%D7%99%D7%AA). עבודות מאוחרות יותר של [אלאן קון](https://he.wikipedia.org/wiki/%D7%90%D7%9C%D7%90%D7%9F_%D7%A7%D7%95%D7%9F) העמיקו ברקע של האנליזה הפונקציונלית, וסיפקו נוסחת עקבה שתקפותה שקולה להשערת רימן מוכללת מסוג זה.[^9] נקודת מבט שונה במעט הציג ראלף מאייר, שגזר את הנוסחה המפורשת של וייל באמצעות [אנליזה הרמונית](https://he.wikipedia.org/wiki/%D7%90%D7%A0%D7%9C%D7%99%D7%96%D7%94_%D7%94%D7%A8%D7%9E%D7%95%D7%A0%D7%99%D7%AA) על מרחבי אדלים.[^10]

## ראו גם

- [הנוסחה המפורשת של רימן פון מנגולד](https://he.wikipedia.org/wiki/%D7%94%D7%A0%D7%95%D7%A1%D7%97%D7%94_%D7%94%D7%9E%D7%A4%D7%95%D7%A8%D7%A9%D7%AA_%D7%A9%D7%9C_%D7%A8%D7%99%D7%9E%D7%9F_%D7%A4%D7%95%D7%9F_%D7%9E%D7%A0%D7%92%D7%95%D7%9C%D7%93)

## לקריאה נוספת

- H. M. Edwards, *Riemann's Zeta Function*, Pure and Applied Mathematics 58, Academic Press, New York–London, 1974
- A. E. Ingham, *The Distribution of Prime Numbers*, 2nd ed., Cambridge University Press, 1990
- Serge Lang, *Algebraic Number Theory*, 2nd ed., Graduate Texts in Mathematics 110, Springer-Verlag, 1994
- Hans Riesel, *Prime Numbers and Computer Methods for Factorization*, 2nd ed., Progress in Mathematics 126, Birkhäuser, 1994

## קישורים חיצוניים

- (באנגלית) Eric W. Weisstein, [Explicit Formula](https://mathworld.wolfram.com/ExplicitFormula.html), באתר MathWorld

## הערות שוליים



[^1]: Bernhard Riemann, *Ueber die Anzahl der Primzahlen unter einer gegebenen Grösse*, Monatsberichte der Berliner Akademie, 1859

[^2]: David R. Wilkins (translator), [On the Number of Prime Numbers less than a Given Quantity](https://www.claymath.org/wp-content/uploads/2023/04/Wilkins-translation.pdf), Clay Mathematics Institute, 1998

[^3]: Xian-Jin Li, *Explicit formulas for Dirichlet and Hecke L-functions*, Illinois Journal of Mathematics **48** (2004), no. 2, pp. 491–503, [<doi:10.1215/ijm/1258138394>](https://doi.org/10.1215/ijm/1258138394)

[^4]: Don Zagier, *The first 50 million prime numbers*, The Mathematical Intelligencer **1** (1977), suppl. 2, pp. 7–19, [<doi:10.1007/bf03351556>](https://doi.org/10.1007/bf03351556)

[^5]: Hans von Mangoldt, *Zu Riemanns Abhandlung "Über die Anzahl der Primzahlen unter einer gegebenen Grösse"*, Journal für die reine und angewandte Mathematik **114** (1895), pp. 255–305

[^6]: A. E. Ingham, *The Distribution of Prime Numbers*, 2nd ed., Cambridge Tracts in Mathematics and Mathematical Physics 30, Cambridge University Press, 1990, p. 77

[^7]: André Weil, *Sur les "formules explicites" de la théorie des nombres premiers*, Comm. Sém. Math. Univ. Lund, Tome Supplémentaire (1952), pp. 252–265

[^8]:

[^9]: Alain Connes, *Trace formula in noncommutative geometry and the zeros of the Riemann zeta function*, Selecta Mathematica **5** (1999), no. 1, pp. 29–106, [<doi:10.1007/s000290050042>](https://doi.org/10.1007/s000290050042)

[^10]: Ralf Meyer, *On a representation of the idele class group related to primes and zeros of L-functions*, Duke Mathematical Journal **127** (2005), no. 3, pp. 519–595, [<doi:10.1215/s0012-7094-04-12734-4>](https://doi.org/10.1215/s0012-7094-04-12734-4)


---
קטגוריות: פונקציות זטא · תורת המספרים האנליטית · מספרים ראשוניים


---
<sub>מבוסס על הערך [Explicit formulae for L-functions](https://en.wikipedia.org/wiki/Explicit_formulae_for_L-functions) בוויקיפדיה האנגלית ([היסטוריית העריכות ומחברים](https://en.wikipedia.org/w/index.php?title=Explicit_formulae_for_L-functions&action=history)). התוכן מופץ ברישיון [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/), ואפשר להעתיק אותו בחזרה לוויקיפדיה. [קוד הוויקי של הדף](../wiki/%D7%A0%D7%95%D7%A1%D7%97%D7%90%D7%95%D7%AA%20%D7%9E%D7%A4%D7%95%D7%A8%D7%A9%D7%95%D7%AA%20%D7%9C%D7%A4%D7%95%D7%A0%D7%A7%D7%A6%D7%99%D7%95%D7%AA%20L.wiki)</sub>
