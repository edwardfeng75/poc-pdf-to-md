# Component Designs 導航 (Component Designs Root)

<docs-ai-ruies>

1. 與本文件同一層的文件有更動時，需要更新本文件

2. 本文件不在 docs-ai/ 時，本文件的上層引用文件是上層的 00_AI_READ_FIRST.md

3. 不得更動 <docs-ai-ruies> 的內容
</docs-ai-ruies>

## 1. 本文件夾的主要任務

`docs-ai/04_Component_Designs/` 存放系統各組件的**詳細設計 (Detailed Design)**。
其核心任務在於：
1.  **指導實作**: 提供程式碼級別的設計藍圖 (Class Diagram, Interface Spec)，讓開發者能直接依據設計進行編碼。
2.  **鏡像結構**: 設計文件的目錄結構應盡可能與原始碼 (Source Code) 結構保持對應，方便雙向查找。
3.  **封裝細節**: 隱藏組件內部的複雜性，僅透過明確的介面與外部溝通。

## 2. 目錄文件導覽

本目錄依據技術領域劃分，建議閱讀順序：

1.  **[backend/ (後端組件)](./backend/00_AI_READ_FIRST.md)**
    *   **核心內容**: Python 核心邏輯、API 服務與領域模型。
    *   **關鍵子目錄**:
        *   `backend/core/`: 核心業務邏輯與類別設計 (包含 Class_Diagram.puml)。
        *   `backend/domain/`: 領域驅動設計 (DDD) 的實體與聚合根。
        *   `backend/testing/core/`: 核心組件的測試計畫 (Test Plan)。

2.  **[frontend/ (前端組件)](./frontend/00_AI_READ_FIRST.md)**
    *   **核心內容**: Web 介面、頁面流 (Page Flow) 與 UI 元件設計。
    *   **關鍵子目錄**:
        *   `frontend/pages/`: 各頁面的詳細設計與狀態流轉。
        *   `frontend/design_system/`: 共用 UI 元件庫規範。

## 3. 維護與一致性

*   **設計優先 (Design First)**: 在撰寫或大幅修改程式碼前，應先在此處更新對應的設計文件 (如 Class Diagram)。
*   **代碼鏡像**: 若原始碼結構發生變動 (e.g., 移動了某個 module)，此處的設計文件也應進行相應的目錄調整。
*   **測試關聯**: 每個組件設計都應對應一份測試計畫 (`testing/` 下)，確保實作符合設計預期。
