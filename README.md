# jarvis

- **Version**  0.1.0

- **Author:** felipe

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

## Design decisions

- I removed the `Library` class because its functionality overlapped with the `VectorStore` class. In my view, both classes served the same purpose, so only `VectorStore` was retained.