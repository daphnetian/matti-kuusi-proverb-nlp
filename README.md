# Exploring Proverb Similarity and Classification with the Matti Kuusi Typology

This **7–8 week exploratory research project** uses **1,727 cleaned proverb-type records** from the Matti Kuusi International Type System of Proverbs to examine how different computational methods handle short, often metaphorical texts.

The result is an analysis-ready corpus with **36 linguistic, hierarchical, geographic, and bibliographic fields**, unique canonical identifiers, and no missing primary texts. The project compares lexical, embedding-based, clustering, LLM, annotation, and supervised classification approaches to understand what each captures and where its limitations lie.

## What the project includes

* Descriptive analysis of themes, regions, languages, and classification hierarchies
* TF-IDF and [`all-MiniLM-L6-v2`](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2) retrieval comparison
* Lexical clustering with [Wisdom Extractor](https://github.com/ovladon/wisdom-extractor)
* Exploratory LLM-generated semantic groupings
* Human annotation of prescriptive and descriptive proverb functions
* Supervised TF-IDF classification proof of concept

Full methodology, code, figures, results, and interpretation are in `kuusi_nlp_research_notebook.ipynb`.

## Key findings

* **TF-IDF and MiniLM retrieved different kinds of neighbours.** TF-IDF favoured shared words and phrases, while MiniLM sometimes retrieved proverbs with less lexical overlap but related topics or meanings. This was a qualitative comparison, so similarity does not establish semantic equivalence.
* **Human coders agreed strongly on explicit prescriptive versus descriptive wording:** **95% agreement, Cohen’s κ = 0.798**. Agreement on implicit prescription was much weaker at **63%, κ = 0.127**, suggesting that this distinction needs a more precise codebook.
* **The supervised classifier did not beat the majority baseline.** Accuracy was **0.817**, compared with **0.874** for the baseline. Higher balanced accuracy and macro-F1 suggest some minority-class signal, but not enough to support a practically useful classifier.

## Repository guide

* `kuusi_nlp_research_notebook.ipynb` — complete analysis and experiments
* `data/processed/kuusi_proverb_types_clean.csv` — cleaned 1,727-record corpus
* `data/README.md` — data manifest, field groups, identifiers, and join rules
* `src/kuusi_cleaning.py` — documented cleaning logic
* `DATA_NOTICE.md` — source, permission, and reuse information
* `requirements.txt` — Python dependencies

## Quick start

Tested with **Python 3.13.5**.

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
jupyter lab
```

Open the notebook and run all cells in order.

On Windows, activate the environment with:

```bash
.venv\Scripts\activate
```

Internet access is required the first time MiniLM is downloaded.

## Scope and limitations

This is an **exploratory project completed over approximately 7–8 weeks**, not a finished semantic taxonomy or benchmark.

The corpus is a cleaned project derivative rather than the complete historical Matti Kuusi database. The public notebook begins with the cleaned CSV and does not reproduce the internal raw-data collection process.

The English titles are short and sometimes translated, and proverb use is analysed without conversational context. Retrieval was evaluated through a small manual comparison rather than a formal benchmark. Wisdom Extractor clusters, LLM-generated categories, and similarity scores should therefore be treated as exploratory outputs rather than semantic ground truth.

## Citation and reuse

The foundational source is:

> Lauhakangas, Outi. 2001. *The Matti Kuusi International Type System of Proverbs*. FF Communications No. 275. Helsinki: Suomalainen Tiedeakatemia / Academia Scientiarum Fennica. ISSN 0014-5815. ISBN 951-41-0882-5 and 951-41-0883-3.

See `DATA_NOTICE.md` before reusing the corpus or research outputs.

The root `LICENSE` covers original project software and configuration. It does not license the underlying data, proverb content, annotations, generated outputs, publications, or other third-party materials.

## Acknowledgements

Developed through research with the DICE Lab at the University of Waterloo, with guidance from Abhishek Dedhe and support from Samuel Johnson, the lab’s principal investigator. Thanks to Outi Lauhakangas for project-specific publication permission and to the undergraduate lab researchers who contributed to the annotation pilot.