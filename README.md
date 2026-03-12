# Movie Score Pipeline

A small data pipeline that ingests, cleans, standardizes, and merges movie data from multiple providers into a single
unified dataset.

The resulting dataset is designed to be easily queried by a data science team.

---

## Overview

The pipeline processes movie data coming from different providers with heterogeneous formats (CSV, JSON, multiple
files). Each provider is responsible for:

* fetching the raw data
* cleaning and standardizing fields
* returning normalized `MovieScore` objects

The pipeline then merges the standardized records into a single dataset and exports it as a unified CSV file.

The final output can be found in:

```
data/output/unified_movies.csv
```

---

## Architecture

The project follows a modular structure:

```
data/
  input/          raw provider files
  output/         generated dataset

models/
  movie_score_model.py

src/
  providers/      provider-specific ingestion logic
  movie_merger.py merging logic
  pipeline.py     pipeline orchestration

test/             unit and integration tests
```

Responsibilities are separated as follows:

* **Providers** handle ingestion and normalization of each data source.
* **Merger** combines records coming from different providers.
* **Pipeline** orchestrates the full process.

---

## Adding New Providers

The pipeline is designed to support multiple providers.

To add a new provider:

1. Extend the `MovieScore` model if new fields are required.
2. Implement a new provider class inside `src/providers`.
3. Register the provider in the pipeline configuration.

No changes to the core pipeline logic are required.

---

## Prerequisites

This project is built using **Python 3.9+**.

Ensure you have a virtual environment set up and the necessary dependencies installed:

```bash
# Create virtual environment (optional but recommended)
python -m venv .venv
source .venv/bin/activate  # On Windows use: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

---

## Running the Pipeline

From the project root:

```bash
python main.py
```

This will execute the full pipeline and generate the unified dataset.

---

## Running the Tests

Tests are implemented using pytest.

Run all tests with:

```bash
python -m pytest -v
```

---

## Future Improvements

* Introduce a `ConflictSolver` component to handle cases where providers return conflicting non-null values during the
  merge step. This could support configurable strategies (e.g., prioritizing the most recently updated value or applying
  provider-specific precedence rules).
* Strengthen the data validation layer to enforce stricter constraints and improve robustness when handling malformed or
  inconsistent input data.
* Further standardize the `fetch` and `transform` methods in the base provider class. Much of the current logic is
  similar across
  providers (e.g., reading data with
  pandas), so additional abstraction could reduce duplication and improve consistency.
