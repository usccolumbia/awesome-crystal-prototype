# Contributing

Contributions are welcome: new resources, corrections and updated links.

## What belongs here

- Prototype libraries and catalogs, standardization and comparison algorithms, source databases, discovery workflows that use prototypes, template-based and generative CSP methods, benchmarks, mineral-family classifications, and statistical studies of how many distinct structure types exist.
- Peer-reviewed papers, preprints with a stable identifier, maintained code, and open datasets. Prefer a DOI or arXiv link for papers.

## Entry format

One bullet per entry, in the matching section, in this form:

```
* [Name or title](https://link) - One sentence on what it is or does (First-author et al., Year, Venue)
```

- Describe what the resource does, not how good it is.
- For code with a paper, link the code and add the paper at the end as `[[paper](https://doi.org/...)]`.
- State access limits when they matter, for example `(subscription)`.
- Put the entry in alphabetical or chronological order within its subsection, matching the neighbours.
- If a library reports a prototype count, say which equivalence rule it uses. Counts from different rules are not comparable.

## Before you open a pull request

```bash
python scripts/lint_readme.py        # format and duplicate checks
python scripts/check_links.py        # optional: confirms every URL still resolves
```

Add libraries to `data/prototype_libraries.csv` as well, and add BibTeX for new papers to `data/references.bib`.

## Corrections

If an entry is wrong or a link is dead, open an issue or a pull request with the replacement. Please include a source for factual changes such as counts, years and licences.
