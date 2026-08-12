"""Clean the Matti Kuusi proverb-type snapshot for notebook analysis.

Public API
----------
clean_kuusi_data(raw)
    Transform the raw pandas DataFrame into the 36-column cleaned corpus.
validate_clean_data(clean)
    Run project-specific checks on the completed 1,727-row corpus.

This module is self-contained. It replaces the former arrangement in which
``src/kuusi_cleaning.py`` imported the implementation from
``scripts/make_clean_dataset.py``.
"""

from __future__ import annotations

import html
import re
from typing import Any

import pandas as pd


# map each source distribution code to its final binary feature column
DISTRIBUTION_FEATURES = {
    "G": "distribution_G_global_type",
    "F": "distribution_F_finnish_baltic_sea",
    "E": "distribution_E_europe_general",
    "En": "distribution_En_northern_europe",
    "Ew": "distribution_Ew_western_europe_americas",
    "Es": "distribution_Es_southern_europe",
    "Ee": "distribution_Ee_eastern_europe",
    "Eb": "distribution_Eb_balkans",
    "A": "distribution_A_sub_saharan_africa",
    "I": "distribution_I_islamic_cultures",
    "O": "distribution_O_older_asiatic_cultures",
    "P": "distribution_P_pacific_area",
}

# preserve the results of the original manual language audit
NON_ENGLISH_PRIMARY_TEXT_AUDIT = {
    "A3c-31": "German primary text",
    "C1b-20": "German primary text",
    "C1d-23": "Latin primary text",
    "C4d-21": "Mixed English/German primary text",
    "C4h-14": "German primary text",
    "C4h-17": "German primary text",
    "D2a-21": "German primary text",
    "D3e-20b": "Italian primary text",
    "D4c-17b": "German primary text",
    "E1g-22": "German primary text",
    "E1k-26": "German primary text",
    "F1a-13": "French borrowed phrase, not English prose",
    "F2c-10": "German primary text",
    "G3b-26": "German primary text",
    "G5c-10": "French primary text",
    "G6e-13": "German primary text",
    "G8a-18": "German primary text",
    "G8d-15": "German primary text",
    "H3h-11": "German primary text",
    "H6d-12": "German primary text",
    "H7a-17": "Latin primary text",
    "H7m-22": "German primary text",
    "J1e-25": "Latin primary text",
    "J1k-25": "Latin primary text",
    "K1k-27": "German primary text",
    "K1m-20": "German primary text",
    "L1b-23": "German primary text",
    "M1d-10": "French primary text",
    "M1e-11": "German primary text",
    "M3d-29": "German primary text",
    "M4c-16": "German primary text",
    "M9d-10": "German primary text",
    "T4a-11": "German primary text",
    "T4e-19": "French primary text",
}

LANGUAGE_NAMES = [
    "Arabic",
    "Chinese",
    "Czech",
    "Danish",
    "Dutch",
    "English",
    "Estonian",
    "Finnish",
    "French",
    "German",
    "Greek",
    "Hebrew",
    "Hindi",
    "Hungarian",
    "Icelandic",
    "Italian",
    "Japanese",
    "Korean",
    "Latin",
    "Lithuanian",
    "Norwegian",
    "Persian",
    "Polish",
    "Portuguese",
    "Romanian",
    "Russian",
    "Sanskrit",
    "Spanish",
    "Swedish",
    "Turkish",
    "Welsh",
]
LANGUAGE_NAME_MAP = {name.casefold(): name for name in LANGUAGE_NAMES}

# match language tags and translation markers found at the end of proverb text
PARENTHETICAL_PATTERN = re.compile(r"\(([^()]*)\)")
TRANSLATION_LABEL_PATTERN = (
    r"[A-Za-z][A-Za-z0-9 .,'’&-]*"
    r"(?:/[A-Za-z0-9][A-Za-z0-9 .,'’&-]*)*"
)
ABBREVIATED_TRANSLATION_PATTERN = re.compile(
    rf"\b(?:trl|tr)(?:\.\s*|\s+)(?P<label>{TRANSLATION_LABEL_PATTERN})\s*$",
    flags=re.IGNORECASE,
)
TRANSLATED_PATTERN = re.compile(
    rf"\btranslated(?:\s+from)?\s+(?P<label>{TRANSLATION_LABEL_PATTERN})\s*$",
    flags=re.IGNORECASE,
)

RENAMES = {
    "id": "source_id",
    "codeunive3": "universal_code",
    "nbunive3": "universal_number",
    "proverbtype": "proverb_type",
    "name": "slug",
    "missing": "missing_marker",
    "code": "subgroup_code",
    "nb": "type_number",
    "ref": "cross_references",
    "specificref": "specific_reference",
    "levinneisyys": "distribution",
}

# these source fields contain duplicate versions of the same typology values
DUPLICATE_PAIRS = [
    ("subgroup_code", "universal_code"),
    ("type_number", "universal_number"),
]

TYPOLOGY_FIELDS = {
    "subgroup_code",
    "type_number",
    "universal_code",
    "universal_number",
}

# define the complete intermediate schema before redundant source fields are removed
OUTPUT_COLUMNS = [
    "source_id",
    "kuusi_id",
    "theme",
    "main_class",
    "subgroup_code",
    "type_number",
    "universal_code",
    "universal_number",
    "proverb_original",
    "proverb_variant_1",
    "proverb_variant_2",
    "proverb_variant_3",
    "proverb_variant_4",
    "proverb_variant_extra",
    "proverb_primary_en",
    "proverb_primary_en_is_english",
    "proverb_parse_warning",
    "language_tags_raw",
    "translation_tag_types",
    "language_names_extracted",
    "has_language_or_translation_tag",
    "slug",
    "missing_marker",
    "cross_references",
    "specific_reference",
    "distribution",
    *DISTRIBUTION_FEATURES.values(),
]

# remove the duplicate universal fields from the final 36-column corpus
FINAL_COLUMNS = [
    column
    for column in OUTPUT_COLUMNS
    if column not in {"universal_code", "universal_number"}
]


def _normalize(value: Any) -> str | None:
    """return a trimmed string, treating pandas and json nulls as missing."""

    # handle both python nulls and pandas missing values
    if value is None:
        return None
    try:
        if pd.isna(value):
            return None
    except (TypeError, ValueError):
        pass
    normalized = str(value).strip()
    return normalized if normalized else None


def _stored_string(value: Any) -> str:
    # store missing text as an empty string for consistent csv output
    return _normalize(value) or ""


def _decode_source_value(value: Any) -> Any:
    # decode html entities while leaving non-string source values unchanged
    if value is None:
        return None
    try:
        if pd.isna(value):
            return None
    except (TypeError, ValueError):
        pass
    return html.unescape(value) if isinstance(value, str) else value


def _ordered_unique(values: list[str]) -> list[str]:
    # remove duplicates without changing their original order
    return list(dict.fromkeys(values))


def _prepare_rows(raw: pd.DataFrame) -> list[dict[str, Any]]:
    """standardize source names and remove unusable source records."""

    if not isinstance(raw, pd.DataFrame):
        raise TypeError("raw must be a pandas DataFrame")

    rows: list[dict[str, Any]] = []
    for raw_row in raw.to_dict(orient="records"):
        row = {
            RENAMES.get(column, column): _decode_source_value(value)
            for column, value in raw_row.items()
        }

        # the source contains one row without a usable proverb-type value
        if _normalize(row.get("proverb_type")) is None:
            continue

        # typology fields are stored as strings so identifiers remain stable
        for field in TYPOLOGY_FIELDS:
            row[field] = _stored_string(row.get(field))
        rows.append(row)

    return rows


def _backfill_canonical_values(
    rows: list[dict[str, Any]],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    """fill missing canonical fields and record any conflicting duplicates."""

    backfills = []
    conflicts = []

    for row_number, row in enumerate(rows, start=1):
        for canonical, universal in DUPLICATE_PAIRS:
            canonical_value = _normalize(row.get(canonical))
            universal_value = _normalize(row.get(universal))

            # use the equivalent universal value only when the canonical field is empty
            if canonical_value is None and universal_value is not None:
                row[canonical] = universal_value
                backfills.append(
                    {
                        "row": row_number,
                        "field": canonical,
                        "value": universal_value,
                    }
                )
            elif (
                canonical_value is not None
                and universal_value is not None
                and canonical_value != universal_value
            ):
                conflicts.append(
                    {
                        "row": row_number,
                        "field": canonical,
                        "canonical_value": canonical_value,
                        "universal_value": universal_value,
                    }
                )

    return backfills, conflicts


def _add_identifiers(rows: list[dict[str, Any]]) -> None:
    """construct canonical ids and hierarchy fields from subgroup codes."""

    for row in rows:
        subgroup_code = _normalize(row.get("subgroup_code"))
        type_number = _normalize(row.get("type_number"))

        row["kuusi_id"] = (
            f"{subgroup_code}-{type_number}"
            if subgroup_code is not None and type_number is not None
            else ""
        )
        row["theme"] = subgroup_code[0] if subgroup_code else ""

        if subgroup_code:
            # the main class is the leading letter followed by any digits
            prefix_length = 1
            while (
                prefix_length < len(subgroup_code)
                and subgroup_code[prefix_length].isdigit()
            ):
                prefix_length += 1
            row["main_class"] = (
                subgroup_code[:prefix_length] if prefix_length > 1 else ""
            )
        else:
            row["main_class"] = ""


def _parenthetical_language(value: str) -> str | None:
    # normalize case and spacing before checking the approved language list
    normalized = re.sub(r"\s+", " ", value).strip().casefold()
    return LANGUAGE_NAME_MAP.get(normalized)


def _translation_marker(value: str) -> re.Match[str] | None:
    # support both abbreviated and fully written translation markers
    return ABBREVIATED_TRANSLATION_PATTERN.search(
        value
    ) or TRANSLATED_PATTERN.search(value)


def _metadata_events(
    value: str,
    include_translation_marker: bool = True,
) -> list[dict[str, Any]]:
    """extract language and translation metadata with source positions."""

    events = []

    # treat only recognized language names as language metadata
    for match in PARENTHETICAL_PATTERN.finditer(value):
        language_name = _parenthetical_language(match.group(1))
        if language_name is not None:
            events.append(
                {
                    "start": match.start(),
                    "raw_tag": match.group(0),
                    "normalized_type": "parenthetical_language",
                    "language_name": language_name,
                }
            )

    if include_translation_marker:
        # translation markers are expected at the end of the text
        match = _translation_marker(value)
        if match is not None:
            events.append(
                {
                    "start": match.start(),
                    "raw_tag": match.group(0).strip(),
                    "normalized_type": "translation_marker",
                    "language_name": match.group("label").strip(),
                }
            )

    return sorted(events, key=lambda event: event["start"])


def _clean_primary_proverb(value: str) -> tuple[str, bool]:
    """remove recognized metadata from the primary proverb text."""

    def remove_language_tag(match: re.Match[str]) -> str:
        if _parenthetical_language(match.group(1)) is not None:
            return ""
        return match.group(0)

    cleaned = PARENTHETICAL_PATTERN.sub(remove_language_tag, value)
    translation_match = _translation_marker(cleaned)
    if translation_match is not None:
        cleaned = cleaned[: translation_match.start()]
    cleaned = re.sub(r"\s+", " ", cleaned).strip()

    # remaining parentheses may contain uncertain metadata that needs review
    return cleaned, bool(PARENTHETICAL_PATTERN.search(cleaned))


def _add_proverb_fields(rows: list[dict[str, Any]]) -> None:
    """preserve original text and split slash-delimited proverb variants."""

    for row in rows:
        original_value = row.get("proverb_type")
        original = "" if original_value is None else str(original_value)
        row["proverb_original"] = original

        variants = [
            segment.strip()
            for segment in original.split("/")
            if segment.strip()
        ]
        # keep the first four variants in dedicated analysis columns
        for number in range(1, 5):
            row[f"proverb_variant_{number}"] = (
                variants[number - 1] if len(variants) >= number else ""
            )
        row["proverb_variant_extra"] = (
            " / ".join(variants[4:]) if len(variants) > 4 else ""
        )

        # use the cleaned first variant as the default modeling text
        primary_source = variants[0] if variants else ""
        primary, uncertain_metadata = _clean_primary_proverb(primary_source)
        row["proverb_primary_en"] = primary

        warnings = []
        # record parsing issues instead of silently discarding uncertainty
        if _normalize(original) is None:
            warnings.append("empty_original")
        if _normalize(primary) is None:
            warnings.append("empty_primary_after_cleaning")
        if len(variants) > 4:
            warnings.append("many_variants")
        if uncertain_metadata:
            warnings.append("uncertain_language_metadata")
        row["proverb_parse_warning"] = ";".join(warnings) if warnings else "ok"


def _add_primary_english_flags(rows: list[dict[str, Any]]) -> None:
    """flag primary texts using the completed manual language audit."""

    for row in rows:
        kuusi_id = row.get("kuusi_id", "")
        if _normalize(row.get("proverb_primary_en")) is None:
            row["proverb_primary_en_is_english"] = "0"
        elif kuusi_id in NON_ENGLISH_PRIMARY_TEXT_AUDIT:
            row["proverb_primary_en_is_english"] = "0"
        else:
            row["proverb_primary_en_is_english"] = "1"


def _add_language_metadata(rows: list[dict[str, Any]]) -> None:
    """collect language metadata across the original text and all variants."""

    variant_columns = [
        "proverb_variant_1",
        "proverb_variant_2",
        "proverb_variant_3",
        "proverb_variant_4",
        "proverb_variant_extra",
    ]

    for row in rows:
        events = _metadata_events(row["proverb_original"])
        # avoid recording the same trailing translation marker once per variant
        original_has_translation_marker = any(
            event["normalized_type"] == "translation_marker"
            for event in events
        )

        for column in variant_columns:
            events.extend(
                _metadata_events(
                    row.get(column, ""),
                    include_translation_marker=not original_has_translation_marker,
                )
            )

        unique_events = []
        seen = set()
        # deduplicate metadata while preserving its first observed order
        for event in events:
            key = (
                event["raw_tag"],
                event["normalized_type"],
                event["language_name"],
            )
            if key not in seen:
                seen.add(key)
                unique_events.append(event)

        row["language_tags_raw"] = "|".join(
            _ordered_unique([event["raw_tag"] for event in unique_events])
        )
        row["translation_tag_types"] = "|".join(
            _ordered_unique(
                [event["normalized_type"] for event in unique_events]
            )
        )
        row["language_names_extracted"] = "|".join(
            _ordered_unique(
                [event["language_name"] for event in unique_events]
            )
        )
        row["has_language_or_translation_tag"] = (
            "1" if unique_events else "0"
        )


def _stored_distribution(value: Any) -> str:
    # preserve the original distribution string and normalize only missing values
    if value is None:
        return ""
    try:
        if pd.isna(value):
            return ""
    except (TypeError, ValueError):
        pass
    return str(value)


def _add_distribution_features(rows: list[dict[str, Any]]) -> None:
    """expand comma-separated distribution codes into binary columns."""

    known_codes = set(DISTRIBUTION_FEATURES)

    for row_number, row in enumerate(rows, start=1):
        distribution = _stored_distribution(row.get("distribution"))
        row["distribution"] = distribution
        codes = {
            code.strip()
            for code in distribution.split(",")
            if code.strip()
        }

        unknown_codes = codes - known_codes
        # fail loudly if the source introduces a code not covered by the schema
        if unknown_codes:
            raise ValueError(
                f"Unknown distribution code(s) on row {row_number}: "
                + ", ".join(sorted(unknown_codes))
            )

        for code, column in DISTRIBUTION_FEATURES.items():
            row[column] = int(code in codes)


def clean_kuusi_data(raw: pd.DataFrame) -> pd.DataFrame:
    """transform the raw kuusi snapshot into the analysis-ready corpus.

    the function does not modify ``raw``. it removes the single source record
    without a proverb type, backfills missing canonical identifiers, parses
    proverb variants and language metadata, expands distribution codes, and
    returns the established 36-column schema.
    """

    # run each cleaning stage in the order required by later transformations
    rows = _prepare_rows(raw)
    _, conflicts = _backfill_canonical_values(rows)

    # conflicting duplicate identifiers would make canonical ids unreliable
    if conflicts:
        conflict_rows = ", ".join(str(item["row"]) for item in conflicts)
        raise ValueError(
            "Canonical and universal identifier fields conflict on row(s): "
            + conflict_rows
        )

    _add_identifiers(rows)
    _add_proverb_fields(rows)
    _add_primary_english_flags(rows)
    _add_language_metadata(rows)
    _add_distribution_features(rows)

    # select and order the final schema without carrying forward source-only fields
    clean = pd.DataFrame(
        [
            {column: row.get(column, "") for column in FINAL_COLUMNS}
            for row in rows
        ],
        columns=FINAL_COLUMNS,
    )
    return clean


def validate_clean_data(clean: pd.DataFrame) -> dict[str, int]:
    """validate the final project corpus and return a compact summary.

    raises ``valueerror`` when a project invariant fails.
    """

    if not isinstance(clean, pd.DataFrame):
        raise TypeError("clean must be a pandas DataFrame")

    if clean.shape != (1_727, 36):
        raise ValueError(
            "Expected a 1,727-row × 36-column corpus, found "
            f"{clean.shape[0]:,} rows × {clean.shape[1]:,} columns"
        )

    missing_columns = set(FINAL_COLUMNS) - set(clean.columns)
    if missing_columns:
        raise ValueError(
            "Missing required columns: " + ", ".join(sorted(missing_columns))
        )

    if list(clean.columns) != FINAL_COLUMNS:
        raise ValueError("The cleaned columns are not in the expected order")

    # every record must have one unique and reconstructable canonical identifier
    if clean["kuusi_id"].isna().any() or clean["kuusi_id"].eq("").any():
        raise ValueError("Missing kuusi_id values remain")
    if clean["kuusi_id"].duplicated().any():
        raise ValueError("Duplicate kuusi_id values remain")

    reconstructed_ids = (
        clean["subgroup_code"].astype(str)
        + "-"
        + clean["type_number"].astype(str)
    )
    if not clean["kuusi_id"].astype(str).equals(reconstructed_ids):
        raise ValueError(
            "At least one kuusi_id cannot be reconstructed from its components"
        )

    if (
        clean["proverb_primary_en"].isna().any()
        or clean["proverb_primary_en"].astype(str).str.strip().eq("").any()
    ):
        raise ValueError("Missing proverb_primary_en values remain")

    # confirm that each binary feature exactly matches its source distribution code
    for code, column in DISTRIBUTION_FEATURES.items():
        if not clean[column].isin([0, 1]).all():
            raise ValueError(f"{column} contains non-binary values")

        expected = clean["distribution"].fillna("").map(
            lambda value: int(
                code
                in {
                    item.strip()
                    for item in str(value).split(",")
                    if item.strip()
                }
            )
        )
        if not clean[column].equals(expected):
            raise ValueError(f"{column} does not match distribution")

    # return a compact validation summary for display in the notebook
    summary = {
        "records": len(clean),
        "fields": clean.shape[1],
        "missing_canonical_ids": int(clean["kuusi_id"].isna().sum()),
        "duplicate_canonical_ids": int(clean["kuusi_id"].duplicated().sum()),
        "missing_primary_texts": int(
            clean["proverb_primary_en"].isna().sum()
        ),
    }
    print("Validation passed:", summary)
    return summary


__all__ = ["clean_kuusi_data", "validate_clean_data"]