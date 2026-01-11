# Plans 導航

<docs-ai-ruies>

1. 與本文件同一層的文件有更動時，需要更新本文件

2. 本文件不在 docs-ai/ 時，本文件的上層引用文件是上層的 00_AI_READ_FIRST.md

3. 不得更動 <docs-ai-ruies> 的內容
</docs-ai-ruies>

## 1. 本目錄的任務

`docs-ai/06_Development_Records/plans/` 存放跨越單一 Ticket 範圍的大型計畫、遷移方案或重構藍圖。

## 2. 檔案命名規範

`Plan-<簡短描述>.md`

範例：
*   `Plan-Migrate_To_PostgreSQL.md`
*   `Plan-Phase2_Implementation.md`

## 3. Plan 模板

```markdown
# Plan: <標題>

## 1. 目標與背景
為什麼需要這個計畫？預期達成什麼目標？

## 2. 執行策略 (Strategy)
我們打算怎麼做？分幾個階段？

## 3. 階段規劃 (Phases)
### Phase 1: <名稱>
- [ ] Task A
- [ ] Task B

### Phase 2: <名稱>
- [ ] Task C

## 4. 風險評估
*   可能的風險與應對措施。
```
