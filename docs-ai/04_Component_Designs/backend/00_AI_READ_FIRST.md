# Backend Component Designs 導航 (Backend Design Root)

<docs-ai-ruies>

1. 與本文件同一層的文件有更動時，需要更新本文件

2. 本文件不在 docs-ai/ 時，本文件的上層引用文件是上層的 00_AI_READ_FIRST.md

3. 不得更動 <docs-ai-ruies> 的內容
</docs-ai-ruies>

## 1. 本目錄的任務

`docs-ai/04_Component_Designs/backend/` 負責存放所有後端服務與核心邏輯的詳細設計。
這包括了 Python CLI 工具的核心邏輯 (`core/`)、領域模型 (`domain/`) 以及測試計畫 (`testing/`)。

## 2. 目錄文件導覽

本目錄包含以下關鍵子目錄：

1.  **[core/ (核心邏輯)](./core/00_AI_READ_FIRST.md)**
    *   **內容**: 系統最核心的業務邏輯設計，對應原始碼中的 `src/poc_pdf_to_md` 核心模組。
    *   **關鍵文件**: `Class_Diagram.puml` (核心類別設計)。

2.  **[testing/ (測試計畫)](./testing/00_AI_READ_FIRST.md)**
    *   **內容**: 後端組件的詳細測試策略與計畫。
    *   **關鍵子目錄**: `testing/core/` (核心邏輯的測試計畫)。

3.  **[domain/ (領域模型)](./domain/00_AI_READ_FIRST.md)**
    *   **內容**: 領域驅動設計 (DDD) 下的實體 (Entities)、值物件 (Value Objects) 與聚合 (Aggregates)。

4.  **[plugin_core_business/ (核心業務插件)](./plugin_core_business/00_AI_READ_FIRST.md)**
    *   **內容**: 特定業務功能的插件設計 (如 Chat Service, Docs Service)。

5.  **[shared_modules/ (共用模組)](./shared_modules/00_AI_READ_FIRST.md)**
    *   **內容**: 跨服務共用的基礎設施與工具設計。

## 3. 維護規則

*   **核心優先**: 對於 `core/` 下的設計變更，必須嚴格審查，因為它影響系統最基礎的功能。
*   **測試對應**: `core/` 中的設計變更，應同步反映在 `testing/core/` 的測試計畫中。
