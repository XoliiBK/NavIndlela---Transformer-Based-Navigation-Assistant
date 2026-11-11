# NavIndlela 

I'm building this to understand how language models actually work, not just how to call one through an API. NavIndlela is a navigation assistant for a fictional town: a small transformer language model, trained from scratch on synthetic route data, wrapped in a system that checks every route it generates against a traditional pathfinding algorithm.

Navigation is a good test case because the correct answer is known. A pathfinder can say exactly what the right route is, so I can measure the model instead of guessing how good it is.

> **Status: in development.** Nothing below is claimed as finished until its checkbox is ticked and the results table has real numbers.

## What it does

1. **Guided input**: Pick where you are and where you're going from dropdowns (street, then building). No typing sentences, and no misread place names.

2. **Route generation**: A small transformer trained from scratch generates the route in a compact format, for example `L MILL_ST | R CHURCH_RD | ARRIVE BAKERY`.

3. **Verification layer**: Every generated route is checked against a Dijkstra pathfinder: valid streets, valid turns, one-way roads respected, and the destination actually reached.

4. **Automatic fallback**: If the model's route fails verification, the pathfinder's route is returned instead and flagged as a fallback, so the user only ever receives a valid route.

5. **Schematic route graph**: A clean graph of intersections and streets with the route highlighted and step-by-step instructions. Left and right come from the map geometry, so the picture never depends on parsing model text.

6. **Evaluation harness**: Tests the model on place pairs held out of training and measures accuracy, invented-street rate, accuracy by route length, fallback rate and latency.

7. **Request logging**: Logs latency and whether each answer came from the model or the fallback.

## How it works

1. Pick your start and destination from the guided inputs
2. The resolver turns your choices into place IDs
3. The small GPT generates a compact route
4. The verifier compares it with the pathfinder's route
5. Valid: the model's route is used. Invalid: the pathfinder's route is used and flagged
6. The UI draws the route on the graph with step-by-step instructions
7. The request is logged

```
Guided input -> resolver -> small GPT -> verifier vs pathfinder
                                              |            |
                                            valid       invalid
                                              |            |
                                        model route   pathfinder route (flagged)
                                              \            /
                                         UI graph + step-by-step -> log
```

## Tech stack

- **Backend:** Python, FastAPI
- **Model:** PyTorch (small GPT, word-level tokenizer)
- **Algorithms:** Dijkstra pathfinder with one-way support
- **Data handling:** JSON town file, generated training data with a saved held-out split
- **Frontend:** HTML, CSS, JavaScript, inline SVG
- **Testing:** pytest
- **Logging:** JSONL
- **Training:** Free Colab or Kaggle GPU

## Getting started

Setup instructions will be added as each component lands. The plan is Python 3.10+, a virtual environment, `pip install -r requirements.txt`, then scripts to generate data, train the model and run the app.

## Data structure

The town is stored as a JSON file:

- **places**: id, name, street, attached intersection
- **intersections**: id, x/y coordinates (used for drawing the graph)
- **segments**: from, to, street name, one-way flag

Training data is generated from the pathfinder. Every ordered pair of places becomes an example:

```
FROM library TO bakery => L MILL_ST | R CHURCH_RD | ARRIVE BAKERY
```

About 20% of place pairs are held out of training. The split is saved to disk and the random seeds are fixed, so the evaluation is reproducible.

## Evaluation

| Metric | Result |
|---|---|
| Exact-match accuracy, seen pairs | _pending_ |
| Exact-match accuracy, held-out pairs | _pending_ |
| Invented street or turn rate | _pending_ |
| Accuracy by route length | _pending_ |
| Fallback rate | _pending_ |
| Latency (p50 / p95) | _pending_ |

A "what failed and why" analysis will go here once there are results.

## Scope and limitations

- It only works for this one fictional town and these structured inputs.
- It's a small model trained on a small synthetic dataset. This is a learning project, not a production system.
- The pathfinder already solves routing perfectly. The point is to study how well a small model can learn the task, and how to deploy a model that can't be fully trusted.

## What I'm aiming to demonstrate

- Training a transformer from scratch: tokenization, training loop, train/validation split
- Synthetic data generation for a narrow domain
- Validating model output, with a deterministic fallback
- Evaluating against ground truth, including held-out generalization
- Serving a model through an API with logging
- Reporting results honestly, including failures

## What's missing / what's next

- [ ] Town data (`town.json`) with automated graph tests
- [ ] Dijkstra pathfinder with tests
- [ ] Synthetic data generator and saved split
- [ ] Word-level tokenizer
- [ ] Small GPT, training loop and loss curve
- [ ] Verifier and fallback layer
- [ ] Evaluation harness and results table
- [ ] FastAPI service with request logging
- [ ] Single-page UI with guided input and route graph
- [ ] Demo recording

Later ideas:
- Natural-language phrasing in the output
- Free-text place lookup using embedding-based retrieval
- Tool calling and an agent version, with the pathfinder exposed as an MCP tool
- Voice output and a larger town

## Status

In development. Built as a learning-focused project and not production-ready.


