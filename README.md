# Scottish Government data centre FOI annexes (November 2026): searchable text and index

This repository holds machine-readable text and a search interface for two Scottish Government information releases about data centres. It was compiled for research on hyperscale data centre planning in Scotland.

| Release | Title | Published | Pages | Source |
|---|---|---|---|---|
| FOI/202600522764 | Green Data Centre guidance: FOI release, Annex | 2 November 2026 | 147 | https://www.gov.scot/publications/foi-202600522764/ |
| EIR/202600522802 | Data centre guidance: EIR release, Annex | 3 November 2026 | 36 | https://www.gov.scot/publications/foi-202600522802/ |

The original PDFs are **not** redistributed here. Download them from the gov.scot pages above. You can check that your copy is the same one used to build this repository against these SHA-256 checksums (files downloaded on 22 November 2026):

```
52603a8f1b90c6858bc8fa38a2d2faced7e7bf5053c26bbaa74c2a63a00f5afd  FOI 202600522764 - Information released - Annex.pdf
9bd55b2879e9ede0d289ffcf818a285cf1ebea4638b2caca373e5dd230540320  EIR 202600522802 - Information released - Annex.pdf
```

## Contents

- `text/FOI-202600522764/p001.txt` to `p147.txt`, and `text/EIR-202600522802/p001.txt` to `p036.txt`: text of each page, taken from the PDF text layer with `pdftotext -layout` (poppler). File numbers match PDF page numbers.
- `docs/index.html`: a self-contained search page (all terms on one page, "quoted" phrases, highlighting, a page reader, and copyable page-level citations). It also has a sortable index of 78 emails and 5 sets of working-group minutes, and a short list of key passages. It runs on GitHub Pages from `/docs`.
- `docs/index.json`: the data behind the page. It holds normalised page text plus the email and minutes index (date, subject and page).
- `scripts/make_index.py`: the script that builds `index.json` from the page text.

## Method and caveats

- Text is unchanged from the PDF text layer apart from Unicode NFKC normalisation (which expands ligatures such as "ﬁ" to "fi") and collapsing of long runs of spaces.
- In `index.json`, pages with fewer than 200 characters of text were supplemented by OCR (Tesseract, 200 dpi), marked "[OCR of page image]". These are mostly email signatures and presentation slides in the EIR annex. The OCR is imperfect, and the files in `text/` contain the text layer only.
- Redactions appear as they do in the originals, e.g. "[Redacted - S.38(1)(b)]".
- The email index was built automatically from `Sent:` and `Subject:` header lines, so it may miss items or split threads. Always check against the PDF before citing.
- Cite the original releases and their PDF page numbers. This repository is a finding aid, not a substitute for them.

## Rights

The released documents are Crown copyright. Where the Scottish Government's Open Government Licence v3.0 applies, the derived text here is reused under it. The annexes also contain material written by third parties, including industry slides, a developer's charter, and correspondence from journalists and members of the public. Copyright in that material stays with its authors, and it is reproduced here only as text for research and criticism.

The code (`scripts/`, and the HTML, CSS and JavaScript in `docs/index.html`) is released under the MIT licence.

## How to cite

See `CITATION.cff`, or:

> Cross, J. (2026). *Scottish Government data centre FOI annexes (November 2026): searchable text and index* [Data set]. GitHub. https://github.com/jamiejcross/scotgov-data-centres-foi-2026

For a persistent DOI, archive a tagged release through the GitHub–Zenodo integration.
