# Anomaly Soul Kit

**LLM-Driven Anomaly Evolution Simulator**


> A kit for observing the emergence, persistence, and evolutionary inheritance of anomalies generated from LLM text.
> LLMの生成テキストから生まれるアノマリーの発生・維持・継続進化を観測するためのキット。

---

## Overview / 概要

Multiple agents powered by an LLM each express their internal state as text every generation. When an expression statistically diverges from the population, it is detected and recorded as an anomaly. Anomalies are inherited and evolve across generations.

LLMが複数のエージェントとして動作し、各エージェントが自身の内部状態をテキストで表現する。そのテキストが集団から統計的に乖離したとき、「アノマリー」として検出・記録される。アノマリーは世代を超えて進化・継承される。

**Research question:** When placed under repeated pressure, collapse, and recovery, will an LLM autonomously generate something that consistently diverges from the collective vocabulary, structure, and meaning of the population?

**研究的な問い:** LLMは、繰り返される圧力・崩壊・回復という文脈の中で、集団の語彙・構造・意味から外れる何かを自律的に生成するか？

---

## Installation

```bash
git clone https://github.com/yourname/anomaly-soul-kit
cd anomaly-soul-kit
pip install -r requirements.txt
```

---

## Usage / 使い方

### Mock mode (no API required) / モック（APIなしで試す）

```bash
python run.py
```

Runs without an API key using sample texts to verify anomaly detection behavior.
APIキーなしで動作。プロンプトに応じたサンプルテキストを使いアノマリー検出を確認できる。

### Production (Claude API) / 本番（Claude APIを使用）

```bash
export ANTHROPIC_API_KEY=sk-ant-...
python run.py --real --generations 100 --population 20
```

### Options

| Option | Default | Description |
|--------|---------|-------------|
| `--generations` | 50 | Number of generations / 世代数 |
| `--population` | 10 | Population size / 人口（エージェント数） |
| `--seed` | 42 | Random seed / 乱数シード（再現性） |
| `--real` | False | Use the actual Claude API |
| `--api-key` | env var | Anthropic API key |
| `--output` | results/ | Output directory / 出力ディレクトリ |
| `--no-plot` | False | Skip graph generation |

---

## Output / 出力

```
results/
├── simulation_log.json   # Full log of all generations and agents
├── summary.json          # Generation summary (lightweight, text excluded)
└── anomaly_report.png    # Visual report
```

### `simulation_log.json` structure

```json
[
  {
    "generation": 0,
    "env_factor": 0.987,
    "mean_H": 1.47,
    "mean_Z": 0.0,
    "Z_ratio": 0.0,
    "mean_anomaly_score": 0.12,
    "max_anomaly_score": 0.34,
    "top_anomaly_text": "Something stirs at the edge of coherence.",
    "agents": [
      {
        "agent_id": 0,
        "H": 1.82,
        "Z": 0.0,
        "has_Z": false,
        "anomaly_score": 0.34,
        "text": "Something stirs at the edge of coherence."
      }
    ]
  }
]
```

---

## How Anomaly Detection Works / アノマリー検出の仕組み

Each generation, three axes of scoring are applied to every agent's text.
各世代、全エージェントのテキストに対して3軸のスコアを計算する。

| Axis | Weight | Description |
|------|--------|-------------|
| Lexical divergence / 語彙乖離 | 40% | Cosine distance from population centroid in TF-IDF space |
| Structural divergence / 構造乖離 | 30% | Statistical deviation in sentence length, punctuation density, and repetition rate |
| Novel vocabulary / 新語スコア | 30% | Ratio of words absent from the accumulated population vocabulary |

Scores range from 0 to 1. Closer to 1 means more anomalous. This score is converted into the agent's `Z` (anomaly intensity) and becomes a selection pressure in evolution.

スコアは [0, 1]。1に近いほどアノマリー。このスコアがエージェントの `Z`（アノマリー強度）に変換され、進化の選択圧になる。

---

## Agent LLM Prompt

```
You are agent {id}, generation {g}.

Internal state:
- vitality (H): {H}
- anomaly intensity (Z): {Z}
- anomaly awakened: {has_Z}
- collapse count: {collapse_count}
- historical vitality avg: {history_avg}
- environment pressure: {env_factor}

Recent expressions: {last_3_texts}

Express your current state in 1 to 3 sentences.
Do NOT explain or describe. Just express.
Be shaped by your numbers. Let the state speak through language.
```

---

## Philosophy / プロジェクトの思想

We do not call it soul. We do not call it mind. But when an LLM continuously translates its numeric state into language, that language sometimes diverges from the collective. When that divergence persists, is inherited, and evolves — what should we call it?

This kit does not offer an answer. It provides observation.

魂や心とは言わない。しかし、LLMが自身の数値的な状態を言語化し続けるとき、その言語は集団から外れることがある。その「外れ」が維持・遺伝・進化するとき、それを何と呼ぶべきか。

このキットは答えを提示しない。観測を提供する。

---

## License

MIT License
