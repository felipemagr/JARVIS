# jarvis

- **Version**  1.1.0

- **Author:** Felipe Macías Granado

> **Note:** This project was originally developed in mid-2025 as a take-home coding assignment for a SF-based company, which was successfully passed. It is now being released as a public repository. The developer landscape has certainly evolved since then, but this may still serve as a useful reference for someone.

## Objetive
JARVIS is a playful nod to Tony Stark’s legendary AI assistant. The main goal of this project is to develop a REST API that allows users to index and query their documents within a Vector Database.

## Release Notes

* `1.0.0` Stable baseline.
* `1.1.0` Add filtering of metadata.

## Pre-requirements

- Python 3.11
- Podman/Docker

### Environment variables

To ensure the service runs correctly, the required environment variables must be declared in the `Config` class. This centralizes configuration and ensures that all necessary values are accessible within the application. Make sure to define all static or deployment-specific variables in the `Config` class unless they are explicitly meant to be loaded from a `.env` file.

## How to start

Build the project (install poetry + create a virtual environment + install dependencies):
```
make build
```

Activate the created virtual environment:
```
make shell
```

List the available commands:
```
make help
```

## Running the application
### Local
```
python src/jarvis/main.py
```

### No Docker
#### Development
```
python src/jarvis/run.py --reload --log-level debug
```

#### Production
```
python src/jarvis/run.py --host 0.0.0.0 --port 8000 --log-level info
```

### Docker
```
make docker-build
make docker-run
```

## Calling the API
Once the application is running, you can test the available endpoints using the provided Postman collection, located at: `data/JARVIS.postman_collection.json`

## Design decisions & justifications

- Sample data has been generated with OpenAI's GPT-4.1-mini.
- To prevent data races during concurrent reads and writes, all access to the in-memory index data is protected by a reentrant lock (threading.RLock). This ensures that only one thread can modify or read the shared data at a time.
- The `Ingestor` class is a dedicated service responsible for ingesting and processing raw data from JSON files, i.e., performing ETL (Extract, Transform, Load). It handles parsing documents, splitting them into token chunks, generating embeddings via Cohere API, and structuring domain objects. It encapsulates ingestion logic separately from API endpoints and the vectorstore persistence layer.

### Indexing algorithms

#### LinearKNN

- **Space Complexity:** O(n*d) — stores vectors of dimension d.
- **Time Complexity:** O(n*d) per similarity calculation.
- **Reason for Choice:**
  A straightforward brute-force method serving as a baseline. It makes no assumptions about the vector structure and is simple to implement. However, it is inefficient for large datasets since it performs linear comparisons across all vectors.

#### HierarchicalKNN

- **Space Complexity:** >O(n*d) — stores hierarchical weights and vectors.
- **Time Complexity:** >O(n*d) per scoring, slightly higher than LinearKNN due to the weighting computations.
- **Reason for Choice:**  
  Incorporates hierarchical weighting of dimensions, based on the assumption that earlier dimensions carry more importance. This approach aims to improve similarity scoring by emphasizing important features and is especially useful when vector dimensions have differing significance.

### Metadata filtering

- **Approach:**  
  The metadata filtering was fairly easy. It is just a matter of introducing a filter with the desired metadata as an optional parameter in VectorStore.query_index(). If the filter is not empty -> we keep the data from index_data that matches (aka let's copy the variable index_data, do the filtering, and use it for the search). ✅ (see v1.1.0).
