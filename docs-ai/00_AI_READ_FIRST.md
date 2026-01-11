# AI 驅動的可追溯設計系統入口 (Docs-AI Root)

<docs-ai-ruies>

1. 與本文件同一層的文件有更動時，需要更新本文件

2. 本文件不在 docs-ai/ 時，本文件的上層引用文件是上層的 00_AI_READ_FIRST.md

3. 不得更動 <docs-ai-ruies> 的內容
</docs-ai-ruies>

## 1. 本文件的主要任務

本文件是整個 `docs-ai/` 設計文件系統的**唯一優先入口**與**全域導航地圖**。
其核心任務在於：
1.  **引導方向**：為 AI 與開發者提供從需求到實作的正確閱讀路徑。
2.  **維護一致性**：定義各目錄的職責邊界，防止資訊錯位或重複。
3.  **確保可追溯性**：建立文件間的連結，確保所有實作都能回溯至需求。

## 2. 系統架構與目錄導覽

本系統採用級聯式設計，`docs-ai/` 為根目錄，各子目錄皆包含其專屬的 `00_AI_READ_FIRST.md` 作為局部導航。

### 第一層目錄說明

以下目錄按照**建議閱讀與執行順序**排列：

1.  **[01_Requirements (需求分析)](./01_Requirements/00_AI_READ_FIRST.md)**
    *   **核心內容**: 產品需求文件 (PRD)、Use Case 圖、User Stories。
    *   **意圖**: 定義「要做什麼」以及「為什麼要做」。這是所有設計與實作的源頭。
    *   **何時閱讀**: 接到新任務、確認功能細節、編寫測試案例時。

2.  **[00_System_View (系統全貌)](./00_System_View/00_AI_READ_FIRST.md)**
    *   **核心內容**: 高層次系統架構圖、部署架構圖、Tech Stack。
    *   **意圖**: 提供系統的宏觀視角，定義組件間的關係與邊界。
    *   **何時閱讀**: 需要了解整體架構、組件互動方式或部署環境時。

3.  **[02_Contracts (合約與介面)](./02_Contracts/00_AI_READ_FIRST.md)**
    *   **核心內容**: API 規格 (OpenAPI)、資料庫 Schema。
    *   **意圖**: 定義系統內外部的通訊協定與資料結構，作為前後端開發的契約。
    *   **何時閱讀**: 開發 API、設計資料庫、前後端對接時。

4.  **[03_Cross_Cutting_Scenarios (跨切面場景)](./03_Cross_Cutting_Scenarios/00_AI_READ_FIRST.md)**
    *   **核心內容**: 跨組件的業務流程 (Main Flow)、安全性、日誌、可觀測性、測試策略。
    *   **意圖**: 處理跨越單一組件邊界的複雜流程與非功能性需求。
    *   **何時閱讀**: 實作跨組件功能、規劃 E2E 測試、設計資安或監控機制時。

5.  **[04_Component_Designs (組件詳細設計)](./04_Component_Designs/00_AI_READ_FIRST.md)**
    *   **核心內容**: 各模組 (Backend, Frontend) 的內部詳細設計，結構與程式碼庫 (src) 鏡像對應。
    *   **意圖**: 指導具體的程式碼實作，確保實作符合架構規範。
    *   **何時閱讀**: 進入編碼階段 (Coding) 前，需先參閱或撰寫此處的詳細設計。

6.  **[05_Principles (設計原則)](./05_Principles/00_AI_READ_FIRST.md)**
    *   **核心內容**: 架構決策記錄 (ADR)、資料庫設計原則、開發規範。
    *   **意圖**: 記錄「為什麼這樣設計」的決策脈絡，確保團隊遵循一致的標準。
    *   **何時閱讀**: 進行架構決策、Code Review、遇到設計兩難時。

7.  **[06_Development_Records (開發記錄)](./06_Development_Records/00_AI_READ_FIRST.md)**
    *   **核心內容**: 工單 (Tickets)、工作日誌 (Worklogs)。
    *   **意圖**: 追蹤開發進度、記錄每日變更與待辦事項。
    *   **何時閱讀**: 每日工作開始與結束時、更新任務狀態時。

## 3. 常見任務導航

*   **新增功能 (New Feature)**:
    1.  先到 `01_Requirements` 確認需求與 User Story。
    2.  若涉及跨組件互動，更新 `03_Cross_Cutting_Scenarios`。
    3.  若涉及 API 變更，更新 `02_Contracts`。
    4.  在 `04_Component_Designs` 撰寫詳細設計。
    5.  最後進行程式碼實作。

*   **修改現有邏輯 (Refactor/Bugfix)**:
    1.  查閱 `04_Component_Designs` 理解現有設計。
    2.  查閱 `03_Cross_Cutting_Scenarios` 確認是否影響其他組件。
    3.  更新設計文件後，再修改程式碼。

*   **架構決策 (Architecture Decision)**:
    1.  查閱 `00_System_View` 與 `05_Principles`。
    2.  撰寫新的 ADR 於 `05_Principles/ADR`。

## 4. 維護與相依性說明

*   **級聯原則**: 當你進入子目錄時，請務必先閱讀該目錄下的 `00_AI_READ_FIRST.md`，它提供了該局部的詳細規範。
*   **同步更新**: 修改程式碼時，必須同步檢查 `04_Component_Designs` 下的對應文件是否過時。
*   **SSOT (Single Source of Truth)**: 設計文件是系統的真理來源。若程式碼與設計不符，應先修正設計或確認是否為實作錯誤。

---
**請務必隨時保持本文件的連結有效性，當新增或移除第一層目錄時，需同步更新本文件。**
