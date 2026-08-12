# Data documentation

This directory contains the curated data used in the public analysis. Row order is never treated as a stable identifier. See `../DATA_NOTICE.md` for provenance, rights, and reuse boundaries.

## Data manifest

| File                                                  | Contents                                                            |   Rows / size | Key                        | Notes                                                                                                    |
| ----------------------------------------------------- | ------------------------------------------------------------------- | ------------: | -------------------------- | -------------------------------------------------------------------------------------------------------- |
| `processed/kuusi_proverb_types_clean.csv`             | Cleaned proverb-type corpus                                         |         1,727 | `kuusi_id`                 | Not the complete historical database; types are not usage observations                                   |
| `annotations/prescriptive_descriptive_sample_100.csv` | Stable pilot sample and text reference                              |           100 | `kuusi_id`                 | Label columns are intentionally blank; not an adjudicated gold standard                                  |
| `annotations/p1_label_100_proverbs.csv`               | First human coder’s original labels                                 |           100 | `kuusi_id`                 | Primary encoding is reversed relative to the study standard; includes 14 structural implicit-label skips |
| `annotations/p2_label_100_proverbs.csv`               | Second human coder’s original labels                                |           100 | `kuusi_id`                 | No adjudicated consensus is supplied for disagreements                                                   |
| `annotations/llm_annotation_input_100.csv`            | Blinded text and identifiers sent to ChatGPT                        |           100 | `kuusi_id`                 | Human-label columns are blank                                                                            |
| `annotations/llm_annotation_output_100.csv`           | Binary labels, confidence, and rationale returned by ChatGPT        |           100 | `id` → `kuusi_id`          | The exact model was not recorded; confidence and rationale each contain one unique retained value        |
| `unconstrained_llms/llm_text_input.csv`               | Text supplied for unconstrained category induction                  |         1,727 | `id`                       | Four identifiers are blank; text is retained for every row                                               |
| `unconstrained_llms/categorized_texts.csv`            | Category assignment returned for every input row                    |         1,727 | `id`                       | Four identifiers are blank; proverb text, rationale, and confidence are not retained                     |
| `unconstrained_llms/categories.txt`                   | Ten category definitions and the retained prompt                    | 10 categories | `category_id` 0–9          | Run conducted using GPT-5.5 through ChatGPT on the Free plan                                             |
| `wisdom_extractor/clusters.csv`                       | Cluster-level claims, scores, themes, and coverage                  |         1,606 | `cluster_id`               | Lexical and heuristic clusters, not validated semantic equivalence                                       |
| `wisdom_extractor/cluster_members.csv`                | Cluster membership and retained metadata for imported proverb types |         1,689 | `external_id` → `kuusi_id` | Repeated `cluster_id` values are expected                                                                |
| `wisdom_extractor/exclusions.csv`                     | Corpus records excluded from the Wisdom Extractor run               |            38 | `kuusi_id`                 | 34 records were not English-ready; four had blank distribution metadata                                  |
| `wisdom_extractor/sensitivity.csv`                    | Lexical-distance threshold summaries                                |             6 | `tau`                      | Describes this run only; no human-validated optimum was established                                      |

## Cleaned corpus fields

The 36 fields in `processed/kuusi_proverb_types_clean.csv` are grouped as follows:

| Group                         | Fields                                                                                                                                                                | Meaning                                                                       |
| ----------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------- |
| Identifiers and hierarchy (6) | `source_id`, `kuusi_id`, `theme`, `main_class`, `subgroup_code`, `type_number`                                                                                        | Source record link and inherited Kuusi classification hierarchy               |
| Proverb text and variants (7) | `proverb_original`, `proverb_variant_1`, `proverb_variant_2`, `proverb_variant_3`, `proverb_variant_4`, `proverb_variant_extra`, `proverb_primary_en`                 | Preserved source wording, parsed alternatives, and primary modeling text      |
| Text and language audit (6)   | `proverb_primary_en_is_english`, `proverb_parse_warning`, `language_tags_raw`, `translation_tag_types`, `language_names_extracted`, `has_language_or_translation_tag` | Flags and extracted metadata for auditing parsing and English readiness       |
| Source references (4)         | `slug`, `missing_marker`, `cross_references`, `specific_reference`                                                                                                    | Retained website markers and typological references                           |
| Distribution metadata (13)    | `distribution` and the 12 `distribution_*` indicator fields                                                                                                           | Original distribution code and one binary indicator for each broad Kuusi area |

The corpus contains 13 observed themes, 52 main classes, and 316 observed subgroup codes. These are corpus observations, not a redefinition of the broader historical system.

## Identifier and join rules

* Use `kuusi_id` as the canonical identifier for the cleaned corpus and annotation files. It is unique and non-missing across all 1,727 cleaned records.
* Join Wisdom Extractor `external_id` to `kuusi_id`.
* Use normalized `source_id` only for the unconstrained LLM experiment. The notebook removes a terminal `.0` introduced by CSV numeric formatting without overwriting the original value.
* Join the 100-record LLM annotation output’s `id` to annotation `kuusi_id` after string normalization.
* Wisdom Extractor `cluster_id` identifies a cluster, not a proverb. Repeated values in `cluster_members.csv` are expected.
* Record-level merges are validated as one-to-one wherever uniqueness is expected. Row order is never used as the join key.

## Annotation encoding

P1’s raw primary-label convention is `0 = descriptive` and `1 = prescriptive`. The study convention is `0 = prescriptive` and `1 = descriptive`. The notebook preserves P1’s raw values and reverses them once using `1 - value`. It also verifies that every non-missing original and standardized pair sums to one. P2 and the LLM already use the study convention.

P1 has 14 missing `has_implicit_prescription` values. These are structural skips for records that P1 labeled explicitly prescriptive. The notebook preserves the missing values and derives `implicit prescription absent` only for comparison under the pilot protocol. These derived values are not presented as original annotations.

Human disagreements are not converted into an invented consensus. The human-agreement subset includes only records on which P1 and P2 agree for the dimension being analyzed.

## Unidentified unconstrained-LLM outputs

The unconstrained input and output files each contain 1,727 rows, including four rows with blank identifiers. Aggregate category counts use all 1,727 valid output labels. Record-level analyses use the 1,723 uniquely identified outputs that join one-to-one to the saved input and cleaned corpus.

Each blank-ID input row retains proverb text with one exact corpus match, but its corresponding output retains only a category label. Because row position is not a stable identifier, these four categories are not assigned to corpus records and remain excluded from record-level joins.

## Wisdom Extractor boundary

The notebook analyzes precomputed Wisdom Extractor v19.22 results rather than rebuilding the third-party tool. The released outputs contain:

* 1,689 imported proverb types;
* 38 exclusions;
* 1,606 clusters;
* 4,068 type-to-distribution-area links;
* 1,527 singleton clusters and 79 multi-type clusters.

The original `run_metadata.json`, `RUN_NOTES.md`, and upstream source hash are not included. The released files support inspection and validation of the saved results, but not exact reconstruction of the original Wisdom Extractor run.
