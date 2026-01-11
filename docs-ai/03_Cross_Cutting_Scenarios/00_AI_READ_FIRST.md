# Cross Cutting Scenarios 導航 (Cross Cutting Root)

<docs-ai-ruies>

1. 與本文件同一層的文件有更動時，需要更新本文件

2. 本文件不在 docs-ai/ 時，本文件的上層引用文件是上層的 00_AI_READ_FIRST.md

3. 不得更動 <docs-ai-ruies> 的內容
</docs-ai-ruies>

## 1. 本文件夾的主要任務

`docs-ai/03_Cross_Cutting_Scenarios/` 負責處理**跨越單一組件邊界**的複雜業務流程，以及影響全系統的**非功能性需求**。
其核心任務在於：
1.  **串聯流程 (Orchestration)**: 定義多個組件如何協同工作以完成核心業務價值 (e.g., Main Flow)。
2.  **統一標準 (Standardization)**: 定義日誌、資安、可觀測性等全域規範，避免各組件各自為政。
3.  **驗證品質 (Verification)**: 透過 E2E 測試策略確保端對端的功能正確性。

## 2. 目錄文件導覽

本目錄包含以下關鍵文件與子目錄，建議閱讀順序：

1.  **[Main_Flow.puml (核心流程)](./Main_Flow.puml)**
    *   **內容**: 系統最核心的業務執行路徑循序圖 (Sequence Diagram)。
    *   **意圖**: 提供 "Big Picture"，展示 CLI, Engine, PDF Parser 與 AI 如何協作完成 PDF 轉 Markdown 的任務。
    *   **何時閱讀**: 理解系統主邏輯、除錯流程問題、或新增核心功能時。

2.  **[testing/ (測試策略)](./testing/00_AI_READ_FIRST.md)**
    *   **內容**: 端對端 (E2E) 測試場景與 Use Case 測試計畫。
    *   **意圖**: 定義如何從使用者角度驗證系統功能。

3.  **[logging/ (日誌規範)](./logging/00_AI_READ_FIRST.md)**
    *   **內容**: 定義 Log Level, Log Format 與 Trace ID 傳遞機制。
    *   **意圖**: 確保日誌的可讀性與可追溯性，支援維運除錯。

4.  **[security/ (安全性設計)](./security/00_AI_READ_FIRST.md)**
    *   **內容**: API Key 管理、檔案存取權限控制等資安規範。
    *   **意圖**: 確保系統運行的安全性，防止資料外洩。

5.  **[observability/ (可觀測性)](./observability/00_AI_READ_FIRST.md)**
    *   **內容**: 監控指標 (Metrics) 與追蹤 (Tracing) 設計。
    *   **意圖**: 提供系統運行狀態的可視化能力。

## 3. 維護規則

*   **流程變更**: 若修改了 `Main_Flow.puml` 中的互動邏輯，必須同步檢查 `testing/` 下的 E2E 測試案例是否需要更新。
*   **規範落地**: 在 `04_Component_Designs` 進行細部設計時，必須引用此處定義的 Logging 與 Security 規範。
