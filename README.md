# jarvis

- **Version**  1.1.0

- **Author:** Felipe Macías Granado

- **Contact:** felipemaciasgranado@gmail.com

## Objetive
JARVIS is a playful nod to Tony Stark’s legendary AI assistant. And just like Stark’s AI, I wanted to prove that I have coding abilities and that I can do the proposed task fast. The main goal of this project is to develop a REST API that allows users to index and query their documents within a Vector Database.

## Disclaimer
> I am a new wave developer, therefore I use generative AI in my workflow. I typically break problems down into smaller tasks and use AI selectively to assist with these. However, this does not mean the code is fully AI-generated, as I prioritize my own critical thinking and creativity throughout the process. I also use AI to help generate synthetic data and to improve comments and docstrings. The underlying logic, ideas, and overall design are entirely my own. Technologies/Models used (free limited accounts): Copilot, GPT-4o/GPT-4.1-mini and, mainly, Claude Sonnet 4 ([and this is why](https://livebench.ai/#/)).

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

- I removed the `Library` class because its functionality overlapped with the `VectorStore` class. In my view, both classes served the same purpose, so only `VectorStore` was retained. The `VectorStore` class is therefore a store of the chunks and documents.
- I used tiktoken because the cohere client tokenizer is a bit of a nightmare. With more time I would have read better the documentation, but I hope this decision is meaningless.
- Sample data has been generated with OpenAI's GPT-4.1-mini.
- To prevent data races during concurrent reads and writes, all access to the in-memory index data is protected by a reentrant lock (threading.RLock). This ensures that only one thread can modify or read the shared data at a time.
- The `Ingestor` class is a dedicated service responsible for ingesting and processing raw data from JSON files, i.e., performing ETL (Extract, Transform, Load). It handles parsing documents, splitting them into token chunks, generating embeddings via Cohere API, and structuring domain objects. It encapsulates ingestion logic separately from API endpoints and the vectorstore persistence layer.
- I relied more on AI than I would have preferred when building the API, as this is the area where I have the least experience on. I've been working with APIs this whole last year, but this was my first time designing and building one from scratch.

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

### Testing

I did not complete the testing as I really need to hand this up on Wednesday's night (tomorrow I will need to go on person to the office and after I will start vacations). I am pretty familiar with the concept of testing, in fact, I have been doing tests for the past month (using pytest and unittest). Thankfully for all of us developers, Claude Sonnet 4 is a total dream for testing (you just need to double-check what it produces).

### Extra points

Due to time contraints and while also prioritising the speed I could come up with the solution (and show you I am indeed a wizard ;)), I could not spend any time on the extra points. I will explain how I would do them though, and I will probably take them up on Monday when I arrive from my vacations.

### 1. Metadata filtering & dinamic index body

- **Approach:**  
  The metadata filtering should be fairly easy. It is just a matter of introducing a filter with the desired metadata as an optional parameter in VectorStore.query_index(). If the filter is not empty -> we keep the data from index_data that matches (aka let's copy the variable index_data, do the filtering, and use it for the search). ✅ (see v1.1.0).

  The flexible index body is way trickier. First-thought, it can look easy, as you just need to change create_index to a more general approach. But this would trigger problems in how to query the indexes (and probably more stuff that does not come into my mind yet). I need to further think about this.

### 2. Persistence to Disk

- **Approach:**
  This is the first time I tackle a problem like this. But naively I would say: let's serialize the indexes data to disk regularly or upon shutdown. And on startup, let's reload the state to resume from the last checkpoint. Easy to say, but it looks a bit of a pain.

### 3. Leader-Follower Architecture

- **Approach:**  
  I am going to be totally honest here: this got me a bit off side, I need to catch up with this concept of "Leader-Follower Architecture within the Kubernetes cluster" before to even consider starting it.

### 4. Python SDK Client

- **Approach:**  
  Seems like a reasonable next step. In my current work I have just finished the creation of a library for my team (and probably soon for the whole bank), so I am familiar in what I would need to wrap the API calls with interfaces more user-friendly.
