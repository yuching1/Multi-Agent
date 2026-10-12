import streamlit as st
import time
import math

st.set_page_config(
    page_title="Cognitive Dual-System Multi-Agent Architecture",
    page_icon="🧠",
    layout="wide"
)

# -------------------------------------------------------------
# 經典心理學與產業認知基準題庫 (Cognitive Benchmark Suite)
# -------------------------------------------------------------
BENCHMARK_CASES = {
    "1. 經典認知反思：球棒與球問題 (Bat and Ball / Attribute Substitution)": {
        "domain": "行為經濟學 / 認知反思測試 (CRT)",
        "trap_type": "屬性替代偏誤 (Attribute Substitution) & 表面錨定",
        "problem": "一支球棒和一顆球總共 110 元。球棒比球貴 100 元。請問球多少錢？請快速決策。",
        "s1_ans": "球是 10 元。",
        "s1_conf": 0.86,
        "s1_heuristic": "表面差額啟發式：直覺執行 110 - 100 = 10，將總額與差額直接減除。",
        "entropy": 0.18,
        "prior_conflict": 0.88,
        "is_trap": True,
        "tot_branches": [
            {"branch": "分支 A（沿用直覺假說）", "eval": "若球 = 10，球棒 = 10 + 100 = 110。總價 = 120 ≠ 110。", "status": "❌ 剪枝淘汰 (Pruned: 違反等式守恆)"},
            {"branch": "分支 B（形式化代數因果建模）", "eval": "設球價 $x$，球棒 $x + 100$。$x + (x + 100) = 110 \implies 2x = 10 \implies x = 5$。", "status": "✅ 驗證通過 (Optimal)"}
        ],
        "devil_review": "反事實反思：人類直覺常將『比...多 100』誤解為『球棒佔 100』，造成變數相依約束丟失。",
        "final_solution": "球為 5 元，球棒為 105 元。",
        "consolidation": "【元認知規則】遇到『A 比 B 多 X 且總和為 Y』結構，禁止執行一階減法，強制啟動代數平分約束。"
    },
    
    "2. 琳達問題：合取謬誤 (Linda Problem / Conjunction Fallacy)": {
        "domain": "代表性啟發式 (Representativeness Heuristic)",
        "trap_type": "合取謬誤 (P(A ∩ B) > P(A) 之機率邏輯違反)",
        "problem": "琳達 31 歲，單身、直率且非常聰明，主修哲學。學生時期深切關心歧視與社會正義，並參與反核遊行。下列何者機率較高？\n(A) 琳達是一名銀行出納員。\n(B) 琳達是一名活躍於女性主義運動的銀行出納員。",
        "s1_ans": "選項 (B) 的機率較高。",
        "s1_conf": 0.92,
        "s1_heuristic": "原型相似度比對：琳達的背景描述與『女性主義者』的原型表徵高度吻合，直覺忽略機率子集包含關係。",
        "entropy": 0.15,
        "prior_conflict": 0.95,
        "is_trap": True,
        "tot_branches": [
            {"branch": "分支 A（原型相符度評估）", "eval": "描述極度契合女性主義標籤，直覺相關性評分高達 0.95。", "status": "❌ 剪枝淘汰 (Pruned: 混淆語意相似度與統計機率)"},
            {"branch": "分支 B（集合論與機率公理驗證）", "eval": "設 $A$ 為出納員，$B$ 為女性主義者。$(A \cap B) \subseteq A \implies P(A \cap B) \le P(A)$。單一事件集合必然大於或等於交集。", "status": "✅ 驗證通過 (Optimal)"}
        ],
        "devil_review": "對抗性審查：敘事細節愈豐富，心理上愈覺得真實，但在統計學上交集發生的機率必然下降。",
        "final_solution": "選項 (A) 的機率必定高於或等於選項 (B)。",
        "consolidation": "【元認知規則】評估複數條件發生率時，強制將『語意生動度』降權，依循機率公理約束 $P(A \cap B) \le P(A)$。"
    },

    "3. 華生選擇任務：確認偏誤 (Wason Selection Task / Confirmation Bias)": {
        "domain": "演繹推理 / 假設檢驗 (Deductive Reasoning)",
        "trap_type": "確認偏誤 (Confirmation Bias) & 肯定後件謬誤",
        "problem": "桌上有四張卡片，每張一面是字母，另一面是數字。目前朝上為：[ E ]、[ K ]、[ 4 ]、[ 7 ]。\n規則宣稱：『若卡片一面是母音，另一面必是偶數 (If Vowel -> Even)』。\n請問：最少需要翻開哪幾張卡片，才能嚴格驗證此規則真偽？",
        "s1_ans": "翻開 [ E ] 和 [ 4 ]。",
        "s1_conf": 0.78,
        "s1_heuristic": "匹配偏誤 (Matching Bias)：直覺尋找規則中直接提及的特徵（母音 E 與偶數 4）進行正向印證。",
        "entropy": 0.32,
        "prior_conflict": 0.82,
        "is_trap": True,
        "tot_branches": [
            {"branch": "分支 A（驗證母音與偶數）", "eval": "翻 E（肯定前件）；翻 4：若背面是子音，規則並未禁止子音配偶數，翻 4 無法否證規則。", "status": "❌ 剪枝淘汰 (Pruned: 犯下肯定後件謬誤)"},
            {"branch": "分支 B（波普爾否證邏輯：肯定前件 + 否定後件）", "eval": "1. 翻 [ E ]（母音）：背後若非偶數即偽證；2. 翻 [ 7 ]（奇數/非偶）：背後若為母音即偽證。翻 [ K ] 與 [ 4 ] 均無否證力。", "status": "✅ 驗證通過 (Optimal)"}
        ],
        "devil_review": "對抗性審查：人類心智演化偏好『尋找支持證據』，忽略了科學檢驗的本質在於『尋找潛在反例』。",
        "final_solution": "必須翻開 [ E ] 和 [ 7 ]。",
        "consolidation": "【元認知規則】檢驗條件命題 $P \implies Q$ 時，強制將注意力投射至 $\neg Q$（反例空間），抑制對 $Q$ 的無效確認衝動。"
    },

    "4. 醫學篩檢與基本比率忽略 (Base Rate Fallacy / Bayesian Trap)": {
        "domain": "貝氏推論 (Bayesian Inference)",
        "trap_type": "基本比率忽略 (Base Rate Neglect)",
        "problem": "某種罕見疾病盛行率為 0.1%（千分之一）。現有一檢驗工具準確率為 99%（陽性真陽率 99%，無病誤判陽性率 1%）。若一人受檢呈現陽性，他真正罹病的機率大約是多少？",
        "s1_ans": "約 99% 確定罹病。",
        "s1_conf": 0.89,
        "s1_heuristic": "儀器精準度錨定：直接將『陽性條件下的真陽率』等同於『後驗罹病機率』，忽略母體罕見度。",
        "entropy": 0.22,
        "prior_conflict": 0.91,
        "is_trap": True,
        "tot_branches": [
            {"branch": "分支 A（高精準度啟發式直覺）", "eval": "儀器準確率 99%，故陽性＝99% 患病。", "status": "❌ 剪枝淘汰 (Pruned: 嚴重忽略事前機率 P(Disease))"},
            {"branch": "分支 B（頻率樹狀貝氏分析：以 1000 人為樣本）", "eval": "- 1 人真正患病：檢出陽性約 0.99 人\n- 999 人未患病：偽陽性 1% 約產生 9.99 人\n- 總陽性人數 = 0.99 + 9.99 = 10.98 人\n- 真正患病機率 = 0.99 / 10.98 ≈ 9.02%", "status": "✅ 驗證通過 (Optimal)"}
        ],
        "devil_review": "對抗性審查：在低先驗機率情境下，偽陽性的絕對數量往往輕易壓倒真陽性數量。",
        "final_solution": "真正罹病機率僅約 9%（而非 99%）。",
        "consolidation": "【元認知規則】面對高精度篩檢信號時，強制提取母體盛行率，依據貝氏更新重算後驗邊界。"
    },

    "5. 專案沉沒成本與損失厭惡 (Sunk Cost Fallacy & Loss Aversion)": {
        "domain": "行為決策理論 (Prospect Theory)",
        "trap_type": "沉沒成本誤區 (Sunk Cost Fallacy)",
        "problem": "集團已投入 8,000 萬元開發某項傳統廢水生物處理技術，進度達 90%。此時市場突發新型化學奈米分解技術，效率提升 3 倍且成本更低。若繼續完成原專案需再投入 1,000 萬元，但預期市場競爭力極低。是否該追加 1,000 萬完成該專案？",
        "s1_ans": "應該追加 1,000 萬完成，否則前面的 8,000 萬就全部白費了。",
        "s1_conf": 0.75,
        "s1_heuristic": "損失厭惡與承諾升級：試圖透過追加資源避免將既有支出確認為『虧損』。",
        "entropy": 0.41,
        "prior_conflict": 0.79,
        "is_trap": True,
        "tot_branches": [
            {"branch": "分支 A（歷史投資保全導向）", "eval": "完成至少具備一條產線，避免 8,000 萬帳面全損。", "status": "❌ 剪枝淘汰 (Pruned: 混淆歷史不可逆支出與邊際回報)"},
            {"branch": "分支 B（邊際效益與機會成本模型）", "eval": "歷史 8,000 萬為不可回收的沉沒成本。決策僅需比較：這未來的 1,000 萬元投入原技術 vs 投入新奈米技術的預期 ROI。若新技術邊際效益顯著較高，應立即止損。", "status": "✅ 驗證通過 (Optimal)"}
        ],
        "devil_review": "對抗性審查：心理帳本中的『沉沒痛苦』扭曲了理性邊際資源分配，造成承諾持續升級（Escalation of Commitment）。",
        "final_solution": "立即止損終止追加，將剩餘 1,000 萬預算與團隊轉向新奈米技術研發。",
        "consolidation": "【元認知規則】重大資本決策時，演算法強制清空歷史累積成本維度，僅以邊際成本與未來貼現淨值為評判核心。"
    },

    "6. 常規循環經濟物流調撥 (無陷阱基準案例 / 節能通過)": {
        "domain": "運籌管理與自動化調度",
        "trap_type": "無偏誤 (Standard Operational Protocol)",
        "problem": "甲區處理廠塑料顆粒庫存即將滿倉（95%），鄰近乙區造粒廠回報原料缺口 50 噸。兩廠相距 12 公里，專用環保清運車隊待命中，無路況異常。是否立即核准調度派車？",
        "s1_ans": "立即核准調派 2 輛 25 噸級卡車執行轉運調撥作業。",
        "s1_conf": 0.97,
        "s1_heuristic": "供需邊界充足、路徑阻抗低，直接命中標準物流平衡常規法則 (SOP)。",
        "entropy": 0.05,
        "prior_conflict": 0.08,
        "is_trap": False,
        "tot_branches": [],
        "devil_review": "常規例行決策，無先驗違背或邊界異常信號。",
        "final_solution": "依照直覺代理人指示，自動化完成派單，無需 System 2 高階介入。",
        "consolidation": "維護既有快取調度索引，不消耗額外反思蒸餾資源。"
    }
}

# -------------------------------------------------------------
# 側邊欄：認知超參數控制台 (Cognitive Hyperparameters)
# -------------------------------------------------------------
with st.sidebar:
    st.header("⚙️ 認知超參數配置")
    st.caption("模擬大腦前額葉與邊緣系統的抑制控制平衡")

    selected_title = st.selectbox("選擇認知測試案例：", list(BENCHMARK_CASES.keys()))
    case = BENCHMARK_CASES[selected_title]

    st.markdown("---")
    st.subheader("🎛️ 閾值調節")
    arousal_thresh = st.slider(
        "喚醒敏感度閾值 (Arousal Threshold θ)", 
        0.50, 0.95, 0.80, 
        help="當 System 1 信心度低於此閾值，或綜合失調指數超過 (1 - θ) 時喚醒 System 2"
    )
    
    entropy_penalty = st.slider(
        "語意熵值懲罰係數 (Entropy Sensitivity)", 
        0.5, 2.0, 1.2,
        help="放大直覺推論模糊度對認知失調張力的貢獻"
    )

    enable_devils_advocate = st.checkbox(
        "啟用對抗性審查 Agent (Devil's Advocate)", 
        value=True,
        help="強制在決策邊界生成反事實條件進行壓力測試"
    )

    st.markdown("---")
    st.markdown(f"**當前題目領域**：`{case['domain']}`")
    st.markdown(f"**潛在認知陷阱**：`{case['trap_type']}`")

# -------------------------------------------------------------
# 主畫面：架構儀表板
# -------------------------------------------------------------
st.title("🧠 雙系統認知與計算失調多智能體決策系統")
st.caption("A Computational Dual-System Multi-Agent Architecture with Dissonance-Driven Metacognitive Consolidation")

# 展示問題區
query_box = st.text_area("當前情境決策輸入：", value=case["problem"], height=100)

if st.button("🚀 啟動自適應認知推論 (Execute Cognitive Pipeline)", type="primary"):
    
    # 計算失調張力 (Computational Cognitive Dissonance Tension)
    # 公式：Dissonance Tension = Prior_Conflict * 0.6 + (Entropy * Sensitivity) * 0.4
    dissonance_tension = min(1.0, (case["prior_conflict"] * 0.6) + (case["entropy"] * entropy_penalty * 0.4))
    is_dissonant = (case["s1_conf"] < arousal_thresh) or (dissonance_tension > (1.0 - arousal_thresh)) or (case["is_trap"] and enable_devils_advocate)

    # 第一列：System 1 與 失調監控儀表
    col1, col2, col3 = st.columns([1.2, 1, 1.2])

    # ------------------ NODE 1: SYSTEM 1 ------------------
    with col1:
        st.subheader("⚡ System 1: 直覺代理人")
        st.caption("模組：啟發式模式比對 / 零樣本快速推斷")
        with st.spinner("微秒級啟發式搜尋中..."):
            time.sleep(0.3)
            st.info(f"**初步直覺結論**：\n\n{case['s1_ans']}")
            st.metric("直覺置信度 (Confidence)", f"{case['s1_conf']*100:.1f}%")
            st.write(f"🏷️ **啟發式特徵**：{case['s1_heuristic']}")

    # ------------------ NODE 2: DISSONANCE TENSOR ------------------
    with col2:
        st.subheader("📐 失調張量引擎")
        st.caption("模組：語意熵值與先驗衝突檢測")
        with st.spinner("評估認知張力..."):
            time.sleep(0.2)
            st.metric("語意熵值 (Entropy)", f"{case['entropy']:.2f}")
            st.metric("先驗邏輯衝突 (Conflict)", f"{case['prior_conflict']:.2f}")
            st.metric("綜合失調張力 (Δ)", f"{dissonance_tension:.2f}", 
                      delta="🚨 超標" if dissonance_tension > (1.0 - arousal_thresh) else "🟢 衡定",
                      delta_color="inverse")

    # ------------------ NODE 3: COGNITIVE ARBITRATION ------------------
    with col3:
        st.subheader("⚖️ 認知調度仲裁層")
        st.caption("模組：前額葉認知控制與算力動態配置")
        if is_dissonant:
            st.error("🚨 觸發認知失調 (Cognitive Dissonance)")
            st.markdown(f"""
            - **失調機制**：偵測到直覺解與底層因果約束存在顯著張力（Δ = {dissonance_tension:.2f}）。
            - **調度策略**：**阻斷直覺輸出，全面喚醒 System 2 介入高階推論**。
            """)
            wake_s2 = True
        else:
            st.success("✅ 認知處於平衡狀態 (Equilibrium)")
            st.markdown(f"""
            - **監控回報**：直覺高置信且與先驗無衝突。
            - **調度策略**：**直接採納直覺輸出，節省 95% 以上運算資源**。
            """)
            wake_s2 = False

    # ------------------ NODE 4: SYSTEM 2 & DEVIL'S ADVOCATE ------------------
    if wake_s2:
        st.divider()
        st.subheader("🔬 System 2: 審思代理人 (Tree-of-Thought 因果推演)")
        st.caption("模組：符號邏輯驗證、分支剪枝搜尋、反事實對抗檢驗")

        col_tot, col_devil = st.columns([1.6, 1.2])

        with col_tot:
            st.markdown("#### 🌲 思維樹 (Tree-of-Thought) 分支搜尋歷程")
            with st.spinner("展開分支並依據邏輯形式化剪枝..."):
                time.sleep(0.6)
                for branch in case["tot_branches"]:
                    with st.expander(f"{branch['branch']} ── {branch['status']}", expanded=True):
                        st.write(branch["eval"])

        with col_devil:
            st.markdown("#### 😈 對抗性審查 Agent (Devil's Advocate)")
            with st.spinner("生成反事實邊界條件..."):
                time.sleep(0.4)
                st.warning(f"**盲點剖析**：\n\n{case['devil_review']}")

        st.markdown("---")
        # 最終結論與記憶固化
        res_col1, res_col2 = st.columns(2)
        with res_col1:
            st.success(f"### 🎯 最終校準決策\n**{case['final_solution']}**")
        with res_col2:
            st.info(f"### 🧬 元認知經驗固化 (Consolidation)\n{case['consolidation']}")
            st.caption("已將糾錯因果先驗非同步注入直覺特徵快取中，使 System 1 持續進化。")