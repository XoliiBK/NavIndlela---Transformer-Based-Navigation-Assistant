# NavIndlela 🗺️
### A Transformer-Based Navigation Assistant

NavIndlela is an experimental AI navigation assistant that explores how a small Transformer model can generate navigation directions within a fictional town.

The project uses a lightweight Transformer implemented and trained from scratch using PyTorch. It combines neural sequence generation with graph-based pathfinding and deterministic route verification to explore how AI-generated outputs can be made more reliable.

## Project Overview

NavIndlela operates within a simulated town consisting of streets, buildings, landmarks, and connected locations.

Users provide a starting address and a destination address through a guided address-entry interface. Each address consists of a street and a building.

The system then generates directions between the selected locations using a trained Transformer model. A verification layer checks the generated directions against the town's graph and pathfinding algorithm. If the generated directions are invalid, a pathfinding fallback provides a valid route.

Address suggestions are restricted to locations that exist within the fictional town. If an address cannot be found, the system returns a "Not found in this town" message rather than passing an invalid address to the model.

## Project Goals

NavIndlela is designed to explore three areas of AI engineering and software development:

- **Understanding Model Internals:** Demonstrate practical understanding of tokenisation, Transformer architecture, model training, held-out evaluation, and analysing model failures.
- **Engineering for Reliability:** Explore how deterministic verification and pathfinding fallbacks can make AI-generated outputs more reliable when model predictions cannot be fully trusted.
- **Measurable Evaluation:** Use the town's graph structure as ground truth to evaluate route accuracy, identify invalid predictions, and measure model performance using quantitative metrics rather than subjective assessment.

## Key Features

- **Guided Address Input:** Users select a starting address and destination using town-validated address suggestions.
- **Transformer-Based Route Generation:** A lightweight Transformer architecture is implemented and trained from scratch using PyTorch.
- **Synthetic Dataset Generation:** Training examples are generated from the fictional town's graph structure.
- **Graph-Based Navigation:** Represents streets and buildings as connected locations to support route generation and verification.
- **Route Verification:** Validates generated directions against the town graph, including street connectivity, one-way restrictions, and destination reachability.
- **Pathfinding Fallback:** Uses a deterministic pathfinding algorithm when the model generates an invalid route.
- **Model Evaluation and Request Logging:** Tracks model performance, route validity, fallback usage, and request latency.

## System Architecture

```text
       User
        |
        v
  Address Input
 (Start + Destination)
        |
        v
  Address Validation
        |
   +----+----+
   |         |
 Valid     Invalid
   |         |
   v         v
 Transformer  Not Found
   |          Response
   v
 Route Generation
   |
   v
 Route Verification
   |
 +--+-----------+
 |              |
Valid          Invalid
 |              |
 v              v
Return Route   Pathfinding
               Fallback
 |              |
 +------+-------+
        |
        v
 Navigation Directions
        |
        v
   Request Logging
```

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Core development |
| PyTorch | Transformer implementation and model training |
| FastAPI | Backend API development |

## Evaluation Strategy

The model and navigation pipeline will be evaluated using a held-out dataset to assess route generation accuracy, reliability, and performance.

| Metric | Purpose |
|---|---|
| Route Accuracy | Measures how accurately the model generates expected routes. |
| Valid Route Rate | Measures the proportion of generated routes that pass verification. |
| Invalid Street Rate | Measures how frequently the model generates streets or locations that do not exist. |
| Fallback Rate | Measures how frequently the pathfinding fallback is required because of invalid model-generated routes. |
| Request Latency | Measures the time taken to process a navigation request and return directions. |

Requests and their outcomes will also be logged to support debugging, performance analysis, and evaluation of the complete navigation pipeline.

## Limitations

NavIndlela operates within a controlled fictional town environment and is not intended for real-world navigation.

- **Restricted Environment:** Only streets, buildings, and connections defined within the town graph are supported.
- **Validated Inputs:** Users must select addresses that exist within the town. Arbitrary or unknown addresses are not supported.
- **Limited Training Data:** The Transformer is trained on a synthetic dataset generated from a predefined town structure. Its performance may not generalise beyond that environment.
- **Model Reliability:** The model may generate invalid or incomplete routes, which is why deterministic verification and pathfinding fallback are necessary.
- **Why Use a Transformer?** Traditional graph-based pathfinding algorithms can already calculate valid routes efficiently. NavIndlela uses a Transformer as an experimental approach to learning route generation from data, exploring sequence modelling, neural generation, and the reliability challenges associated with AI-generated outputs. The pathfinder remains the deterministic source of correctness.

## Project Structure

The planned project structure is:

```text
NavIndlela/
│
├── data/
│   ├── town_graph/
│   ├── generated/
│   └── processed/
│
├── src/
│   ├── data/
│   │   └── generator.py
│   │
│   ├── model/
│   │   ├── tokenizer.py
│   │   ├── transformer.py
│   │   └── train.py
│   │
│   ├── navigation/
│   │   ├── graph.py
│   │   ├── pathfinder.py
│   │   └── validator.py
│   │
│   ├── evaluation/
│   │   └── evaluate.py
│   │
│   └── api/
│       └── main.py
│
├── tests/
├── requirements.txt
└── README.md
```

*Note: The project structure is a proposed layout and may change during development.*

## Development Roadmap

- [ ] Design and implement the fictional town graph.
- [ ] Implement address lookup and validation.
- [ ] Develop synthetic navigation dataset generation.
- [ ] Implement tokenisation and preprocessing.
- [ ] Build a lightweight Transformer architecture from scratch.
- [ ] Train and evaluate the model.
- [ ] Implement model-based route generation.
- [ ] Develop route verification, including one-way street and destination checks.
- [ ] Implement graph-based pathfinding fallback.
- [ ] Build the FastAPI backend.
- [ ] Implement request logging and evaluation metrics.
- [ ] Test the complete navigation pipeline.

---

**Built with Python and PyTorch and .**
