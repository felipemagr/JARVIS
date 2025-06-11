# jarvis

- **Version**  0.1.0

- **Author:** Felipe Macías Granado

- **Contact:** felipemaciasgranado@gmail.com

## Objetive
TBD

## Pre-requirements

- Python 3.11

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

## Disclaimer
> I am a new wave developer, therefore I use generative AI in my workflow. I typically break problems down into smaller tasks and use AI selectively to assist with these. However, this does not mean the code is fully AI-generated, as I prioritize my own critical thinking and creativity throughout the process. I also use AI to help generate synthetic data and to improve comments and docstrings. The underlying logic, ideas, and overall design are entirely my own. Technologies/Models used (free limited accounts): Copilot, GPT-4o/GPT-4.1-mini and, mainly, Claude Sonnet 4 ([and this is why](https://livebench.ai/#/)).

## Design decisions

- I removed the `Library` class because its functionality overlapped with the `VectorStore` class. In my view, both classes served the same purpose, so only `VectorStore` was retained. The `VectorStore` class is therefore a store of the chunks and documents.
- I used tiktoken because the cohere client tokenizer is a bit of a nightmare. With more time I would have read better the documentation, but I hope this decision is meaningless.
- Sample data has been generated with OpenAI's GPT-3.5.
- To prevent data races during concurrent reads and writes, all access to the in-memory index data is protected by a reentrant lock (threading.RLock). This ensures that only one thread can modify or read the shared data at a time.
- The `Ingestor` class is a dedicated service responsible for ingesting and processing raw data from JSON files, i.e., performing ETL (Extract, Transform, Load). It handles parsing documents, splitting them into token chunks, generating embeddings via Cohere API, and structuring domain objects. It encapsulates ingestion logic separately from API endpoints and the vectorstore persistence layer.
