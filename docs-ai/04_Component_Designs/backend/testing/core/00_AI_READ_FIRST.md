# Core Testing Design 導航

<docs-ai-ruies>

1. 與本文件同一層的文件有更動時，需要更新本文件

2. 本文件不在 docs-ai/ 時，本文件的上層引用文件是上層的 00_AI_READ_FIRST.md

3. 不得更動 <docs-ai-ruies> 的內容
</docs-ai-ruies>

## 1. 本目錄的任務

`docs-ai/04_Component_Designs/backend/testing/core/` 存放針對系統核心邏輯的測試設計。

## 2. 目錄文件導覽

1.  **[Test_Plan.md (核心測試計畫)](./Test_Plan.md)**
    *   **內容**: 定義核心功能 (PDF Parse, AI Convert) 的測試場景、測試資料準備與驗收標準。
    *   **意圖**: 指導 QA 或開發者編寫 `tests/` 目錄下的測試程式碼。

## 3. 維護規則

*   **更新觸發**: 每當 `01_Requirements/Stories/` 中的需求變更，或 `backend/core/` 中的設計變更時，都應檢視本測試計畫是否需要更新。
