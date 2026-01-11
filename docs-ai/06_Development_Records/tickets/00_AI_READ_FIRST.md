# Tickets 導航

<docs-ai-ruies>

1. 與本文件同一層的文件有更動時，需要更新本文件

2. 本文件不在 docs-ai/ 時，本文件的上層引用文件是上層的 00_AI_READ_FIRST.md

3. 不得更動 <docs-ai-ruies> 的內容
</docs-ai-ruies>

## 1. 本目錄的任務

`docs-ai/06_Development_Records/tickets/` 存放具體的開發任務工單。

## 2. 檔案命名規範

`Ticket-<ID>-<簡短描述>.md`

*   **ID**: 3位數字，流水號 (e.g., 001, 002)。
*   **簡短描述**: 使用英文或底線分隔的中文。

範例：
*   `Ticket-001-Init_Project_Structure.md`
*   `Ticket-002-Impl_PDF_Parser.md`

## 3. Ticket 模板

```markdown
# Ticket-<ID>: <標題>

## 1. 關聯需求
*   **Story**: (連結至 `../../01_Requirements/Stories/`)
*   **Type**: [Feature | Bug | Chore | Refactor]

## 2. 任務描述
簡述要完成的工作內容。

## 3. 實作計畫 (Checklist)
- [ ] Step 1
- [ ] Step 2

## 4. 驗收結果
*   (填寫測試結果或截圖)
```
