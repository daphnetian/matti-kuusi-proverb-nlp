# Exploring Proverb Similarity and Classification with the Matti Kuusi Typology

This project uses **1,727 cleaned proverb-type records** from the Matti Kuusi International Type System of Proverbs to explore how different computational methods handle short, often metaphorical texts.

The result is a research corpus with 36 linguistic, hierarchical, geographic, and bibliographic fields, unique canonical identifiers, and no missing primary texts. The analysis compares several methods to understand what each one captures, where it struggles, and how much confidence we should place in its results.

## What the project includes

* Descriptive analysis of themes, regions, languages, and classification hierarchies
* A retrieval comparison between TF-IDF and [`all-MiniLM-L6-v2`](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2)
* Lexical clustering with [Wisdom Extractor](https://github.com/ovladon/wisdom-extractor)
* An exploratory LLM-generated grouping of the corpus
* A human annotation pilot examining prescriptive and descriptive functions
* A supervised TF-IDF classification proof of concept

The full methodology, code, figures, results, and interpretation are in [`kuusi_nlp_research_notebook.ipynb`](kuusi_nlp_research_notebook.ipynb).

## Key findings

* **TF-IDF and MiniLM retrieved different kinds of neighbours.** TF-IDF favoured shared words and phrases. MiniLM sometimes found proverbs with less lexical overlap but related topics or meanings. This was a qualitative comparison, so similarity does not prove that two proverbs express the same idea.
* **Human coders agreed strongly on the prescriptive versus descriptive distinction.** They reached 95% agreement and Cohen’s κ = 0.798. Agreement on implicit prescription was much weaker at 63%, with κ = 0.127.
* **The classifier did not beat the majority baseline.** Its accuracy was 0.817, compared with 0.874 for the baseline. Improvements in balanced accuracy and macro-F1 suggest that it detected some minority-class signal, but not enough to support a practically useful classifier.

## Repository guide

* [`kuusi_nlp_research_notebook.ipynb`](kuusi_nlp_research_notebook.ipynb): complete analysis and experiments
* [`data/processed/kuusi_proverb_types_clean.csv`](data/processed/kuusi_proverb_types_clean.csv): cleaned 1,727-record corpus
* [`data/README.md`](data/README.md): data manifest, field groups, identifiers, and join rules
* [`src/kuusi_cleaning.py`](src/kuusi_cleaning.py): documented cleaning logic
* [`DATA_NOTICE.md`](DATA_NOTICE.md): source, permission, and reuse information
* [`requirements.txt`](requirements.txt): Python dependencies

## Quick start

Tested with **Python 3.13.5**.

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
jupyter lab
```

Open the notebook and run all cells in order. On Windows, activate the environment with `.venv\Scripts\activate`. Internet access is required the first time MiniLM is downloaded.

## Scope and limitations

This corpus is a cleaned project derivative, not the complete historical Matti Kuusi database. The public notebook starts with the cleaned CSV and does not reproduce the internal raw-data collection process.

The English titles are short and sometimes translated. Retrieval was assessed through a small manual comparison rather than a formal benchmark. Wisdom Extractor clusters, LLM-generated categories, and similarity scores are exploratory outputs rather than semantic ground truth.

## Citation and reuse

The foundational source is:

> Lauhakangas, Outi. 2001. *The Matti Kuusi International Type System of Proverbs*. FF Communications No. 275. Helsinki: Suomalainen Tiedeakatemia / Academia Scientiarum Fennica. ISSN 0014-5815. ISBN 951-41-0882-5 and 951-41-0883-3.

See [`DATA_NOTICE.md`](DATA_NOTICE.md) before reusing the corpus or research outputs.

The root [`LICENSE`](LICENSE) covers original project software and configuration. It does not license the underlying data, proverb content, annotations, generated outputs, publications, or other third-party materials.

## Acknowledgements

Developed through research with the DICE Lab at the University of Waterloo, with guidance from Abhishek Dedhe and support from Samuel Johnson, the lab’s principal investigator. Thanks to Outi Lauhakangas for project-specific publication permission and to the undergraduate lab researchers who contributed to the annotation pilot.
