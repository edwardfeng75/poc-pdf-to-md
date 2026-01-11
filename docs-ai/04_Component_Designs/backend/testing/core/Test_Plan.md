# 測試案例決策表

本文件列出所有測試案例及其對應的代碼位置，用於快速查找和追蹤測試覆蓋範圍。

## 測試模組總覽

| 模組 | 測試檔案 | 測試類別數 | 測試方法數 |
|------|---------|-----------|-----------|
| CLI | `tests/test_cli.py` | 3 | 11 |
| Engine | `tests/test_engine.py` | 1 | 8 |
| Image Handler | `tests/test_image_handler.py` | 3 | 9 |
| Parse Result | `tests/test_parse_result.py` | 5 | 16 |
| PDF Parser | `tests/test_pdf_parser.py` | 3 | 9 |
| PDF Parser Fontsize | `tests/test_pdf_parser_fontsize.py` | 1 | 4 |
| Phase 2 | `tests/test_phase2.py` | 1 | 7 |
| **總計** | **7** | **17** | **64** |

---

## 1. CLI 模組測試 (`tests/test_cli.py`)

### 1.1 TestCLIParseArgs - CLI 參數解析測試

| 測試方法 | 描述 | 代碼位置 | 測試情境 |
|---------|------|---------|---------|
| `test_parse_args_with_valid_input` | 測試解析有效的輸入參數 | `34:49:tests/test_cli.py` | 提供有效的 input 和 output 參數 |
| `test_parse_args_with_parse_only` | 測試解析 `--parse-only` 標記 | `50:62:tests/test_cli.py` | 使用 `--parse-only` 參數 |
| `test_parse_args_with_from_parse` | 測試解析 `--from-parse` 參數 | `63:76:tests/test_cli.py` | 使用 `--from-parse` 參數 |
| `test_parse_args_mutual_exclusivity_error` | 測試 `--parse-only` 和 `--from-parse` 互斥錯誤 | `77:92:tests/test_cli.py` | 同時使用兩個互斥參數 |
| `test_parse_args_nonexistent_pdf_error` | 測試不存在的 PDF 檔案錯誤 | `93:105:tests/test_cli.py` | 提供不存在的 PDF 檔案路徑 |
| `test_parse_args_nonexistent_parse_file_error` | 測試不存在的解析結果檔案錯誤 | `106:118:tests/test_cli.py` | 提供不存在的 JSON 檔案路徑 |

### 1.2 TestGetModelName - 模型名稱解析測試

| 測試方法 | 描述 | 代碼位置 | 測試情境 |
|---------|------|---------|---------|
| `test_get_model_name_from_cli_arg` | 測試從 CLI 參數取得模型名稱 | `134:139:tests/test_cli.py` | 透過 CLI 參數指定模型名稱 |
| `test_get_model_name_from_env` | 測試從環境變數取得模型名稱 | `140:146:tests/test_cli.py` | 透過環境變數 `GEMINI_MODEL` 指定 |
| `test_get_model_name_default` | 測試預設模型名稱 | `147:153:tests/test_cli.py` | 未指定模型名稱時使用預設值 |

### 1.3 TestPrintFunctions - 打印函數測試

| 測試方法 | 描述 | 代碼位置 | 測試情境 |
|---------|------|---------|---------|
| `test_print_parse_output_path` | 測試打印解析輸出路徑 | `167:173:tests/test_cli.py` | 驗證輸出訊息格式 |
| `test_print_success_message` | 測試打印成功訊息 | `174:181:tests/test_cli.py` | 驗證成功訊息包含所有必要資訊 |

---

## 2. Engine 模組測試 (`tests/test_engine.py`)

### 2.1 TestPhase1ParsePDF - Phase 1 PDF 解析整合測試

| 測試方法 | 描述 | 代碼位置 | 測試情境 |
|---------|------|---------|---------|
| `test_phase1_parse_pdf_success` | 測試成功的 Phase 1 解析 | `28:33:tests/test_engine.py` | 驗證解析成功並產生 JSON 檔案 |
| `test_phase1_parse_pdf_creates_directories` | 測試建立必要的目錄 | `34:39:tests/test_engine.py` | 驗證 `parsed` 和 `images` 目錄被建立 |
| `test_phase1_parse_pdf_generates_json` | 測試產生 JSON 檔案 | `40:50:tests/test_engine.py` | 驗證 JSON 檔案包含必要的欄位 |
| `test_phase1_parse_pdf_extracts_images` | 測試提取圖片 | `51:63:tests/test_engine.py` | 驗證圖片檔案被提取到 images 目錄 |
| `test_phase1_parse_pdf_image_paths_in_json` | 測試 JSON 中記錄圖片路徑 | `64:91:tests/test_engine.py` | 驗證圖片區塊包含路徑和尺寸資訊 |
| `test_phase1_parse_pdf_block_index_order` | 測試 blockIndex 順序正確 | `92:99:tests/test_engine.py` | 驗證 blockIndex 是連續的 |
| `test_phase1_parse_pdf_timestamp_filename` | 測試檔名使用時間戳格式 | `100:109:tests/test_engine.py` | 驗證檔名格式為 `parse_result_YYYYMMDD_HHMMSS.json` |
| `test_phase1_parse_pdf_nonexistent_file` | 測試不存在的 PDF 檔案錯誤 | `110:113:tests/test_engine.py` | 提供不存在的 PDF 檔案路徑 |

---

## 3. Image Handler 模組測試 (`tests/test_image_handler.py`)

### 3.1 TestGenerateImageFilename - 圖片檔名生成測試

| 測試方法 | 描述 | 代碼位置 | 測試情境 |
|---------|------|---------|---------|
| `test_generate_image_filename_format` | 測試生成的檔名格式正確 | `27:35:tests/test_image_handler.py` | 驗證檔名以正確副檔名結尾且包含 UUID |
| `test_generate_image_filename_unique` | 測試生成的檔名唯一 | `36:40:tests/test_image_handler.py` | 驗證多次生成不會重複 |
| `test_generate_image_filename_different_extensions` | 測試不同副檔名的檔名生成 | `41:47:tests/test_image_handler.py` | 驗證 PNG 和 JPG 副檔名正確 |

### 3.2 TestSaveImage - 圖片保存功能測試

| 測試方法 | 描述 | 代碼位置 | 測試情境 |
|---------|------|---------|---------|
| `test_save_image_creates_directory` | 測試建立圖片目錄 | `63:69:tests/test_image_handler.py` | 驗證 `images` 目錄被建立 |
| `test_save_image_writes_file` | 測試正確寫入圖片檔案 | `70:77:tests/test_image_handler.py` | 驗證檔案內容正確 |
| `test_save_image_returns_relative_path` | 測試返回相對路徑 | `78:84:tests/test_image_handler.py` | 驗證返回的路徑是相對路徑且以 `images/` 開頭 |

### 3.3 TestUpdateParseResultImagePath - 解析結果圖片路徑更新測試

| 測試方法 | 描述 | 代碼位置 | 測試情境 |
|---------|------|---------|---------|
| `test_update_parse_result_image_path_success` | 測試成功更新圖片路徑 | `103:108:tests/test_image_handler.py` | 更新圖片區塊的路徑 |
| `test_update_parse_result_image_path_text_block` | 測試文字區塊不被更新 | `109:116:tests/test_image_handler.py` | 驗證文字區塊不受影響 |
| `test_update_parse_result_image_path_nonexistent_block` | 測試更新不存在的區塊索引 | `117:122:tests/test_image_handler.py` | 使用不存在的 blockIndex 不應出錯 |

---

## 4. Parse Result 模組測試 (`tests/test_parse_result.py`)

### 4.1 TestCreateParseResult - 解析結果創建測試

| 測試方法 | 描述 | 代碼位置 | 測試情境 |
|---------|------|---------|---------|
| `test_create_parse_result_structure` | 測試解析結果結構正確 | `33:41:tests/test_parse_result.py` | 驗證包含所有必要欄位 |
| `test_create_parse_result_values` | 測試解析結果數值正確 | `42:48:tests/test_parse_result.py` | 驗證欄位值正確 |
| `test_create_parse_result_created_at_format` | 測試 `created_at` 為 ISO 8601 格式 | `50:57:tests/test_parse_result.py` | 驗證時間戳格式正確 |

### 4.2 TestSaveParseResult - 解析結果保存測試

| 測試方法 | 描述 | 代碼位置 | 測試情境 |
|---------|------|---------|---------|
| `test_save_parse_result_creates_directory` | 測試建立 parsed 目錄 | `79:84:tests/test_parse_result.py` | 驗證 `parsed` 目錄被建立 |
| `test_save_parse_result_filename_format` | 測試檔名格式正確 | `85:96:tests/test_parse_result.py` | 驗證檔名使用時間戳格式 |
| `test_save_parse_result_content` | 測試保存內容正確 | `97:101:tests/test_parse_result.py` | 驗證保存的 JSON 內容正確 |

### 4.3 TestLoadParseResult - 解析結果載入測試

| 測試方法 | 描述 | 代碼位置 | 測試情境 |
|---------|------|---------|---------|
| `test_load_parse_result_success` | 測試成功載入解析結果 | `126:130:tests/test_parse_result.py` | 驗證載入的內容正確 |
| `test_load_parse_result_nonexistent_file` | 測試不存在的檔案錯誤 | `131:135:tests/test_parse_result.py` | 提供不存在的檔案路徑 |
| `test_load_parse_result_invalid_json` | 測試無效的 JSON 錯誤 | `136:142:tests/test_parse_result.py` | 提供無效的 JSON 內容 |

### 4.4 TestValidateSchemaVersion - Schema 版本驗證測試

| 測試方法 | 描述 | 代碼位置 | 測試情境 |
|---------|------|---------|---------|
| `test_validate_schema_version_valid` | 測試有效的 schema 版本 | `155:159:tests/test_parse_result.py` | 驗證版本 "1.0" 通過驗證 |
| `test_validate_schema_version_invalid` | 測試無效的 schema 版本 | `160:164:tests/test_parse_result.py` | 驗證版本 "2.0" 不通過驗證 |
| `test_validate_schema_version_missing` | 測試缺少 schema 版本 | `165:168:tests/test_parse_result.py` | 驗證缺少版本欄位不通過驗證 |

### 4.5 TestValidateBlockIndexOrder - Block Index 順序驗證測試

| 測試方法 | 描述 | 代碼位置 | 測試情境 |
|---------|------|---------|---------|
| `test_validate_block_index_order_valid` | 測試有效的 block index 順序 | `182:192:tests/test_parse_result.py` | 驗證連續的 blockIndex 通過驗證 |
| `test_validate_block_index_order_invalid` | 測試無效的 block index 順序 | `193:203:tests/test_parse_result.py` | 驗證不連續的 blockIndex 不通過驗證 |
| `test_validate_block_index_order_empty` | 測試空的 blocks | `204:208:tests/test_parse_result.py` | 驗證空的 blocks 陣列通過驗證 |
| `test_validate_block_index_order_missing_blocks` | 測試缺少 blocks 鍵 | `209:212:tests/test_parse_result.py` | 驗證缺少 blocks 鍵通過驗證 |

---

## 5. PDF Parser 模組測試 (`tests/test_pdf_parser.py`)

### 5.1 TestOpenPDF - PDF 開啟功能測試

| 測試方法 | 描述 | 代碼位置 | 測試情境 |
|---------|------|---------|---------|
| `test_open_pdf_success` | 測試成功開啟 PDF 檔案 | `24:30:tests/test_pdf_parser.py` | 驗證返回 fitz.Document 物件 |
| `test_open_pdf_nonexistent_file` | 測試不存在的 PDF 檔案錯誤 | `31:34:tests/test_pdf_parser.py` | 提供不存在的檔案路徑 |

### 5.2 TestParsePDF - PDF 解析功能測試

| 測試方法 | 描述 | 代碼位置 | 測試情境 |
|---------|------|---------|---------|
| `test_parse_pdf_returns_blocks` | 測試返回 blocks | `53:58:tests/test_pdf_parser.py` | 驗證返回非空的 blocks 列表 |
| `test_parse_pdf_block_structure` | 測試 blocks 結構正確 | `59:69:tests/test_pdf_parser.py` | 驗證每個 block 包含必要欄位 |
| `test_parse_pdf_block_index_order` | 測試 blockIndex 是連續的 | `70:75:tests/test_pdf_parser.py` | 驗證 blockIndex 從 0 開始連續 |
| `test_parse_pdf_sorting_by_page_index` | 測試按 page_index 排序 | `76:83:tests/test_pdf_parser.py` | 驗證 blocks 按頁面索引排序 |
| `test_parse_pdf_sorting_by_bbox` | 測試同一頁面內按 bbox 排序 | `84:105:tests/test_pdf_parser.py` | 驗證同一頁面的 blocks 按 Y 座標排序 |

### 5.3 TestExtractImage - 圖片提取功能測試

| 測試方法 | 描述 | 代碼位置 | 測試情境 |
|---------|------|---------|---------|
| `test_extract_image_success` | 測試成功提取圖片 | `123:141:tests/test_pdf_parser.py` | 驗證返回圖片位元組和元資料 |
| `test_extract_image_invalid_xref` | 測試無效的 xref 錯誤 | `142:145:tests/test_pdf_parser.py` | 提供無效的 xref 值 |

---

## 6. PDF Parser Fontsize 模組測試 (`tests/test_pdf_parser_fontsize.py`)

### 6.1 TestFontSizeExtraction - 字型大小（已停用，保留作為參考）測試

| 測試方法 | 描述 | 代碼位置 | 測試情境 |
|---------|------|---------|---------|
| `test_font_size_extraction` | 驗證目前不再處理文字區塊（僅回傳嵌入圖片 blocks） | `24:33:tests/test_pdf_parser_fontsize.py` | 確認所有 blocks 都是 image 且含 xref |
| `test_font_size_format` | 字型大小格式檢查（文字區塊目前不適用） | `34:46:tests/test_pdf_parser_fontsize.py` | 若存在 fontSize 欄位則需為正數數值 |
| `test_font_size_min_max` | min/max 邏輯檢查（文字區塊目前不適用） | `47:62:tests/test_pdf_parser_fontsize.py` | 若存在 fontSizeMax 則需有 fontSizeMin，且 max>=min |
| `test_font_size_average_calculation` | 平均值邏輯檢查（文字區塊目前不適用） | `63:75:tests/test_pdf_parser_fontsize.py` | 若同時有 min/max，平均需落在區間內 |

---

## 7. Phase 2 模組測試 (`tests/test_phase2.py`)

### 7.1 TestPhase2ConvertToMarkdown - parse_result → Markdown（含續跑快取）測試

| 測試方法 | 描述 | 代碼位置 | 測試情境 |
|---------|------|---------|---------|
| `test_phase2_generates_output_markdown_and_calls_ai_per_page` | 每頁呼叫 AI、產出 output_*.md，並寫入 per-page 快取與 state | `101:143:tests/test_phase2.py` | 2 頁 parse_result，mock AI，確認 prompt 附帶 JSON 與分頁輸出存在 |
| `test_phase2_missing_prompt_file_raises` | prompt 檔案不存在應拋錯 | `144:152:tests/test_phase2.py` | 指定不存在的 prompt 檔案 |
| `test_phase2_empty_prompt_file_raises` | prompt 檔案為空應拋錯 | `153:163:tests/test_phase2.py` | 指定空內容 prompt 檔案 |
| `test_phase2_ai_error_includes_page_context` | AI 回應錯誤應包含頁面上下文資訊 | `164:184:tests/test_phase2.py` | mock AI 丟錯，驗證錯誤訊息含 page/page_index/image/model |
| `test_phase2_resume_skips_completed_pages` | 第二次執行應命中快取、不再呼叫 AI | `185:209:tests/test_phase2.py` | 先跑一次建立 per-page md，再跑一次確認 call_count=0 |
| `test_phase2_resume_survives_prompt_change_via_disk_cache` | prompt 變更後仍以磁碟快取為準（跳過 AI） | `210:236:tests/test_phase2.py` | 改 prompt 內容，確認仍不呼叫 AI |
| `test_phase2_recitation_retries_with_safe_prompt` | 觸發 RECITATION 時應切換安全模式重試 | `237:274:tests/test_phase2.py` | 第一次丟 RECITATION，第二次成功，確認 prompt 含「安全模式」 |

---

## 測試覆蓋範圍統計

### 按功能分類

| 功能類別 | 測試類別數 | 測試方法數 |
|---------|-----------|-----------|
| 參數解析與驗證 | 1 | 6 |
| 模型名稱解析 | 1 | 3 |
| 輸出訊息 | 1 | 2 |
| PDF 解析整合 | 1 | 8 |
| 圖片檔名生成 | 1 | 3 |
| 圖片保存 | 1 | 3 |
| 圖片路徑更新 | 1 | 3 |
| 解析結果創建 | 1 | 3 |
| 解析結果保存 | 1 | 3 |
| 解析結果載入 | 1 | 3 |
| Schema 驗證 | 1 | 3 |
| Block Index 驗證 | 1 | 4 |
| PDF 開啟 | 1 | 2 |
| PDF 解析 | 1 | 5 |
| 圖片提取 | 1 | 2 |
| 字型大小（已停用） | 1 | 4 |
| Phase 2（分頁轉換/續跑快取/RECITATION） | 1 | 7 |

### 按測試類型分類

| 測試類型 | 測試方法數 | 說明 |
|---------|-----------|------|
| 成功案例 | 43 | 正常流程與主要功能驗證（含 Phase 2 轉換與續跑快取） |
| 錯誤處理 | 11 | 異常情況測試（例如檔案不存在、無效 xref、無效 JSON、AI 回應錯誤） |
| 邊界條件 | 10 | 空值、缺失值、保留測試（例如文字區塊已移除） |

---

## 使用說明

1. **查找測試案例**：使用表格中的「代碼位置」欄位快速定位到具體的測試方法
2. **理解測試目的**：參考「描述」和「測試情境」欄位了解每個測試的目標
3. **追蹤測試覆蓋**：使用統計表格了解各模組的測試覆蓋情況
4. **新增測試**：參考現有測試結構和命名規範新增測試案例

---

## 更新記錄

- 2025-01-XX: 初始版本
- 2026-01-02: 同步最新 tests（新增 `test_pdf_parser_fontsize.py`，並更新各模組方法數與 line range）
- 2026-01-03: 新增 Phase 2 測試（`tests/test_phase2.py`），並更新總計與各表格統計
