# System View 導航 (System View Root)

<docs-ai-ruies>

1. 與本文件同一層的文件有更動時，需要更新本文件

2. 本文件不在 docs-ai/ 時，本文件的上層引用文件是上層的 00_AI_READ_FIRST.md

3. 不得更動 <docs-ai-ruies> 的內容
</docs-ai-ruies>

## 1. 本文件夾的主要任務

`docs-ai/00_System_View/` 的主要任務是提供系統的**宏觀靜態視圖**。
它定義了：
1.  **技術基石**：專案所依賴的語言、框架與工具 (Tech Stack)。
2.  **系統架構**：組件如何劃分以及它們之間的關係 (Architecture)。
3.  **部署架構**：軟體如何在物理或虛擬環境中運行 (Deployment)。

## 2. 目錄文件說明

本目錄包含以下關鍵文件，建議依照需求閱讀：

1.  **[Tech_Stack.md (技術棧)](./Tech_Stack.md)**
    *   **內容**: 定義 Python 版本、核心依賴 (PyMuPDF, Google GenAI)、開發工具 (uv, pytest) 等選型。
    *   **意圖**: 確保所有開發者使用一致的工具鏈與技術標準。
    *   **何時閱讀**: 專案初始化、添加新依賴、或查詢特定工具版本時。

2.  **[Architecture.puml (系統架構圖)] (待建立)**
    *   **內容**: 系統的高層次邏輯架構圖 (C4 Model - Container/Component Level)。
    *   **意圖**: 展示系統內部的模組劃分與互動關係。

3.  **[Deployment.puml (部署架構圖)] (待建立)**
    *   **內容**: 系統的運行環境配置 (Local, Cloud)。
    *   **意圖**: 展示應用程式如何部署與運行。

## 3. 維護與相依性

*   **Tech Stack 更新**: 當 `pyproject.toml` 有重大變更 (如引入新的核心庫或更換建置工具) 時，必須同步更新 `Tech_Stack.md`。
*   **架構演進**: 當系統引入新的頂層模組或改變核心互動模式時，需評估是否需要建立或更新 `Architecture.puml`。
