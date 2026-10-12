# Cognitive Dual-System Multi-Agent
### A Computational Implementation of Dual-Process Theory & Dissonance-Driven Metacognitive Consolidation


> **"Can we build autonomous AI systems that know *when to doubt themselves* and *when to allocate compute*?"**  
> 本專案將認知心理學的 **雙系統理論（Dual-Process Theory, System 1 / System 2）**、**費斯汀格認知失調（Cognitive Dissonance）** 與 **元認知記憶固化（Metacognitive Consolidation）** 完整計算化，構建出一套具備自適應算力調配與抗辯消解能力的多智能體架構（Multi-Agent System）。

---

## 📌 Demo 預覽



https://github.com/user-attachments/assets/8ed7de73-7823-46e6-8531-3f8ed3c94a0f



---

## 💡 研究動機與核心假設 (Core Hypothesis)

現行 LLM 與 Multi-Agent 系統面臨兩大核心瓶頸：
1. **靜態算力浪費（Static Compute Waste）**：無論任務輕重，一律調用昂貴的大模型跑完整 CoT（Chain of Thought），缺乏生物大腦的認知節能彈性。
2. **缺乏深層自我懷疑機制**：多數 Agent 在遇到邏輯衝突時，依賴表面式的加權投票（Majority Voting），抹煞了邊界處的關鍵因果矛盾。

### 核心理論映射 (Psychological Mapping to Computation)
- **System 1 (直覺代理人)**：模擬啟發式思考（Heuristics），以微秒級延遲與低耗能快速輸出先驗假設。
- **認知失調張量引擎 (Cognitive Dissonance Tensor Engine)**：量化「語意熵值（Entropy）」與「先驗邏輯衝突（Prior Conflict）」，決定是否打破認知衡定。
- **System 2 (審思代理人)**：以思維樹（Tree-of-Thought, ToT）展開形式化因果推導與分支剪枝。
- **對抗性審查 Agent (Devil's Advocate)**：生成反事實情境（Counterfactuals），嚴格檢驗確認偏誤。
- **經驗固化閉環 (Consolidation)**：模擬人類睡眠時的記憶重構，將深思後的因果規則回填至 System 1，實現低成本持續演化。

---


## 🧪 認知題庫 (Benchmark Suite)

系統內建 6 組具代表性的認知心理學、行為經濟學與實務運籌測試情境：

| 基準測試題目 | 心理學領域 | 認知陷阱 / 機制 | 系統響應機制 |
| :--- | :--- | :--- | :--- |
| **球棒與球問題 (Bat and Ball)** | 行為經濟學 (CRT) | 屬性替代偏誤 (Attribute Substitution) | 觸發失調 $\rightarrow$ 喚醒 System 2 代數求解 |
| **琳達問題 (Linda Problem)** | 代表性啟發式 | 合取謬誤 ($P(A \cap B) > P(A)$) | 集合論剪枝，消除語意相符度混淆 |
| **華生選擇任務 (Wason Task)** | 演繹推理 / 假設檢驗 | 確認偏誤 (Confirmation Bias) | 對抗 Agent 介入，執行波普爾否證推演 |
| **醫學篩檢與罕見病** | 貝氏推論 | 基本比率忽略 (Base Rate Neglect) | 展開頻率樹狀分析，校準後驗機率 |
| **專案沉沒成本** | 前景理論 (Prospect Theory) | 沉沒成本誤區與承諾升級 | 強制歸零歷史支出，回歸邊際效益模型 |
| **常規物流調運** | 實務運籌管理 | 常規無偏誤操作 (SOP) | **System 1 綠燈直行，節省 95% 算力** |

---

## 補充

超參數調節說明：

1.喚醒敏感度閾值 ($\theta$)：控制前額葉抑制閾值。$\theta$ 愈高，系統愈趨向謹慎、愈容易喚醒 System 2 進行深度查驗。

2.語意熵值敏感係數：放大推論模糊度對失調張力 $\Delta$ 的貢獻度。

3.對抗性審查開關 (Devil's Advocate)：啟用後強制在推論邊界生成反事實條件，執行邊界壓力測試。


未來演進路線：

1.LLM API 接軌：整合 LangGraph，以微調後的 SLM（如 Llama-3-8B）擔任 System 1，前緣推論模型（如 o1 / Claude 3.5 Sonnet）擔任 System 2。

2.向量化直覺記憶庫：整合 ChromaDB / Qdrant，將記憶固化成果自動向量化索引，動態更新 System 1 檢索增強先驗。

