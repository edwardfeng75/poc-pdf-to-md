# Core Logic Design 導航

<docs-ai-ruies>

1. 與本文件同一層的文件有更動時，需要更新本文件

2. 本文件不在 docs-ai/ 時，本文件的上層引用文件是上層的 00_AI_READ_FIRST.md

3. 不得更動 <docs-ai-ruies> 的內容
</docs-ai-ruies>

## 1. 本目錄的任務

`docs-ai/04_Component_Designs/backend/core/` 存放專案最核心的業務邏輯設計。
此目錄的內容直接對應原始碼中的核心模組 (主要對應 `src/poc_pdf_to_md` 及其核心邏輯)。

## 2. 目錄文件導覽

1.  **[Class_Diagram.puml (核心類別圖)](./Class_Diagram.puml)**
    *   **內容**: 定義系統核心元件 (PDF Parser, AI Engine, Image Handler) 的類別結構、屬性、方法與繼承關係。
    *   **意圖**: 指導開發者實作物件導向結構，確保職責分離。

## 3. 維護規則

*   **鏡像更新**: 當修改原始碼中的核心類別 (如 `engine.py`, `pdf_parser.py`) 時，必須同步更新 `Class_Diagram.puml`。
*   **介面穩定**: 核心模組的公開介面變更應視為重大變更，需評估對上層調用者 (CLI, API) 的影響。
