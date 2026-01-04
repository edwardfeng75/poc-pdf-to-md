# PDF 轉 Markdown 工具開發計畫

## 專案概述

開發一個 PDF 轉 Markdown 的工具，支援圖片提取與 AI 輔助轉換。使用 PyMuPDF 進行 PDF 解析，Gemini AI 進行文字轉換，分兩階段執行以確保解析品質。

**目前代碼現況（截至 2026-01-03）**
- Phase 1 已完成，解析輸出以「圖片」為主：**每頁渲染為 page PNG + 提取 embedded images**
- **暫未解析文字區塊（text blocks）**（Phase 1 目前只做 embedded images 掃描與整頁渲染）
- Phase 2 已完成基本轉換：讀取 `parse_result*.json` → 依頁呼叫 Gemini（prompt 文字 + 本頁截圖 PNG）→ 產出 per-page Markdown → 串接成 `output_<timestamp>.md`
- Phase 2 支援續跑/快取：
  - per-page 輸出：`outputDir/phase2/pages/page_0000.md`
  - 狀態檔：`outputDir/phase2/state.json`
  - **磁碟快取是事實來源**：只要 `page_XXXX.md` 已存在就會跳過 AI 呼叫（即使 prompt 或 model 改變）
- 目前尚未產生實際 log（僅預留 `outputDir/logs/`；`--overwrite` 會清空該目錄）
- CLI 行為：
  - Phase 1：`--parse-only`
  - Phase 2：`--from-parse <parse_result.json>`
  - 只提供 `--input`（未加 `--parse-only/--from-parse`）目前只會跑 Phase 1，並印出「Phase 2 conversion is not yet implemented」提示（實際上 Phase 2 已可透過 `--from-parse` 執行）
  - `--overwrite` 目前**不會**清空 `outputDir/phase2/`（需手動清理才會強制重跑 Phase 2）

## 測試策略

### 測試工具與執行方式

- 使用 `uv` 管理 Python 專案與依賴套件
- 使用 `pytest` 作為測試框架
- 透過 `uv run pytest` 執行測試
- 測試腳本必須包含三個階段：setup（準備）、test（測試執行）、teardown（清理）

### 測試腳本結構

每個測試腳本應遵循以下結構：

1. **Setup 階段**：準備測試環境
   - 建立臨時目錄與檔案
   - 初始化測試資料
   - 設定測試所需的環境變數或模擬物件

2. **Test 階段**：執行測試案例
   - 執行被測試的功能
   - 驗證預期結果
   - 檢查輸出檔案與資料結構

3. **Teardown 階段**：清理測試環境
   - 刪除臨時檔案與目錄
   - 清理測試產生的資源
   - 重置環境狀態

### 測試範圍

- **單元測試**：針對個別函數與模組進行測試
- **整合測試**：測試多個模組之間的協作
- **端對端測試**：測試完整的處理流程
- **錯誤處理測試**：驗證各種錯誤情況的處理機制

### 測試資料管理

- 測試資料存放在 `test_data/` 目錄
- 測試過程中產生的臨時檔案應在 teardown 階段清理
- 避免測試檔案互相干擾，使用時間戳或 UUID 確保唯一性

## 專案設定

- [x] 使用 uv 初始化 Python 專案
- [x] 設定專案結構（src/ 目錄）
- [x] 設定 .venv / .env / git / gitignore
- [x] 安裝依賴套件（PyMuPDF、Google Generative AI SDK 等）
- [x] 建立 output/ 目錄結構（parsed/、images/、logs/）

### 驗證項目
- [x] 專案結構符合約定
- [x] 依賴套件可正常安裝
- [x] 目錄結構建立完成

## Phase 1：PDF 解析與可檢查的中間產出

### 1.1 CLI 介面開發

- [x] 實作 CLI 參數解析
  - [x] `--input <pdf_path>`：PDF 檔案路徑（必填）
  - [x] `--output <output_dir>`：輸出目錄（可選，預設：output/）
  - [x] `--model <model_name>`：AI 模型（可選，優先序：--model > GEMINI_MODEL 環境變數 > 預設值 gemini-3-pro-preview）
  - [x] `--parse-only`：只產出 PDF 解析結果，不進行轉換（與 `--from-parse` 互斥）
  - [x] `--from-parse <path>`：直接以解析產出作為輸入，進行轉換（與 `--parse-only` 互斥）
  - [x] `--overwrite`：清空 `outputDir` 下既有產物並以固定檔名輸出（方便反覆開發/迭代）
    - [x] 清空範圍：`outputDir/parsed/`、`outputDir/images/`、`outputDir/logs/` 與 `outputDir/output_*.md`
    - [x] 固定檔名：`outputDir/parsed/parse_result.json`（覆蓋既有檔案）
- [x] 實作參數互斥驗證（`--parse-only` 與 `--from-parse` 不能同時使用）
- [x] 實作輸入驗證（檢查 PDF 檔案是否存在）
- [x] 實作錯誤處理與訊息顯示

#### 驗證項目
- [x] CLI 參數可正確解析
- [x] 輸入驗證功能正常運作
- [x] 錯誤訊息清楚明確
- [x] `--parse-only` 模式可正常執行

#### 測試項目
- [x] 撰寫 CLI 參數解析測試腳本（包含 setup/test/teardown）
- [x] 測試所有 CLI 參數的正確解析
- [x] 測試參數互斥驗證（`--parse-only` 與 `--from-parse` 同時使用應報錯）
- [x] 測試輸入驗證（不存在的 PDF 檔案應報錯）
- [x] 測試錯誤訊息的格式與內容
- [x] 使用 `uv run pytest` 執行測試並通過（64 passed）

### 1.2 PDF 解析器開發

- [x] 實作 PDF 開啟功能（使用 PyMuPDF）
- [x] 實作 PDF 解析功能 `parsePdf(doc)`（目前只輸出 embedded images，不處理文字區塊）
  - [x] 依順序讀取所有頁面（page_index 從 0 開始）
  - [x] 識別圖片區塊（embedded image）
    - [x] 記錄圖片區塊的 bbox（bounding box，座標資訊）
    - [x] 記錄圖片區塊的 xref（原始來源資訊）
  - [x] 實作 blockIndex 排序邏輯
    - [x] 排序規則：先依 `page_index` 排序（由小到大）
    - [x] 同頁內依 bbox 的 `y` 座標排序（由上到下）
    - [x] 若 `y` 座標相同或相近（容差範圍內），則依 `x` 座標排序（由左到右）
    - [x] 記錄每個 block 的 blockIndex（排序後的順序）
- [x] 實作每頁渲染功能 `renderPageAsImage(page)`
  - [x] 將整頁渲染為 PNG（用於人工檢查與後續 OCR/AI 使用）
- [x] 實作圖片提取功能 `extractImage(imageRef)`
  - [x] 使用 `page.get_images(full=true)` 取得 xref
  - [x] 使用 `doc.extract_image(xref)` 取得 image bytes 與元資料
  - [x] 回傳 imageBytes + imageMeta（包含 ext、width、height、xref 等）

#### 驗證項目
- [x] PDF 檔案可正常開啟
- [ ] 文字區塊可正確識別與提取（目前未納入 Phase 1，暫不實作）
- [x] 圖片區塊可正確識別
- [x] blockIndex 順序正確
- [x] 圖片元資料完整

#### 測試項目
- [x] 撰寫 PDF 解析器測試腳本（包含 setup/test/teardown）
- [x] 測試 PDF 檔案開啟功能
- [x] 測試圖片區塊識別（embedded images）
- [x] 測試 blockIndex 排序邏輯（page_index → bbox.y → bbox.x）
- [x] 測試圖片提取功能與元資料完整性
- [x] 測試多頁 PDF 的解析
- [x] （回歸）確認不解析文字區塊（text blocks removed / not used）
- [x] 使用 `uv run pytest` 執行測試並通過（64 passed）

### 1.3 圖片處理與儲存

- [x] 實作圖片檔案命名（使用 UUID，避免檔名衝突）
- [x] 實作頁面圖片命名（使用 page_0000.png 形式，方便定位頁碼）
- [x] 實作圖片檔案寫入功能
  - [x] 儲存到 `outputDir/images/<uuid>.png` 或 `<uuid>.jpg`
  - [x] 頁面渲染圖儲存到 `outputDir/images/page_0000.png`（依頁碼遞增、**固定檔名**；overwrite=false 時若檔案已存在仍會覆蓋，屬預期行為）
  - [x] 根據圖片格式選擇副檔名
  - [x] 確保每個圖片檔案使用唯一 UUID，避免覆蓋
- [x] 實作 `updateParseResultImagePath()` 功能
  - [x] 更新 parseResult 中對應 block 的 imagePath

#### 驗證項目
- [x] 圖片檔案可正常寫入
- [x] 檔案命名符合 UUID 格式
- [x] 圖片格式正確（PNG/JPG）
- [x] parseResult 中的 imagePath 正確更新

#### 測試項目
- [x] 撰寫圖片處理測試腳本（包含 setup/test/teardown）
- [x] 測試圖片檔案命名（UUID 格式）
- [x] 測試圖片檔案寫入功能
- [x] 測試不同圖片格式的處理（PNG/JPG）
- [x] 測試 `updateParseResultImagePath()` 功能
- [x] 測試圖片檔案不會互相覆蓋（UUID 圖片）
- [x] 在 teardown 階段清理測試產生的圖片檔案
- [x] 使用 `uv run pytest` 執行測試並通過（64 passed）

### 1.4 解析結果輸出

- [x] 定義 parse_result.json 結構
  - [x] Run-level metadata（檔案層級資訊）
    - [x] `schema_version`：結構版本號（例如："1.0"）
    - [x] `created_at`：建立時間（ISO 8601 格式）
    - [x] `source_pdf`：來源 PDF 檔案路徑
    - [x] `total_pages`：PDF 總頁數
  - [x] Block-level metadata（區塊層級資訊）
    - [x] `blockIndex`：排序後的順序（從 0 開始）
    - [x] `page_index`：頁面索引（從 0 開始）
    - [x] `type`：區塊類型（目前支援 "page_image"、"image"）
    - [x] `imagePath`：圖片檔案路徑（相對於 outputDir）
    - [x] `ext`：圖片副檔名（例如："png"、"jpg"）
    - [x] `width`：圖片寬度（像素）
    - [x] `height`：圖片高度（像素）
    - [x] （當 type="image" 時）`bbox`：邊界框座標 `[x0, y0, x1, y1]`（用於排序與除錯）
    - [x] （當 type="image" 時）`xref`：圖片在 PDF 中的 xref 編號（原始來源資訊）
    - [ ] （保留擴充）`type="text"`：文字區塊（目前未輸出）
- [x] 實作解析結果寫入功能
  - [x] 預設寫入到 `outputDir/parsed/parse_result_<timestamp>.json`（使用時間戳避免檔名衝突）
  - [x] `--overwrite` 時寫入到 `outputDir/parsed/parse_result.json`（固定檔名，便於反覆開發）
  - [x] 時間戳格式：YYYYMMDD_HHMMSS（例如：20250115_143022）
- [x] 實作輸出路徑顯示功能 `printParseOutputPath()`

#### 驗證項目
- [x] parse_result.json 格式正確
- [x] Run-level metadata 完整（schema_version、created_at、source_pdf、total_pages）
- [x] 所有 blocks 都正確記錄
- [x] 每個 block 都包含 page_index（embedded image blocks 另包含 bbox/xref；page_image blocks 不包含 bbox）
- [x] blockIndex 順序符合排序規則（page_image 先依 page_index；embedded images 再依 page_index → bbox.y → bbox.x）
- [x] 圖片路徑正確
- [x] embedded image blocks 包含完整的原始來源資訊（xref、ext、width、height）
- [x] page_image blocks 包含完整的圖片資訊（imagePath、ext、width、height）
- [x] 輸出路徑可正確顯示

#### 測試項目
- [x] 撰寫解析結果輸出測試腳本（包含 setup/test/teardown）
- [x] 測試 parse_result.json 格式正確性
- [x] 測試 Run-level metadata 完整性
- [x] 測試 Block-level metadata 完整性
- [x] 測試 blockIndex 順序符合排序規則
- [x] 測試時間戳格式正確性
- [x] 測試輸出路徑顯示功能
- [x] 在 teardown 階段清理測試產生的 JSON 檔案
- [x] 使用 `uv run pytest` 執行測試並通過（64 passed）

### Phase 1 整體驗證

- [x] 使用測試資料執行 Phase 1（例如：`test_data/test_data.pdf`、`test_data/test_data2.pdf`）
- [x] 驗證 parse_result 檔名預設使用時間戳避免覆蓋（overwrite=false）
- [x] 驗證 embedded images 檔名使用 UUID 避免覆蓋（overwrite=false）
- [x] 頁面渲染圖使用固定命名 `page_0000.png`（重跑可能覆蓋，屬預期行為）
- [x] 檢查 parse_result.json 內容正確性
  - [x] 驗證 Run-level metadata 存在且格式正確
  - [x] 驗證每個 block 都包含 page_index（embedded image blocks 另包含 bbox）
  - [x] 驗證 blockIndex 順序符合排序規則（page_image 先依 page_index；embedded images 再依 page_index → bbox.y → bbox.x）
- [x] 檢查圖片檔案是否正確提取與儲存
- [x] 驗證 blockIndex 排序邏輯正確（page_index → bbox.y → bbox.x）
- [x] 驗證 `--parse-only` 模式可正常運作
- [x] 驗證 `--parse-only` 與 `--from-parse` 互斥檢查正常運作
- [x] 執行時顯示進度（TTY 時以單行更新方式輸出）

#### 測試項目
- [x] 撰寫 Phase 1 整合測試腳本（包含 setup/test/teardown）
- [x] 使用測試資料執行完整 Phase 1 流程
- [x] 驗證 parse_result.json 內容正確性
- [x] 驗證圖片檔案正確提取與儲存
- [x] 驗證 blockIndex 排序邏輯正確性
- [x] 測試 `--parse-only` 模式的完整流程
- [x] 測試參數互斥檢查功能
- [x] 在 teardown 階段清理所有測試產物
- [x] 使用 `uv run pytest` 執行測試並通過（64 passed）

## Phase 2：以解析產出作為輸入，轉換 Markdown（含圖片）

Phase 2 目標（更新）：
- 以 page 為單位處理：每頁送 `images/page_<page_index:04d>.png` 與該頁 embedded images 資訊給 Gemini，回收「該頁」Markdown 內容
- 該頁 Markdown **必須包含對圖片的引用**（使用 `images/...` 路徑）
- 提示詞可快速調整：提示詞內容獨立成 md 文件，程式於執行時讀取（可用 CLI 參數指定/覆寫）
- 每頁額外提供該頁的 `pageParseDict`（從 parse_result.json 擷取的原始 JSON）供 AI 參考（提示詞需明示可使用此資料）

### 2.1 解析結果讀取

- [x] 實作 `convertToMarkdown(parseInputPath, outputDir, model)` 函數（已可完成 Phase 2：讀取 → 分頁 → 呼叫 AI → 串接 → 輸出）
- [x] 實作解析結果讀取功能
  - [x] 讀取 `parseInputPath` 指定的 parse_result.json
  - [x] 驗證 JSON 格式正確性
  - [x] 驗證 schema_version 相容性
  - [x] 載入 parseResult 資料結構
  - [x] 驗證 blockIndex 順序完整性（確保 blockIndex 連續且從 0 開始）
- [x] Phase 2 介面更新：`convertToMarkdown(parseInputPath, outputDir, model, promptFile)`
- [x] 新增 `--prompt-file <path>` 參數（預設：`prompts/phase2_page_to_md.md`）
- [x] 讀取並驗證提示詞模板（md 文件）
- [x] 將 parseResult 依 `page_index` 分組（page_image + embedded images）

#### 驗證項目
- [x] 可正確讀取 parse_result.json
- [x] JSON 格式驗證正常
- [x] parseResult 資料結構正確載入
- [x] 提示詞模板可正確讀取
- [x] 每個 page 都可建立正確的輸入資料（pageImagePath + embeddedImagesMeta + pageParseDict）

#### 測試項目
- [x] 撰寫解析結果讀取測試腳本（包含 setup/test/teardown）
- [x] 測試 parse_result.json 讀取功能
- [x] 測試 JSON 格式驗證
- [x] 測試 schema_version 相容性檢查
- [x] 測試 blockIndex 順序完整性驗證
- [x] 測試錯誤情況（格式錯誤、schema 不相容等）
- [x] 在 teardown 階段清理測試產生的檔案
- [x] 使用 `uv run pytest` 執行測試並通過（64 passed）
- [x] 測試提示詞模板讀取（檔案不存在/空檔/不可讀）
- [x] 測試 per-page 分組：同頁 embedded images 正確收斂到該頁輸入資料

### 2.2 AI 整合開發

- [x] 設定 Google Generative AI SDK（使用 `google-genai`；import path：`google.genai`）
- [x] 實作 API 金鑰管理（使用環境變數或 .env：`GEMINI_API_KEY` / `GOOGLE_API_KEY`）
- [x] 實作模型參數解析邏輯（CLI 層）
  - [x] 優先序：`--model` CLI 參數 > `GEMINI_MODEL` 環境變數 > 預設值 `gemini-3-pro-preview`
- [x] 實作 `generatePageMarkdown(...)` 函數
  - [x] 呼叫 Gemini API（multimodal：圖片 + 文字提示詞）
  - [x] 傳遞 page PNG（圖片）與 embedded images / pageParseDict（以 JSON 附加在 prompt 末尾）
  - [x] 要求輸出為「該頁」Markdown，並引用 `images/...`（含 page 圖與 embedded 圖）
  - [x] 處理 API 回應與錯誤（空回應視為錯誤）
  - [x] 回傳 pageMd（Markdown）

#### 驗證項目
- [x] API 金鑰可正確讀取（支援 `GEMINI_API_KEY` / `GOOGLE_API_KEY`；缺失時會報錯）
- [ ] Gemini API 連線正常
- [ ] 每頁可成功產出 pageMd
- [ ] pageMd 內容包含圖片引用（`images/page_XXXX.png` + `images/<uuid>.*`）

#### 測試項目
- [ ] 撰寫 AI 整合測試腳本（包含 setup/test/teardown）
- [ ] 測試 API 金鑰讀取（環境變數與 .env）
- [x] 測試模型參數解析邏輯（優先序驗證，CLI 層）
- [ ] 測試 `generatePageMarkdown()` 函數（以 mock 方式驗證輸入包含：promptTemplate + pageImagePath + embeddedImagesMeta）
- [ ] 測試 Gemini API 回應處理（mock 回傳 pageMd）
- [ ] 測試 API 錯誤處理（金鑰錯誤、連線失敗等）
- [ ] 使用 mock 物件測試 API 呼叫邏輯（避免實際 API 呼叫）
- [ ] 在 teardown 階段清理測試環境變數
- [ ] 使用 `uv run pytest` 執行測試並通過

### 2.3 Markdown 組合邏輯

- [x] 實作依 page_index 順序處理 pages 的迴圈
- [x] 組合 per-page 輸入資料
  - [x] pageImagePath：`images/page_<page_index:04d>.png`
  - [x] embeddedImagesMeta：從 parseResult 過濾 `type=image` 且 `page_index` 相同（至少包含 imagePath；包含 bbox/xref/尺寸）
- [x] pageParseDict：從 parseResult 擷取該頁相關 blocks 的原始 JSON（page_image + embedded images）
- [x] 呼叫 `generatePageMarkdown(...)` 取得 pageMd，並以串接方式組合結果
- [x] 加入頁分隔（`---`）

#### 驗證項目
- [x] pages 處理順序正確（依 page_index 由小到大）
- [ ] 每頁 pageMd 都包含對該頁圖片的引用
- [x] 最終 Markdown 串接順序正確（頁序）

#### 測試項目
- [x] 撰寫 Markdown 組合邏輯測試腳本（包含 setup/test/teardown；見 `tests/test_phase2.py`）
- [x] 測試 pages 處理順序（依 page_index；以 prompt 內 page_index 順序驗證）
- [x] 測試 per-page 輸入資料構建（每頁 embedded images 正確帶入；檢查 prompt 附帶 JSON）
- [x] 測試 appendMarkdown 串接結果順序（驗證輸出包含頁分隔 `---`）
- [x] 在 teardown 階段清理測試產生的檔案
- [x] 使用 `uv run pytest` 執行測試並通過（64 passed）

### 2.4 Markdown 輸出

- [x] 實作 Markdown 檔案寫入功能
  - [x] 寫入到 `outputDir/output_<timestamp>.md`（使用時間戳避免檔名衝突）
  - [x] 時間戳格式：YYYYMMDD_HHMMSS（例如：20250115_143022）
- [x] 實作完成訊息顯示（CLI）
  - [x] 顯示輸出路徑（output_<timestamp>.md、images/、logs/）
  - [x] 設定 exit code 0

#### 驗證項目
- [x] Markdown 檔案可正確寫入
- [x] 檔案內容格式正確（至少包含頁分隔 `---`，且為純 Markdown 文字）
- [ ] 圖片路徑正確（相對路徑或絕對路徑）
- [ ] 完成訊息清楚明確

#### 測試項目
- [x] 撰寫 Markdown 輸出測試腳本（包含 setup/test/teardown；見 `tests/test_phase2.py`）
- [x] 測試 Markdown 檔案寫入功能
- [x] 測試檔案內容格式正確性
- [ ] 測試圖片路徑正確性（相對路徑與絕對路徑）
- [x] 測試時間戳格式正確性（檔名 `output_<timestamp>.md`）
- [ ] 測試完成訊息顯示
- [x] 在 teardown 階段清理測試產生的 Markdown 檔案
- [x] 使用 `uv run pytest` 執行測試並通過（64 passed）

### 2.5 Phase 2 續跑/快取與 RECITATION 安全重試

- [x] per-page 輸出落地：`outputDir/phase2/pages/page_<page_index:04d>.md`
- [x] 狀態檔：`outputDir/phase2/state.json`（identity + completed_pages）
- [x] 續跑策略：若 per-page md 已存在，直接讀取並跳過 AI 呼叫（磁碟是事實來源）
- [x] RECITATION 處理：觸發 `RECITATION` 時改用「安全模式」提示詞重試一次
- [x] 並行處理機制
  - [x] 實作並行呼叫 Gemini（ThreadPoolExecutor）
  - [x] 從 `.env` 讀取 `GEMINI_CONCURRENCY`（預設 10）
  - [x] 確保 state.json 的更新是 thread-safe
  - [x] 確保 progress 顯示正確（因並行執行，需考慮進度條或 log 呈現）
  - [x] 最後依 page_index 順序合併所有 pageMd

#### 驗證項目
- [x] 第二次執行可命中快取、不重複呼叫 AI
- [x] prompt 變更不會自動重跑（仍以磁碟快取為準）
- [x] RECITATION 會切換安全模式並重試一次

#### 測試項目
- [x] 測試快取命中（第二次呼叫 AI 次數為 0）
- [x] 測試 prompt 變更仍可續跑（不因 identity 改變而丟棄磁碟快取）
- [x] 測試 RECITATION 觸發時的安全模式重試

### Phase 2 整體驗證

- [ ] 使用 Phase 1 產出的 parse_result_<timestamp>.json 執行 Phase 2
- [ ] 驗證所有中間產物檔案名稱使用時間戳，不會互相覆蓋
- [ ] 檢查 output.md 內容正確性
  - [ ] 圖片正確嵌入
  - [ ] Markdown 格式正確
- [ ] 驗證圖片檔案可正常顯示
- [ ] 驗證 `--from-parse` 參數可正常運作
- [ ] 驗證 `--prompt-file` 可用且修改 prompt 後可影響輸出

#### 測試項目
- [ ] 撰寫 Phase 2 整合測試腳本（包含 setup/test/teardown）
- [ ] 使用 Phase 1 產出的 parse_result.json 執行完整 Phase 2 流程
- [ ] 驗證所有中間產物檔案名稱使用時間戳
- [ ] 驗證 output.md 內容正確性（文字轉換、圖片嵌入、格式）
- [ ] 驗證圖片檔案可正常顯示
- [ ] 測試 `--from-parse` 參數的完整流程
- [ ] 測試 `--prompt-file` 覆寫提示詞
- [ ] 在 teardown 階段清理所有測試產物
- [ ] 使用 `uv run pytest` 執行測試並通過

## 日誌與錯誤處理

- [ ] 實作日誌功能
  - [ ] 寫入到 `outputDir/logs/`
  - [ ] 日誌檔案命名：`log_<timestamp>.log`（使用時間戳避免檔名衝突）
  - [ ] 時間戳格式：YYYYMMDD_HHMMSS（例如：20250115_143022）
  - [ ] 記錄各階段執行狀況
  - [ ] 記錄錯誤訊息
- [ ] 實作錯誤處理機制
  - [ ] PDF 開啟失敗處理
  - [ ] 圖片提取失敗處理
  - [ ] AI API 呼叫失敗處理
  - [ ] 檔案寫入失敗處理

### 驗證項目
- [ ] 日誌檔案可正常寫入
- [ ] 錯誤訊息清楚明確
- [ ] 錯誤處理機制正常運作

### 測試項目
- [ ] 撰寫日誌與錯誤處理測試腳本（包含 setup/test/teardown）
- [ ] 測試日誌檔案寫入功能
- [ ] 測試日誌檔案命名與時間戳格式
- [ ] 測試各階段執行狀況的記錄
- [ ] 測試錯誤訊息的記錄
- [ ] 測試 PDF 開啟失敗處理
- [ ] 測試圖片提取失敗處理
- [ ] 測試 AI API 呼叫失敗處理
- [ ] 測試檔案寫入失敗處理
- [ ] 在 teardown 階段清理測試產生的日誌檔案
- [ ] 使用 `uv run pytest` 執行測試並通過

## 整合測試

- [ ] 端對端測試（Phase 1 + Phase 2）
  - [ ] 使用測試資料完整執行流程
  - [ ] 驗證所有產出檔案正確
- [ ] 測試各種 PDF 格式
  - [ ] 純文字 PDF
  - [ ] 包含圖片的 PDF
  - [ ] 多頁 PDF
- [ ] 測試錯誤情況
  - [ ] 不存在的 PDF 檔案
  - [ ] 損壞的 PDF 檔案
  - [ ] API 金鑰錯誤
  - [ ] `--parse-only` 與 `--from-parse` 同時使用（應顯示錯誤）
  - [ ] parse_result.json schema_version 不相容（應顯示錯誤）

### 驗證項目
- [ ] 完整流程可正常執行
- [ ] 各種 PDF 格式可正確處理
- [ ] 錯誤情況可正確處理

### 測試項目
- [ ] 撰寫端對端測試腳本（包含 setup/test/teardown）
- [ ] 測試完整流程（Phase 1 + Phase 2）
- [ ] 使用測試資料執行完整流程並驗證所有產出檔案
- [ ] 測試各種 PDF 格式（純文字、包含圖片、多頁）
- [ ] 測試錯誤情況處理
  - [ ] 不存在的 PDF 檔案
  - [ ] 損壞的 PDF 檔案
  - [ ] API 金鑰錯誤
  - [ ] `--parse-only` 與 `--from-parse` 同時使用
  - [ ] parse_result.json schema_version 不相容
- [ ] 驗證錯誤訊息的準確性與可讀性
- [ ] 在 teardown 階段清理所有測試產物
- [ ] 使用 `uv run pytest` 執行所有測試並通過

## 文件與部署

- [ ] 撰寫 README.md
  - [ ] 安裝說明
  - [ ] 使用說明
  - [ ] 參數說明
  - [ ] 範例
- [ ] 撰寫開發文件
  - [ ] 專案結構說明
  - [ ] API 文件
- [ ] 準備部署相關文件
  - [ ] 環境變數設定說明
  - [ ] 依賴套件清單

### 驗證項目
- [ ] README.md 內容完整
- [ ] 文件可讓新開發者快速上手
- [ ] 部署文件清楚明確
