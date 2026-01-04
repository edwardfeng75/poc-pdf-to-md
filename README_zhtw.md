# PDF 轉 Markdown 工具

[English](README.md)

一個支援圖片提取與 AI 輔助轉換的 PDF 轉 Markdown 工具。使用 PyMuPDF 進行 PDF 解析，Gemini AI 進行文字轉換，分兩階段執行以確保解析品質。

## 功能特色

- **PDF 解析**：使用 PyMuPDF 提取 PDF 中的文字與圖片
- **圖片提取**：自動提取 PDF 中的圖片並儲存為獨立檔案
- **字體大小檢測**：自動檢測文字的字體大小，用於未來 Markdown 標題等級（h1-h5）判斷
- **AI 轉換**：使用 Gemini AI 將文字內容轉換為 Markdown 格式
- **兩階段處理**：先解析 PDF 產生中間產出，再進行 Markdown 轉換，確保品質
- **完整測試**：包含單元測試、整合測試與端對端測試

## 專案狀態

- **Phase 1**：PDF 解析與可檢查的中間產出（已完成）
- **Phase 2**：以解析產出作為輸入，轉換 Markdown（已完成）

## 系統需求

- Python >= 3.14.0
- uv（Python 套件管理工具）

## 如何設定運行環境

### 1. 安裝 uv

如果尚未安裝 `uv`，請先安裝：

```bash
# macOS / Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# 或使用 pip
pip install uv
```

### 2. 複製專案

```bash
git clone <repository-url>
cd poc-pdf-to-md
```

### 3. 安裝依賴套件

使用 `uv` 安裝專案依賴：

```bash
uv sync
```

這會自動：
- 建立虛擬環境（`.venv`）
- 安裝所有依賴套件（PyMuPDF、Google Generative AI SDK 等）
- 安裝開發依賴（pytest）

### 4. 設定環境變數（Phase 2 需要）

複製 `.env.example` 並設定 API 金鑰：

```bash
cp .env.example .env
```

編輯 `.env` 檔案，填入您的 Google Generative AI API 金鑰：

```bash
GEMINI_API_KEY=your_api_key_here
GEMINI_MODEL=gemini-3-pro-preview
GEMINI_CONCURRENCY=10 # 選填：設定 Phase 2 的並發數（預設：10）
```

**注意**：Phase 1（PDF 解析）不需要 API 金鑰，只有 Phase 2（Markdown 轉換）才需要。

## 如何使用（uv）

### 查看說明

```bash
uv run poc-pdf-to-md --help
```

### Phase 1：解析 PDF（僅解析，不轉換）

```bash
uv run poc-pdf-to-md --input <pdf檔案路徑> --parse-only
```

**範例**：

```bash
uv run poc-pdf-to-md --input test_data/test_data.pdf --parse-only
```

**輸出**：
- `output/parsed/parse_result_<timestamp>.json`：解析結果 JSON 檔案
- `output/images/<uuid>.png|jpg`：提取的圖片檔案

### Phase 2：從解析結果轉換為 Markdown

```bash
uv run poc-pdf-to-md --from-parse <parse_result.json路徑>
```

**範例**：

```bash
uv run poc-pdf-to-md --from-parse output/parsed/parse_result_20260102_160622.json
```

## 命令列參數說明

| 參數 | 說明 | 必填 | 預設值 |
|------|------|------|--------|
| `--input <path>` | PDF 檔案路徑（除非使用 `--from-parse`） | 條件式 | - |
| `--output <dir>` | 輸出目錄 | ❌ | `output/` |
| `--parse-only` | 僅執行 Phase 1（解析），不進行轉換 | ❌ | `false` |
| `--from-parse <path>` | 使用已解析的 JSON 檔案進行 Phase 2 轉換 | ❌ | - |
| `--model <name>` | AI 模型名稱（優先序：--model > GEMINI_MODEL 環境變數 > 預設值） | ❌ | `gemini-3-pro-preview` |
| `--prompt-file <path>` | Phase 2 使用的 Prompt 模板 Markdown 檔案 | ❌ | `prompts/phase2_page_to_md.md` |
| `--overwrite` | 覆寫輸出目錄內既有檔案（刪除既有 `parsed/`、`images/`、`logs/` 與 `output_*.md`） | ❌ | `false` |

## 參數優先序

**模型名稱優先序**：
1. `--model` CLI 參數（最高優先）
2. `GEMINI_MODEL` 環境變數
3. 預設值 `gemini-3-pro-preview`

## 輸出檔案結構

執行後會在輸出目錄產生以下結構：

```
output/
├── parsed/
│   └── parse_result_<timestamp>.json  # 解析結果 JSON
├── images/
│   ├── <uuid>.png                     # 提取的圖片檔案
│   └── <uuid>.jpg
├── phase2/
│   ├── pages/                         # 每頁的中間產出 Markdown
│   │   └── page_0000.md
│   └── state.json                     # 用於中斷恢復的狀態檔
└── output_<timestamp>.md              # 最終合併的 Markdown 檔案
```

## 如何運行測試

### 執行所有測試

```bash
uv run pytest tests/ -v
```

### 執行特定測試檔案

```bash
# CLI 測試
uv run pytest tests/test_cli.py -v

# PDF 解析器測試
uv run pytest tests/test_pdf_parser.py -v

# 圖片處理測試
uv run pytest tests/test_image_handler.py -v

# 解析結果測試
uv run pytest tests/test_parse_result.py -v

# Phase 1 整合測試
uv run pytest tests/test_engine.py -v

# Phase 2 測試
uv run pytest tests/test_phase2.py -v
```

## 常見問題

### Q: Phase 1 執行後沒有產生圖片？

A: 請確認 PDF 檔案中包含圖片。某些 PDF 可能使用向量圖形而非點陣圖，這些不會被提取。

### Q: 如何檢查解析結果是否正確？

A: 查看 `output/parsed/parse_result_<timestamp>.json` 檔案，確認：
- `blocks` 陣列中的 `blockIndex` 是否連續
- 圖片區塊是否包含 `imagePath`、`ext`、`width`、`height`
- `page_index` 和 `bbox` 是否正確

### Q: 如何執行 Phase 2？

A: 請先執行 Phase 1 取得解析結果 JSON，再使用 `--from-parse <json路徑>` 參數進行 Markdown 轉換。

### Q: 如何取得 Google Generative AI API 金鑰？

A: 請前往 [Google AI Studio](https://makersuite.google.com/app/apikey) 申請 API 金鑰。

## 授權

本專案為 PoC（概念驗證）專案。

## 貢獻

歡迎提交 Issue 或 Pull Request！
