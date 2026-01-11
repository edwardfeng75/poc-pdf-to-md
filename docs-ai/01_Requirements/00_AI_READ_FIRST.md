# Requirements 導航 (Requirements Root)

<docs-ai-ruies>

1. 與本文件同一層的文件有更動時，需要更新本文件

2. 本文件不在 docs-ai/ 時，本文件的上層引用文件是上層的 00_AI_READ_FIRST.md

3. 不得更動 <docs-ai-ruies> 的內容
</docs-ai-ruies>

## 1. 本文件夾的主要任務

`docs-ai/01_Requirements/` 是所有設計與開發工作的**源頭與起點**。
其核心任務在於：
1.  **定義目標 (Product Goal)**: 透過 PRD 說明產品願景、目標與範圍。
2.  **定義行為 (User Behavior)**: 透過 Use Cases 與 Stories 描述系統應如何回應使用者操作。
3.  **確保追溯 (Traceability)**: 提供唯一的識別代碼 (Story ID / Use Case ID)，讓所有設計與程式碼都能回溯至具體需求。

## 2. 目錄文件導覽

本目錄包含以下關鍵文件，建議按照**閱讀順序**進行理解：

1.  **[PRD.md (產品需求文件)](./PRD.md)**
    *   **內容**: 產品願景、目標使用者、功能全景、全域約束 (技術/資安)。
    *   **意圖**: 建立對產品的宏觀認知，理解「為什麼要做」以及「核心限制」。
    *   **何時閱讀**: 專案啟動、新成員加入、確認產品邊界時。

2.  **[Use_Case_Diagram.puml (用例圖)](./Use_Case_Diagram.puml)**
    *   **內容**: 系統功能的視覺化地圖，展示 Actors 與 Use Cases 的互動關係。
    *   **意圖**: 提供需求的結構化視圖，並作為 Story 與 Use Case 的索引。
    *   **關鍵功能**: 每個 Use Case 應對應一個或多個具體的 User Story。

3.  **[Stories/ (使用者故事)](./Stories/00_AI_READ_FIRST.md)**
    *   **內容**: 詳細的 `Story-XXX.md` 文件集合。
    *   **意圖**: 描述單一功能的具體需求、驗收標準 (AC) 與業務邏輯。
    *   **何時閱讀**: 進行具體功能設計、開發或編寫測試案例時。

## 3. 需求追溯與維護

*   **唯一真理 (SSOT)**: 所有的功能開發都必須源自於此處的 Story。若開發過程中發現新需求，應先在此處建立 Story，而非直接寫 Code。
*   **變更管理**: 修改 PRD 或 Use Case 時，需評估對現有 Story 與下游客戶端 (Design/Code) 的影響。
*   **ID 關聯**: 在設計文件 (04_Component_Designs) 與測試文件 (03_Cross_Cutting_Scenarios/testing) 中，應明確引用此處的 Story ID (e.g., "Ref: Story-001")。
