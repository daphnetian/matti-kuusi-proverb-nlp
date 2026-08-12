# Public data documentation

The public analysis uses the curated files below. Row order is never treated as a stable identifier. Rights and reuse boundaries are described in [`../DATA_NOTICE.md`](../DATA_NOTICE.md).

## Public data manifest

| Relative path | Purpose | Records | Identifier | Material type | Notebook section | Important exclusions or limitations |
|---|---|---:|---|---|---|---|
| `processed/kuusi_proverb_types_clean.csv` | Cleaned NLP-ready proverb-type corpus | 1,727 | `kuusi_id` | Cleaned derivative of source data | Source loading and all analyses | Not the complete database; raw scrape excluded; types are not usage observations |
| `annotations/prescriptive_descriptive_sample_100.csv` | Stable 100-record pilot sample and text reference | 100 | `kuusi_id` | Project sample | Human–LLM annotation pilot | Label columns intentionally blank; not an adjudicated gold standard |
| `annotations/p1_label_100_proverbs.csv` | First human coder's original labels | 100 | `kuusi_id` | Human annotation | Human–LLM annotation pilot | Primary encoding is reversed relative to the study standard; 14 structural implicit-label skips |
| `annotations/p2_label_100_proverbs.csv` | Second human coder's original labels | 100 | `kuusi_id` | Human annotation | Human–LLM annotation pilot | No adjudicated consensus is supplied for human disagreements |
| `annotations/llm_annotation_input_100.csv` | Blinded text and identifiers sent to ChatGPT | 100 | `kuusi_id` | LLM experiment input | Human–LLM annotation pilot | Human-label columns are blank |
| `annotations/llm_annotation_output_100.csv` | Binary labels, confidence, and rationale returned by ChatGPT | 100 | `id` (maps to `kuusi_id`) | LLM output | Human–LLM annotation pilot | Exact model unverified; confidence and rationale each contain only one unique retained value |
| `unconstrained_llms/llm_text_input.csv` | Text supplied for unconstrained category induction | 1,727 | `id` (source identifier) | LLM experiment input | Unconstrained LLM experiment | Four identifiers are blank; text is retained for all rows |
| `unconstrained_llms/categorized_texts.csv` | Category assignment returned for every input row | 1,727 | `id` (source identifier) | LLM output | Unconstrained LLM experiment | Four identifiers are blank; no proverb text, rationale, or confidence is retained |
| `unconstrained_llms/categories.txt` | Ten category definitions and the retained prompt | 10 categories | `category_id` 0–9 | LLM output / experiment note | Unconstrained LLM experiment | Historical `GPT5.5` wording is unverified; actual model was not recorded |
| `wisdom_extractor/clusters.csv` | Cluster-level claims, scores, themes, and coverage | 1,606 | `cluster_id` | Precomputed external-tool output | Wisdom Extractor analysis | Lexical/heuristic clusters; not validated semantic equivalence |
| `wisdom_extractor/cluster_members.csv` | Membership and retained metadata for imported proverb types | 1,689 | `external_id` (`kuusi_id`) | Precomputed external-tool output | Wisdom Extractor analysis | `cluster_id` is intentionally many-to-one; metadata include derived tool fields |
| `wisdom_extractor/exclusions.csv` | Corpus records excluded from the external-tool run | 38 | `kuusi_id` | Precomputed external-tool output | Wisdom Extractor analysis | 34 were not English-ready; four had blank distribution metadata |
| `wisdom_extractor/sensitivity.csv` | Six lexical-distance threshold summaries | 6 | `tau` | Precomputed external-tool output | Wisdom Extractor analysis | Describes this run only; no human-validated optimum is established |

## Cleaned corpus fields

The 36 fields in `processed/kuusi_proverb_types_clean.csv` are grouped as follows:

| Group | Fields | Meaning |
|---|---|---|
| Identifiers and hierarchy (6) | `source_id`, `kuusi_id`, `theme`, `main_class`, `subgroup_code`, `type_number` | Source record link and the inherited Kuusi classification hierarchy |
| Proverb text and variants (7) | `proverb_original`, `proverb_variant_1`, `proverb_variant_2`, `proverb_variant_3`, `proverb_variant_4`, `proverb_variant_extra`, `proverb_primary_en` | Preserved source wording, parsed alternatives, and the primary modeling text |
| Text and language audit (6) | `proverb_primary_en_is_english`, `proverb_parse_warning`, `language_tags_raw`, `translation_tag_types`, `language_names_extracted`, `has_language_or_translation_tag` | Flags and extracted metadata for auditing parsing and English readiness |
| Source references (4) | `slug`, `missing_marker`, `cross_references`, `specific_reference` | Retained website/source markers and typological references |
| Distribution metadata (13) | `distribution` plus the 12 `distribution_*` indicator fields | Original distribution code and one binary indicator for each broad Kuusi area |

The project corpus contains 13 observed themes, 52 main classes, and 316 observed subgroup codes. Those are corpus observations, not a redefinition of the broader historical system.

## Identifier and join rules

- Use `kuusi_id` as the canonical identifier for the cleaned corpus, annotation files, and Wisdom Extractor `external_id` joins. It is unique and non-missing across all 1,727 cleaned records.
- Use normalized `source_id` only where the unconstrained-LLM experiment requires it. The notebook removes a terminal `.0` introduced by CSV numeric formatting without overwriting the original value.
- The 100-record LLM annotation output uses `id`; it is joined one-to-one to annotation `kuusi_id` after string normalization.
- Wisdom Extractor `cluster_id` identifies a cluster, not a proverb. Repeated `cluster_id` values in `cluster_members.csv` are expected.
- Every record-level merge is validated as one-to-one where uniqueness is expected. Row order may be inspected as supporting evidence but is never the join key.

## Annotation encoding

P1's raw primary-label convention is `0 = descriptive`, `1 = prescriptive`. The study convention is `0 = prescriptive`, `1 = descriptive`. The notebook therefore preserves P1's raw value and reverses it exactly once with `1 - value`; it also asserts that each non-missing original/standardized pair sums to one. P2 and the LLM already use the study convention. Analysis is performed with descriptive string labels derived from the standardized values.

P1 also has 14 missing `has_implicit_prescription` values. These are documented structural skips on records that P1 labeled explicitly prescriptive. The notebook preserves those original missing values separately and derives `implicit prescription absent` only as a comparison label under the pilot protocol. The derived comparison labels are not presented as originally observed annotations.

Human disagreement is not converted into an invented consensus. The human-agreement subset contains only records on which P1 and P2 agree for the dimension being analyzed.

## Four unidentified unconstrained-LLM outputs

Both unconstrained files contain 1,727 rows, including four blank identifiers. All output category labels are valid, so aggregate category counts use all 1,727 outputs. Record-level analyses use only the 1,723 outputs with unique identifiers that join one-to-one to the saved input and cleaned corpus.

Each blank-ID input row retains proverb text with one exact corpus match. The corresponding output rows retain only category labels and no stable record field. Although the blank rows occupy matching positions in the input and output files, row position alone is insufficient to assign the outputs. No identifiers are imputed, and the four outputs remain excluded from record-level joins.

## Wisdom Extractor boundary

The notebook analyzes precomputed Wisdom Extractor v19.22 results rather than rebuilding the third-party tool. The included outputs report:

- 1,689 imported proverb types;
- 38 exclusions;
- 1,606 clusters;
- 4,068 type-to-distribution-area links;
- 1,527 singleton clusters and 79 multi-type clusters.

The bundle does not include the original `run_metadata.json`, `RUN_NOTES.md`, or a recorded upstream source hash. File integrity and internal counts can be checked, but the exact upstream commit used for the external run cannot be independently verified from this release.

The local project folder also contains `data/llm_text_input.csv`, a duplicate unconstrained-LLM input. It is deliberately excluded from the public manifest and authoritative workflow; `unconstrained_llms/llm_text_input.csv` is the only documented input.
