# Principles & Decisions 導航 (Principles Root)

<docs-ai-ruies>

1. 與本文件同一層的文件有更動時，需要更新本文件

2. 本文件不在 docs-ai/ 時，本文件的上層引用文件是上層的 00_AI_READ_FIRST.md

3. 不得更動 <docs-ai-ruies> 的內容
</docs-ai-ruies>

## 1. 本文件夾的主要任務

`docs-ai/05_Principles/` 負責存放指導系統設計與開發的**核心原則**以及**架構決策記錄 (ADR)**。
其核心任務在於：
1.  **建立共識 (Consensus)**: 記錄團隊共同遵守的設計規範與原則。
2.  **決策記憶 (Memory)**: 透過 ADR 記錄關鍵架構選擇背後的脈絡 (Context) 與理由 (Rationale)，防止決策反覆或遺忘。
3.  **減少爭議 (Consistency)**: 當遇到設計兩難時，以此處的原則作為裁決依據。

## 2. 目錄文件導覽

本目錄包含以下關鍵文件與子目錄：

1.  **[ADR/ (架構決策記錄)](./ADR/00_AI_READ_FIRST.md)**
    *   **內容**: 不可變的決策記錄文件集合。
    *   **意圖**: 記錄「為什麼我們選擇了 A 而不是 B」。
    *   **何時閱讀**: 了解特定設計背後的歷史原因，或準備提出新的架構變更時。

2.  **[Database_Schema_Design_Principles.md (資料庫設計原則)](./Database_Schema_Design_Principles.md)**
    *   **內容**: 資料庫 Schema 的命名規範、正規化標準與索引策略。
    *   **意圖**: 確保資料庫設計的一致性與效能。
    *   **何時閱讀**: 設計新的資料表或修改現有 Schema 時。

## 3. 維護規則

*   **原則優先**: 所有的 Detailed Design (`04_Component_Designs`) 都不得違反此處定義的原則。若有例外，必須撰寫 ADR 說明理由。
*   **不可變性**: 已批准的 ADR 應視為不可變的歷史記錄。若要推翻舊決策，應建立新的 ADR 來取代 (Supersede) 舊的。
