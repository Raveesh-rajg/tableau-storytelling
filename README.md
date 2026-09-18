# Global Health Convergence

A reproducible Gapminder analysis and packaged Tableau workbook covering changes in life expectancy across 142 countries, 1952–2007.

## Delivered artifacts

- [`GlobalHealth.twbx`](GlobalHealth.twbx): packaged workbook with four worksheets and relative CSV connections.
- [`GlobalHealth.twb`](GlobalHealth.twb): inspectable XML source.
- [`build_workbook.py`](build_workbook.py): reproduces population-weighted threshold shares, country gains/declines and the workbook.
- [`outputs/evidence.json`](outputs/evidence.json): source observations, derived series, coverage and interpretation limits.

Four tests pass: balanced panel and weighted denominator, threshold sensitivity, country-change calculation and packaged connection integrity. **Native Tableau rendering and publication have not been verified.** The six-point interactive Story, scatterplot/pages animation and threshold parameter described in `docs/STORY_SPEC.md` are remaining native enhancements; the delivered workbook has four analytical worksheets.

## Reproduce

```sh
python -m pip install -r requirements.txt
python build_workbook.py
python -m pytest tests -q
```

Open `GlobalHealth.twbx` in Tableau Desktop/Public, validate all worksheets and publish from your own account. The packaged workbook embeds only public Gapminder-derived CSVs. A published Tableau Public URL has not been recorded.

## Interpretation

The share living in countries with life expectancy at least 70 rises from approximately 1.1% to 61.4%, **weighted by population within this panel**. It is not coverage of every country or every person worldwide. Median country life expectancy and population-weighted shares answer different questions. National averages conceal inequality; five-year observations miss short-term changes. GDP and health associations do not establish causes of the changes.
