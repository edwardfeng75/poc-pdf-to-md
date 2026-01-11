# Architecture Decision Records 導航

<docs-ai-ruies>

1. 與本文件同一層的文件有更動時，需要更新本文件

2. 本文件不在 docs-ai/ 時，本文件的上層引用文件是上層的 00_AI_READ_FIRST.md

3. 不得更動 <docs-ai-ruies> 的內容
</docs-ai-ruies>

## 1. 本目錄的任務

`docs-ai/05_Principles/ADR/` 存放專案所有的**架構決策記錄 (ADR)**。
ADR 是一種輕量級的文件格式，用於捕捉重要的架構決策，以及決策當時的情境與後果。

## 2. 檔案命名規範

請遵循以下命名格式：

`ADR-<ID>-<簡短標題>.md`

*   **ID**: 3位數字，流水號 (e.g., 001, 002)。
*   **簡短標題**: 使用英文或底線分隔的中文。

範例：
*   `ADR-001-Use_PostgreSQL_As_Primary_DB.md`
*   `ADR-002-Adopt_Clean_Architecture.md`

## 3. ADR 模板

新增 ADR 時，請複製以下模板：

```markdown
# ADR-<ID>: <標題>

## Status
*   [Proposed | Accepted | Deprecated | Superseded]

## Context
*   我們面臨什麼問題？
*   有哪些限制條件？
*   為什麼需要做這個決策？

## Decision
*   我們決定做什麼？
*   我們選擇了什麼技術/方案？

## Consequences
*   **Positive**: 這個決策帶來的好處。
*   **Negative**: 這個決策帶來的壞處或成本。
*   **Risks**: 潛在的風險。
```

## 4. 維護規則

*   **不可變更**: 一旦 Status 變為 `Accepted`，內容就不應再修改。如果情況改變，請建立新的 ADR 並將舊的標記為 `Superseded`。
*   **編號管理**: 請確保 ID 連號，不要跳號。
