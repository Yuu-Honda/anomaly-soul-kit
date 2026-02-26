## “””
run.py

エントリーポイント。コマンドラインから実行する。

使い方:

# モック（APIなし）で試す

python run.py

# 本番（Claude API使用）

export ANTHROPIC_API_KEY=sk-ant-…
python run.py –real –generations 100 –population 20

# パラメータ一覧

python run.py –help
“””

import argparse
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(**file**).parent))

from simulation import run_simulation
from visualize  import plot_results

def main():
parser = argparse.ArgumentParser(
description=“Anomaly Soul Kit — LLM Anomaly Evolution Simulator”
)
parser.add_argument(”–generations”,  type=int,   default=50,       help=“世代数 (default: 50)”)
parser.add_argument(”–population”,   type=int,   default=10,       help=“人口 (default: 10)”)
parser.add_argument(”–seed”,         type=int,   default=42,       help=“乱数シード (default: 42)”)
parser.add_argument(”–real”,         action=“store_true”,          help=“実際のClaude APIを使用”)
parser.add_argument(”–api-key”,      type=str,   default=None,     help=“Anthropic APIキー（環境変数でも可）”)
parser.add_argument(”–output”,       type=str,   default=“results”, help=“出力ディレクトリ (default: results)”)
parser.add_argument(”–no-plot”,      action=“store_true”,          help=“グラフ生成をスキップ”)
parser.add_argument(”–quiet”,        action=“store_true”,          help=“詳細ログを非表示”)

```
args = parser.parse_args()

mock    = not args.real
api_key = args.api_key or os.environ.get("ANTHROPIC_API_KEY")

print("=" * 60)
print("  Anomaly Soul Kit")
print("  LLM-Driven Anomaly Evolution Simulator")
print("=" * 60)
print(f"  Mode:        {'MOCK (no API)' if mock else 'REAL (Claude API)'}")
print(f"  Generations: {args.generations}")
print(f"  Population:  {args.population}")
print(f"  Seed:        {args.seed}")
print(f"  Output:      {args.output}/")
print("=" * 60)
print()

# シミュレーション実行
log = run_simulation(
    generations=args.generations,
    population_size=args.population,
    master_seed=args.seed,
    mock=mock,
    api_key=api_key,
    output_dir=args.output,
    verbose=not args.quiet,
)

# 可視化
if not args.no_plot:
    print("\nグラフを生成中...")
    log_path  = f"{args.output}/simulation_log.json"
    save_path = f"{args.output}/anomaly_report.png"
    plot_results(log_path=log_path, save_path=save_path)

# 最終サマリー
final = log[-1]
print("\n" + "=" * 60)
print("  シミュレーション完了")
print("=" * 60)
print(f"  最終世代 mean_H:     {final['mean_H']:.3f}")
print(f"  最終世代 mean_Z:     {final['mean_Z']:.3f}")
print(f"  Z覚醒率:             {final['Z_ratio']:.1%}")
print(f"  最大アノマリースコア: {final['max_anomaly_score']:.3f}")
print(f"  安定性（進化後）:    {final['mean_stability']:.3f}")
print()
print(f"  最終世代 最高アノマリー表現:")
print(f"  \"{final['top_anomaly_text']}\"")
print("=" * 60)
```

if **name** == “**main**”:
main()
