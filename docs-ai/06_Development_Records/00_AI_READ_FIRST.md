# Development Records 導航 (Dev Records Root)

<docs-ai-ruies>

1. 與本文件同一層的文件有更動時，需要更新本文件

2. 本文件不在 docs-ai/ 時，本文件的上層引用文件是上層的 00_AI_READ_FIRST.md

3. 不得更動 <docs-ai-ruies> 的內容
</docs-ai-ruies>

## 1. 本文件夾的主要任務

`docs-ai/06_Development_Records/` 負責記錄開發過程中的**動態資訊**。
其核心任務在於：
1.  **任務管理 (Tracking)**: 透過 Tickets 追蹤待辦事項與 Bug 修復。
2.  **進度記錄 (Logging)**: 透過 Worklogs 記錄每日的開發進展與遇到的問題。
3.  **計畫擬定 (Planning)**: 透過 Plans 記錄長期的遷移或重構計畫。

## 2. 目錄文件導覽

本目錄包含以下關鍵子目錄：

1.  **[tickets/ (開發工單)](./tickets/00_AI_READ_FIRST.md)**
    *   **內容**: 具體的功能實作或錯誤修復任務。
    *   **意圖**: 每個 Ticket 應對應一個明確的 User Story 或 Bug Report。

2.  **[worklogs/ (工作日誌)](./worklogs/00_AI_READ_FIRST.md)**
    *   **內容**: 按日期記錄的開發日誌。
    *   **意圖**: 記錄每日的變更摘要、決策思考與遇到的阻礙 (Blockers)。

3.  **[plans/ (開發計畫)](./plans/00_AI_READ_FIRST.md)**
    *   **內容**: 跨多個 Tickets 的大型計畫或重構方案。
    *   **意圖**: 規劃複雜的演進路徑，追蹤整體進度。

## 3. 維護規則

*   **即時更新**: 每次代碼提交 (Commit) 或 PR 前，建議更新對應的 Ticket 狀態與 Worklog。
*   **連結需求**: Ticket 必須明確連結到 `01_Requirements` 中的 Story ID。
