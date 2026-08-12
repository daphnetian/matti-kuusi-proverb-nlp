# Data, rights, and attribution

This repository contains a cleaned research derivative of material from the [Matti Kuusi International Type System and Database of Proverbs](https://mattikuusiproverbtypology.fi/proverb-types/). It is not the complete historical database or a newly authored collection of proverbs.

## Source

The foundational publication is:

> Lauhakangas, Outi. 2001. *The Matti Kuusi International Type System of Proverbs*. FF Communications No. 275. Helsinki: Suomalainen Tiedeakatemia / Academia Scientiarum Fennica. ISSN 0014-5815. ISBN 951-41-0882-5 and 951-41-0883-3.

The publication states “© ASF and Outi Lauhakangas.”

The project source was collected from the online proverb-types database in June 2026. The cleaned corpus preserves and restructures selected source information while adding project-specific identifiers and parsed fields. The internal raw JSON and source PDF are not distributed.

## Publication permission

Outi Lauhakangas provided written permission specific to this project to publish the project and modifications of the source dataset.

This permission supports this curated release. It does not create a general open-data licence or grant additional rights to the underlying database, proverb content, translations, publications, or other third-party material.

## Licensing

The root `LICENSE` applies only to original project software and configuration, including original notebook code, `src/kuusi_cleaning.py`, and `requirements.txt`.

It does not apply to:

* source or cleaned data and proverb content;
* human annotations;
* LLM or Wisdom Extractor inputs and outputs;
* generated figures and saved research outputs;
* publications, bibliographic content, or other third-party material.

Unless an item has its own licence, its inclusion in this repository does not grant unrestricted reuse rights.

## Third-party and experimental outputs

The project includes outputs produced using [Wisdom Extractor](https://github.com/ovladon/wisdom-extractor) and [`all-MiniLM-L6-v2`](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2). The associated software and model files are not redistributed and remain subject to their own terms.

The LLM experiment used the ChatGPT free tier, but the exact underlying model was not recorded. The historical label “GPT5.5 free version” remains in `data/unconstrained_llms/categories.txt` but should not be treated as a verified model identity.

## Reuse

Anyone reusing these materials should cite Lauhakangas (2001), identify the Matti Kuusi typology as the source, acknowledge this project’s transformations, and determine whether their intended use requires additional permission.
