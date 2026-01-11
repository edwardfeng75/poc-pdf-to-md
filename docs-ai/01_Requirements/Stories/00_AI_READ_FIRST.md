# 01_Requirements/Stories (用戶故事) 導航

<docs-ai-ruies>

1. 與本文件同一層的文件有更動時，需要更新本文件

2. 本文件不在 docs-ai/ 時，本文件的上層引用文件是上層的 00_AI_READ_FIRST.md

3. 不得更動 <docs-ai-ruies> 的內容
</docs-ai-ruies>

## 1. 本目錄的任務

本目錄存放所有 **User Stories (用戶故事)** 的詳細規格文件。
每個 Story 都是一個可獨立開發、測試與驗收的功能單元。

## 2. 檔案命名規範

請遵循以下命名格式：

`Story-<ID>-<簡短描述>.md`

*   **ID**: 3位數字，例如 `001`, `012`。此 ID 應與 `../Use_Case_Diagram.puml` 中的標註一致。
*   **簡短描述**: 使用英文或底線分隔的中文，簡明扼要。

範例：
*   `Story-001-Parse_PDF_File.md`
*   `Story-002-Generate_Markdown_With_AI.md`

## 3. Story 文件模板

新增 Story 時，請複製以下模板：

```markdown
# Story-<ID>: <標題>

## 1. User Story
**As a** <角色>
**I want** <功能/行為>
**So that** <價值/目的>

## 2. Acceptance Criteria (驗收標準)

### Scenario 1: <場景描述>
- **Given**: <前置條件>
- **When**: <操作行為>
- **Then**: <預期結果>

### Scenario 2: <場景描述>
...

## 3. 技術規格與約束
*   **API**: (若有相關 API，請連結至 `../../02_Contracts/`)
*   **資料結構**: (若涉及資料庫變更)
*   **效能需求**:

## 4. UI/UX 描述 (僅限前端)
*   (描述畫面流或互動細節)

## 5. 關聯資訊
*   **Use Case**: (連結至 Use Case Diagram 中的節點)
*   **Parent Feature**: (所屬的大功能模組)
```

## 4. 維護規則

1.  **粒度控制**: 一個 Story 的開發週期建議控制在 1-3 天內。如果過大，請拆分為多個 Stories。
2.  **狀態同步**: 完成開發後，請確保 Story 文件中的描述與最終實作一致 (SSOT)。
3.  **連結測試**: 這裡的 Acceptance Criteria 是 QA 撰寫測試計畫 (`../../03_Cross_Cutting_Scenarios/testing/`) 的主要依據。
