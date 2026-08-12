# Data, rights, and attribution

This repository contains a cleaned research derivative of selected material from the [Matti Kuusi International Type System and Database of Proverbs](https://mattikuusiproverbtypology.fi/proverb-types/). It is not the complete historical database or a newly authored collection of proverbs.

## Source

The foundational publication is:

> Lauhakangas, Outi. 2001. *The Matti Kuusi International Type System of Proverbs*. FF Communications No. 275. Helsinki: Suomalainen Tiedeakatemia / Academia Scientiarum Fennica. ISSN 0014-5815. ISBN 951-41-0882-5 and 951-41-0883-3.

The publication states “© ASF and Outi Lauhakangas.”

Project data were collected from the online proverb-types database in June 2026. The cleaned corpus preserves and restructures selected source information while adding project-specific identifiers and parsed fields. The internal raw JSON and source PDF are not distributed.

## Publication permission

Outi Lauhakangas provided written permission specific to this project to publish the project and modified versions of the source dataset.

This permission supports this curated release. It does not establish a general open-data licence or grant additional rights to the underlying database, proverb content, translations, publications, or other third-party material.

## Licensing

The root `LICENSE` applies only to original project software and configuration, including original notebook code, `src/kuusi_cleaning.py`, and `requirements.txt`.

It does not license:

* source or cleaned data and proverb content;
* human annotations;
* LLM or Wisdom Extractor inputs and outputs;
* figures and saved research outputs;
* publications, bibliographic content, or other third-party material.

Unless a file states otherwise, its inclusion in this repository does not grant unrestricted reuse rights.

## Third-party tools and experimental outputs

This project includes research outputs produced using [Wisdom Extractor](https://github.com/ovladon/wisdom-extractor), [`all-MiniLM-L6-v2`](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2), and ChatGPT. The third-party software and model weights are not included in this repository and remain subject to their respective terms.

The unconstrained LLM categorization experiment was conducted using GPT-5.5 through ChatGPT on the Free plan.

## Reuse and attribution

Anyone reusing these materials should cite Lauhakangas (2001), identify the Matti Kuusi typology as the source, acknowledge this project’s transformations, and determine whether their intended use requires additional permission.
