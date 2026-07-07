# "The Great Convergence" — Tableau Public story spec

Dataset: Gapminder (1,704 rows: 142 countries x 12 five-year points,
1952-2007; lifeExp, pop, gdpPercap, continent). Every number in the
narrative below was computed from the file — they're annotations, not
copy.

## Thesis (one sentence, on the title slide)

In 1952, 1% of humanity lived in a country with life expectancy over 70;
by 2007 it was 61% — but the convergence ran backwards through southern
Africa, and the story is honest only if it shows both.

## Story points (Tableau Story, 6 points)

**1 — Two worlds (1952).** Histogram/strip plot of lifeExp, 1952: median
45.1, range 28.8-72.7. Annotation: a child born that year in most of the
world had a life expectancy under 50.

**2 — The march (animation).** The classic Gapminder connected scatter:
gdpPercap (log axis) x lifeExp, size = pop, color = continent, Pages
shelf on year for the animation. This is the homage slide — say so in the
caption (Rosling, 2006).

**3 — Convergence measured.** Line: % of world population living in
countries with lifeExp >= 70, by year — 1.1% (1952) to 61.4% (2007).
THE LOD SLIDE:
```
// numerator: population in countries at/above the bar, per year
SUM(IF [Life Exp] >= [p_Threshold] THEN [Pop] END) / SUM([Pop])
// with a parameter p_Threshold (default 70) so the reader can move the bar
```
computed per year via a FIXED LOD on {FIXED [Country], [Year]} grain
(the data is already at that grain; the LOD showcase is the world-share
denominator: { FIXED [Year] : SUM([Pop]) } so the ratio survives country
filters).

**4 — The champions.** Slope chart (custom chart type #1), 1952 -> 2007,
all countries in grey; Oman (+38.1 years), Vietnam (+33.8), Indonesia
(+33.2) highlighted. Caption: the biggest winners weren't the richest —
they were fast followers on vaccines, sanitation, and primary care.

**5 — The reversal.** Same slope chart re-anchored 1987 -> 2007, southern
Africa highlighted: Zimbabwe -18.9 years, Eswatini (Swaziland) -18.1,
Lesotho -14.6, Botswana -12.9. Caption names the cause plainly and
respectfully: the HIV/AIDS epidemic erased a generation of gains before
antiretrovirals scaled. No decoration on this slide; grey + one color.

**6 — Where the bar moves next.** Interactive close: the threshold
parameter from point 3 + country highlighter action; caption invites the
reader to set the bar at 75 and watch the 2007 share fall to a minority
again — convergence is a moving target.

## Techniques checklist (the skills being demonstrated)

- FIXED LOD for world-population denominators that survive filtering
- Parameter (threshold) wired into both a calc and reference line
- Story points with dashboard actions (country highlight across points)
- Custom chart: slope charts built from a dual-filtered line mark
- Pages animation on the scatter
- Annotation discipline: every number annotated is derived from the data

## Design rules

Grey-first palette; one highlight color per point (blue for gains, a
muted red reserved for point 5). Serif for narrative captions, sans for
axis text. Sources footer on every point: "Gapminder v1, via the
gapminder R/Python package."
