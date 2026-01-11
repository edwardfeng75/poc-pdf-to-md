# 產品需求文件 (PRD)

## 📋 產品元資料
- **產品名稱**: POC PDF to Markdown
- **產品版本**: v0.2.0 (Phase 2 Completed)
- **負責人**: Edward
- **建立日期**: 2026-01-03
- **最後更新**: 2026-01-11
- **狀態**: In Progress

## 🎯 產品目標

### 產品願景
開發一個高效的 PDF 轉 Markdown 工具，利用 PyMuPDF 進行精確的 PDF 解析與圖片提取，並結合 Gemini AI 的多模態能力進行高品質的文字與排版轉換。確保轉換後的 Markdown 既能保留原始文件的結構與圖片，又能提供易於編輯與閱讀的文本格式。

### 目標使用者
- **開發者**: 需要將技術文件或規格書從 PDF 轉換為 Markdown 以進行版本控制或發布。
- **內容創作者**: 需要將 PDF 格式的資料轉換為網頁或部落格文章。
- **研究人員**: 需要從論文 PDF 中提取文字與圖片進行整理與分析。

### 核心目標
1. **精確的圖文分離**: 準確提取 PDF 中的圖片（embedded images）並將每頁渲染為圖片，作為 AI 的視覺參考。
2. **AI 輔助的高品質轉換**: 利用 Gemini AI 識別頁面佈局與內容，生成包含正確圖片引用的 Markdown。
3. **可靠的批次處理與快取**: 支援斷點續傳與磁碟快取，避免重複呼叫 AI API，降低成本並提升效率。

## 🗺️ 功能全景

**說明**：功能全景列出支持核心目標的重點上位功能模組。這些是產品層級的功能分組，具體的實作細節與 Stories 對應關係請查看 `01_Requirements/Use_Case_Diagram.puml`。

### 功能模組清單
| 模組 | 說明 |
|------|------|
| **Phase 1: 解析與提取** | 使用 PyMuPDF 解析 PDF，提取內嵌圖片，並將每頁渲染為全頁圖片。產出詳細的 `parse_result.json` 中間檔。 |
| **Phase 2: AI 轉換** | 讀取解析結果，將每頁圖片與中繼資料傳送給 Gemini AI，生成 Markdown 內容並引用圖片。支援快取與並行處理。 |
| **CLI 介面** | 提供完整的命令列參數，支援指定模型、輸入輸出路徑、覆寫模式、僅解析模式等。 |
| **日誌與錯誤處理** | (待實作) 記錄執行過程與錯誤，提供除錯資訊。 |

**注意**：各模組的具體功能需求與 Stories 對應關係，請查看 `01_Requirements/Use_Case_Diagram.puml`。

## 🔗 相關檔案

### 必須參考
- `00_System_View/00_AI_READ_FIRST.md` - 系統全貌導航 (包含 Architecture 與 Tech Stack)
- `01_Requirements/Use_Case_Diagram.puml` - **系統層級的需求總覽**（重要）
  - 展示所有 Actors（參與者）與 Use Cases（用例）的關係
  - 每個 Use Case 標註對應的 Story ID
  - 展示 Use Cases 之間的 include/extend 關係（即需求相依關係）
  - **這是獲取所有需求關係與 Stories 對應的單一來源**
- `03_Cross_Cutting_Scenarios/Main_Flow.puml` - 核心流程循序圖
- `04_Component_Designs/src/poc_pdf_to_md/Class_Diagram.puml` - 核心類別設計圖

### Stories 詳細內容
- `01_Requirements/Stories/00_AI_READ_FIRST.md` - User Stories 導航與詳細需求
  - 請查看此目錄以獲取每個 Story 的完整資訊
  - **Story 之間的相依關係**：請查看 `01_Requirements/Use_Case_Diagram.puml` 中的 Use Cases 相依關係

## 📝 全局約束

### 技術約束
- **Python 版本**: 3.12+
- **專案管理**: 使用 `uv` 管理依賴與虛擬環境
- **PDF 引擎**: PyMuPDF (fitz)
- **AI 模型**: Google Gemini (預設 `gemini-3-pro-preview`)
- **中間格式**: `parse_result.json` 必須符合定義的 Schema 版本

### 安全性約束
- **API Key**: 必須透過環境變數 (`GEMINI_API_KEY`) 管理，不得硬編碼於代碼中。
- **檔案操作**: 所有檔案讀寫限制在指定的輸出目錄 (`output/`) 內，避免影響系統其他部分。

### 效能約束
- **並行處理**: Phase 2 支援多執行緒並行呼叫 AI API，預設並行數需可透過環境變數設定。
- **快取機制**: 必須優先檢查磁碟快取，避免不必要的 API 消耗。

## 🚫 不在範圍內

- **OCR 文字辨識**: Phase 1 目前不進行本地 OCR，文字辨識完全依賴 Phase 2 的 Vision AI 能力。
- **複雜表格重建**: 目前僅依賴 AI 的能力進行 Markdown 表格轉換，不保證複雜巢狀表格的完美還原。
- **GUI 介面**: 目前僅提供 CLI 介面。