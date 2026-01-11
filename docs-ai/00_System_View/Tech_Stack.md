# Tech Stack

技術棧文件描述系統所使用的技術選型與工具。

## 技術選型原則

-   **成熟穩定**: 選擇社群活躍且經過驗證的 Python 套件。
-   **開發效率**: 使用現代化工具 (如 `uv`) 簡化依賴管理與環境設置。
-   **AI 驅動**: 核心功能依賴 Google Gemini API 進行智慧處理。
-   **模組化**: 保持核心邏輯與 CLI 介面分離，便於未來擴展。

## 技術分類

### 核心語言與環境

-   **程式語言**: Python >= 3.14.0
-   **套件管理**: [uv](https://github.com/astral-sh/uv) - 高效的 Python 專案管理工具。
-   **建置系統**: hatchling - 用於構建 Python 套件。

### 核心依賴

-   **PDF 處理**: [PyMuPDF](https://github.com/pymupdf/PyMuPDF) (pymupdf>=1.24.0) - 高效能 PDF 解析與圖片提取。
-   **AI 模型**: [Google Generative AI SDK](https://github.com/google/generative-ai-python) (google-genai>=1.56.0) - 用於與 Gemini 模型互動。
-   **環境配置**: [python-dotenv](https://github.com/theskumar/python-dotenv) (python-dotenv>=1.0.0) - 管理環境變數與密鑰。

### 開發與測試工具

-   **測試框架**: [pytest](https://docs.pytest.org/) (pytest>=8.0.0) - 單元測試與整合測試。
-   **程式碼品質**: [pylint](https://pylint.readthedocs.io/) (pylint>=4.0.4) - 靜態程式碼分析。

## 版本管理

技術選型應明確記錄版本號，並說明選擇該版本的原因。詳細版本鎖定請參考 `uv.lock` 文件。

## 相關文件

-   系統導覽: `00_AI_READ_FIRST.md`
-   架構設計: `Architecture.puml` (待建立)
-   部署配置: `Deployment.puml` (待建立)
-   技術決策記錄: `05_Principles/ADR/` 目錄下的 ADR 文件
