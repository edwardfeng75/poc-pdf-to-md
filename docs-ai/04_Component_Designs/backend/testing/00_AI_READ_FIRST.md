# Backend Testing Design 導航

<docs-ai-ruies>

1. 與本文件同一層的文件有更動時，需要更新本文件

2. 本文件不在 docs-ai/ 時，本文件的上層引用文件是上層的 00_AI_READ_FIRST.md

3. 不得更動 <docs-ai-ruies> 的內容
</docs-ai-ruies>

## 1. 本目錄的任務

`docs-ai/04_Component_Designs/backend/testing/` 存放後端組件的詳細測試計畫與策略。
這裡不包含實際的測試程式碼 (存放在原始碼庫 `tests/`)，而是定義「要測什麼」以及「如何測」。

## 2. 目錄文件導覽

1.  **[core/ (核心測試計畫)](./core/00_AI_READ_FIRST.md)**
    *   **內容**: 針對核心業務邏輯的詳細測試計畫 (對應 `backend/core/` 的設計)。
    *   **關鍵文件**: `Test_Plan.md`。

## 3. 維護規則

*   **同步設計**: 當 `backend/core/` 的設計變更時，必須同步更新這裡的測試計畫，確保測試覆蓋新的設計邏輯。
*   **測試分層**: 這裡專注於單元測試與組件整合測試的設計；跨組件的 E2E 測試設計請參考 `docs-ai/03_Cross_Cutting_Scenarios/testing/`。
