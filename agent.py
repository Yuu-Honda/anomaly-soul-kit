"""
agent.py
--------
SoulAgent: LLMを使って自己状態をテキストで表現するエージェント。
各エージェントは独立したRNGを持ち、H（活力）とZ（アノマリー強度）を進化させる。
"""
import numpy as np
class SoulAgent:
def __init__(
self,
agent_id: int,
rng: np.random.Generator = None,
rule_params: tuple = None,
stability: float = None,
):
self.agent_id = agent_id
self.rng = rng if rng is not None else np.random.default_rng()
# 進化するパラメータ（突然変異で引き継がれる）
if rule_params is None:
self.rule_alpha = self.rng.uniform(0.8, 1.2) # 環境感受性
self.rule_beta = self.rng.uniform(0.8, 1.2) # ノイズ感受性
self.rule_gamma = self.rng.uniform(0.8, 1.2) # 安定性寄与
else:
self.rule_alpha, self.rule_beta, self.rule_gamma = rule_params
self.stability = stability if stability is not None else self.rng.uniform(0.8, 1.2)
# 状態変数
self.H = 0.0 # 活力（Vitality）
self.Z = 0.0 # アノマリー強度（Anomaly intensity）
self.has_Z = False # アノマリー覚醒フラグ
self.memory_H = [] # 直近50世代のH履歴
self.memory_Z = [] # 直近50世代のZ履歴
self.text_log = [] # LLMが生成したテキスト履歴
self.collapse_count = 0
self.generation = 0
# ------------------------------------------------------------------
# 状態更新
# ------------------------------------------------------------------
def step(self, env_factor: float):
"""環境刺激を受けてHを更新する。"""
# Z高値 → 崩壊への抵抗力が上がる（H-Z相互作用）
z_shield = float(np.tanh(self.Z / 50.0) * 0.5)
delta_H = (
self.rule_alpha * env_factor
- self.rule_beta * self.rng.random()
+ self.rule_gamma * self.stability
+ z_shield
)
self.H = max(0.0, self.H + delta_H)
if self.H == 0:
self.collapse_count += 1
self.memory_H.append(self.H)
if len(self.memory_H) > 50:
self.memory_H.pop(0)
self.generation += 1
def update_Z(self, anomaly_score: float):
"""
アノマリー検出レイヤーから受け取ったスコアでZを更新する。
soft cap（上限200）と減衰（×0.98）で爆発を防ぐ。
"""
Z_SOFT_CAP = 200.0
Z_DECAY = 0.98
headroom = max(0.0, 1.0 - self.Z / Z_SOFT_CAP)
self.Z = max(0.0, (self.Z + anomaly_score * headroom) * Z_DECAY)
self.memory_Z.append(self.Z)
if len(self.memory_Z) > 50:
self.memory_Z.pop(0)
def maybe_trigger_Z(self, population_mean_H: float):
"""H が集団平均の2倍超、または崩壊3回以上でアノマリー覚醒。"""
if not self.has_Z:
if self.H > population_mean_H * 2.0 or self.collapse_count >= 3:
self.has_Z = True
self.Z = self.H * 0.5
# ------------------------------------------------------------------
# LLMプロンプト生成
# ------------------------------------------------------------------
def build_prompt(self, env_factor: float) -> str:
"""
現在の状態を渡してLLMに短いテキストを生成させるプロンプト。
エージェントは自分の状態を「表現」する。説明しない。
"""
history_avg = float(np.mean(self.memory_H)) if self.memory_H else 0.0
recent_texts = self.text_log[-3:] if self.text_log else []
history_str = " | ".join(recent_texts) if recent_texts else "none"
return f"""You are agent {self.agent_id}, generation {self.generation}.
Internal state:
- vitality (H): {self.H:.3f}
- anomaly intensity (Z): {self.Z:.3f}
- anomaly awakened: {self.has_Z}
- collapse count: {self.collapse_count}
- historical vitality avg: {history_avg:.3f}
- environment pressure: {env_factor:.3f}
Recent expressions: {history_str}
Express your current state in 1 to 3 sentences.
Do NOT explain or describe. Just express.
Be shaped by your numbers. Let the state speak through language."""
def receive_expression(self, text: str):
"""LLMの生成テキストを受け取って履歴に記録する。"""
self.text_log.append(text.strip())
if len(self.text_log) > 50:
self.text_log.pop(0)
# ------------------------------------------------------------------
# シリアライズ
# ------------------------------------------------------------------
def state_dict(self) -> dict:
return {
"agent_id": self.agent_id,
"generation": self.generation,
"H": float(self.H),
"Z": float(self.Z),
"has_Z": self.has_Z,
}
"collapse_count":self.collapse_count,
"stability": float(self.stability),
"rule_alpha": float(self.rule_alpha),
"rule_beta": float(self.rule_beta),
"rule_gamma": float(self.rule_gamma),
"last_text": self.text_log[-1] if self.text_log else "",
