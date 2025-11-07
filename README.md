````markdown
# AI 規格產生器 - 從想法到規格的加速器

> **專案理念**：讓人們可以快速將原始想法轉化為完整規格書，在使用 AI Coding 時能依據規格書進行開發，減少幻覺、提升準確度。

## 💡 為什麼需要這個工具？

在 AI Coding 時代，最大的挑戰不是寫程式，而是**如何讓 AI 理解你的需求**。這個專案的目標是：

1. **加速規格產出流程** - 從模糊想法 → 清晰規格書，原本需要數小時，現在只需幾分鐘
2. **減少 AI 幻覺** - 有了結構化的規格書（DBML + Gherkin），AI 可以更精準地生成程式碼
3. **提升開發品質** - 規格先行，讓開發過程更可控、可測試、可維護

### 傳統流程 vs AI 加速流程

**傳統流程（耗時且容易出錯）：**
```
💭 想法 → 📝 手寫文件 → 🤔 多次修改 → 💻 開發 → 🐛 發現需求不清 → ♻️ 重新討論
```

**AI 加速流程（快速且精準）：**
```
💭 想法 → 🤖 AI 衍生詳細需求 → 📋 自動生成規格 → 🔍 AI 檢查遺漏 → ✅ 確認規格 → 💻 AI Coding
```

---

## 🚀 完整啟動指南

### 前置需求

- **Python 3.8+** 
- **macOS / Linux / Windows** 均支援
- **AI 服務**（二選一）：
  - OpenAI API Key（推薦，需付費）
  - Ollama 本地 LLM（免費，需安裝）

### 步驟 1：安裝 Python 虛擬環境

```bash
# 檢查 Python 版本（需 3.8+）
python3 --version

# 進入專案目錄
cd /Users/linjunting/Desktop/Django

# 如果沒有虛擬環境，先建立
python3 -m venv venv

# 啟動虛擬環境
source venv/bin/activate

# 確認虛擬環境已啟動（終端會顯示 (venv)）
```

### 步驟 2：安裝依賴套件

```bash
# 安裝 Django 核心
pip install Django==5.2.8
pip install python-dotenv==1.0.0

# 選擇你的 AI 服務
# 選項 A：OpenAI API（推薦）
pip install openai==1.3.0

# 選項 B：Ollama 本地 LLM（免費）
pip install ollama==0.1.0

# 完整安裝（所有功能）
pip install -r requirements.txt
```

### 步驟 3：設定環境變數

```bash
# 複製環境變數範本
cp .env.example .env

# 編輯 .env 檔案
nano .env
# 或使用你習慣的編輯器
open .env
```

**最小必要設定（.env 檔案內容）：**

```bash
# Django 設定
DJANGO_SECRET_KEY=your-random-secret-key-change-this
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1

# OpenAI API（如果使用 OpenAI）
OPENAI_API_KEY=sk-your-actual-openai-api-key-here
OPENAI_MODEL=gpt-4
OPENAI_TEMPERATURE=0.7

# Ollama（如果使用本地 LLM）
OLLAMA_API_URL=http://localhost:11434
OLLAMA_MODEL=llama2
```

**如何取得 OpenAI API Key：**
1. 訪問 https://platform.openai.com/api-keys
2. 登入或註冊帳號
3. 點擊「Create new secret key」
4. 複製 API Key 並貼到 `.env` 的 `OPENAI_API_KEY`

**如何使用 Ollama（免費選項）：**
```bash
# macOS 安裝
brew install ollama

# 啟動 Ollama 服務
ollama serve

# 在新終端視窗下載模型
ollama pull llama2
```

### 步驟 4：檢查環境設定

```bash
# 執行環境檢查腳本
python check_env.py

# 如果顯示 ✅ 代表設定正確
# 如果顯示 ❌ 請依照提示修正
```

### 步驟 5：初始化資料庫

```bash
# 進入 Django 專案目錄
cd mysite

# 執行資料庫遷移
python manage.py migrate

# 看到 "OK" 代表成功
```

### 步驟 6：啟動開發伺服器

```bash
# 啟動伺服器（預設 port 8000）
python manage.py runserver

# 或指定 IP 和 port（允許其他裝置存取）
python manage.py runserver 0.0.0.0:8000
```

### 步驟 7：開始使用

開啟瀏覽器訪問：
- **主要應用**：http://127.0.0.1:8000/polls/
- **管理後台**：http://127.0.0.1:8000/admin/（需先建立管理員帳號）

---

## 🐳 透過 Docker 啟動專案（推薦）

如果你已安裝 Docker Desktop，可以使用 Docker 快速啟動專案，無需手動設定 Python 環境。

### 為什麼選擇 Docker？

✅ **環境一致性** - 開發、測試、生產環境完全相同  
✅ **快速部署** - 一個指令啟動整個應用  
✅ **易於管理** - 不會影響你的本機 Python 環境  
✅ **跨平台** - macOS、Linux、Windows 都能用

### 前置需求：安裝 Docker Desktop

#### macOS 安裝
```bash
# 方法 1：使用 Homebrew（推薦）
brew install --cask docker

# 方法 2：手動下載
# 訪問 https://www.docker.com/products/docker-desktop
# 下載 Docker Desktop for Mac 並安裝
```

#### Windows 安裝
1. 訪問 https://www.docker.com/products/docker-desktop
2. 下載 Docker Desktop for Windows
3. 執行安裝程式並重啟電腦
4. 確保啟用 WSL 2（Windows Subsystem for Linux）

#### Linux 安裝
```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install docker.io docker-compose

# CentOS/RHEL
sudo yum install docker docker-compose
```

**安裝後驗證**：
```bash
docker --version
# 應輸出：Docker version 27.x.x 或更高版本
```

### Docker 啟動步驟（只需 3 步驟）

#### 步驟 1：設定環境變數
```bash
cd /Users/linjunting/Desktop/Django

# 複製環境變數範本
cp .env.example .env

# 編輯 .env 檔案，設定必要參數
nano .env
```

**必須設定的環境變數**：
```bash
DJANGO_SECRET_KEY=your-random-secret-key
OPENAI_API_KEY=sk-your-openai-api-key  # 或使用 Ollama
```

#### 步驟 2：將 Docker 加入 PATH（僅 macOS 需要，一次性設定）

如果你遇到 `docker: command not found` 錯誤，執行以下指令：

```bash
# 將以下內容加入你的 shell 設定檔
echo 'export PATH="/Applications/Docker.app/Contents/Resources/bin:$PATH"' >> ~/.zshrc

# 重新載入設定
source ~/.zshrc

# 驗證 Docker 可用
docker --version
```

#### 步驟 3：啟動 Docker 容器
```bash
# 建立 Docker 映像（第一次需要，約 1-2 分鐘）
docker compose build

# 啟動容器（背景模式）
docker compose up -d

# 查看容器狀態
docker compose ps
```

**預期輸出**：
```
NAME              STATUS          PORTS
django-spec-gen   Up 10 seconds   0.0.0.0:8000->8000/tcp
```

#### 步驟 4：訪問應用
開啟瀏覽器訪問：
- **主要應用**：http://localhost:8000/polls/
- **管理後台**：http://localhost:8000/admin/

### Docker 常用指令

```bash
# 查看容器日誌
docker compose logs -f web

# 停止容器（但不刪除）
docker compose stop

# 啟動已停止的容器
docker compose start

# 停止並刪除容器（資料庫不會遺失）
docker compose down

# 重新建置映像（修改 Dockerfile 後）
docker compose up -d --build

# 進入容器執行指令
docker compose exec web bash

# 執行 Django 管理指令
docker compose exec web python mysite/manage.py migrate
docker compose exec web python mysite/manage.py createsuperuser
```

### Docker 部署的優勢

| 功能 | 傳統方式 | Docker 方式 |
|------|---------|------------|
| 環境設定 | 需手動安裝 Python、依賴套件 | 一個指令完成 |
| 環境隔離 | 可能影響系統 Python | 完全隔離 |
| 版本管理 | 難以控制 | Docker 映像版本化 |
| 部署速度 | 需逐步設定 | 快速部署 |
| 跨平台 | 可能遇到相容性問題 | 完全一致 |

### 故障排除

#### 問題 1：Port 8000 已被佔用
```bash
# 查看佔用 8000 port 的程序
lsof -i :8000

# 停止該程序或修改 docker-compose.yml
# 將 "8000:8000" 改為 "8001:8000"
```

#### 問題 2：容器無法啟動
```bash
# 查看詳細日誌
docker compose logs web

# 檢查 .env 檔案是否存在
ls -la .env
```

#### 問題 3：修改程式碼後沒有更新
```bash
# Docker 預設不會自動同步程式碼
# 需要重新建置映像
docker compose up -d --build
```

#### 問題 4：資料庫檔案遺失
```bash
# 檢查 volume 掛載
docker compose config

# 確保 docker-compose.yml 中有：
# volumes:
#   - ./mysite/db.sqlite3:/app/mysite/db.sqlite3
```

---

## 🎯 核心功能與使用流程

### 三階段智能規格產出系統

#### 階段 1：AI 想法衍生 💡
**目的**：把模糊想法變成三個詳細方案

```
輸入：「我想做一個餐廳點餐系統」
↓ AI 處理
輸出：
  方案 A：傳統桌邊點餐系統
  方案 B：掃碼自助點餐系統
  方案 C：智能推薦點餐系統
```

**使用方式**：
1. 進入「AI 想法衍生」頁面
2. 輸入你的簡單想法（一句話即可）
3. AI 自動生成三個詳細方案
4. 選擇最適合的方案

#### 階段 2：規格生成器 📋
**目的**：將選定方案轉化為結構化規格

**自動生成欄位**：
- 📌 專案目標（Project Goal）
- ⚙️ 核心功能（Core Features）
- 🔧 技術限制（Technical Constraints）
- 👥 目標受眾（Target Audience）

**特色**：
- ✨ 一鍵並行生成所有欄位（效率提升 4 倍）
- 🎨 深紫-橙色漸層主題，視覺清晰
- 💾 即時儲存，隨時編輯

#### 階段 3：進階規格產出（三步驟） 🚀

**Step 1: Formulation（格式化）**
- 從原始規格文本萃取資料模型（DBML）
- 自動生成功能模型（Gherkin）
- 遵循「無腦補原則」：只萃取明確內容，不擅自假設

**Step 2: Discovery（發現問題）**
- AI 自動掃描規格，識別歧義與遺漏
- 產生釐清問題清單
- 檢查項目：必要資訊、一致性、完整性、可實作性

**Step 3: Clarify（釐清與修正）**
- 逐一回答釐清問題
- 即時更新 DBML 和 Gherkin 規格
- 追蹤進度（已完成 X / 總計 Y）
- 生成完整規格結果頁面

#### 最終輸出 📄

**完整規格結果包含**：
1. **背景說明** - Markdown 格式專案概述
2. **專案目標** - 清單式目標描述
3. **資料模型** - DBML 格式實體關係圖
4. **功能規格** - Gherkin 格式使用者故事
5. **流程圖** - Mermaid 圖表（自動渲染）
6. **API 規格** - RESTful API 設計文件


### 輔助功能

#### ⚖️ 權重配置管理
**用途**：設定 Ticket 優先級計算公式

**四個權重說明**：
- **A 權重**：影響範圍的重要性（影響多少用戶或系統）
- **B 權重**：緊急程度的重要性（多快需要處理）
- **C 權重**：技術複雜度的重要性（實作的難易度）
- **D 權重**：商業價值的重要性（對業務的貢獻）

**限制**：四個權重總和必須等於 1.0

**範例**：
```
方案 A（平衡型）：A=0.25, B=0.25, C=0.25, D=0.25
方案 B（緊急優先）：A=0.2, B=0.5, C=0.1, D=0.2
方案 C（價值導向）：A=0.2, B=0.1, C=0.2, D=0.5
```

---

## � 技術堆疊

### 後端
- **Django 5.2.8** - Web 框架
- **SQLite3** - 開發資料庫
- **Python 3.8+** - 程式語言

### AI 服務
- **OpenAI GPT-4** - 商用 AI 模型（推薦）
- **Ollama** - 本地 LLM（免費替代方案）
  - 支援模型：llama2, mistral, codellama 等

### 前端
- **HTML5 + CSS3** - 響應式介面
- **Vanilla JavaScript** - 無框架依賴
- **Mermaid.js** - 流程圖渲染
- **Marked.js** - Markdown 渲染

### 資料模型
- 11 個 Django Models
- 包含：User, Order, WeightConfiguration, ChatSession 等

---

## 📦 專案結構

```
Django/
├── README.md                   # 📘 本檔案（完整指南）
├── ENV_SETUP.md               # 🔑 環境變數設定教學
├── MANUAL.md                  # 📖 使用手冊與 API 文件
├── .env.example               # 📋 環境變數範本
├── requirements.txt           # 📦 Python 依賴清單
├── check_env.py              # ✅ 環境檢查腳本
├── venv/                     # 🐍 Python 虛擬環境
│
├── docs/                     # �📚 文件目錄
│   └── schedule-mustupdate/
│       ├── report/          # 📊 專案完成報告（11 份）
│       ├── plan/finish/     # ✅ 已完成任務（12 個）
│       └── todo/            # 📝 待辦事項
│
└── mysite/                   # 🎯 Django 專案主目錄
    ├── manage.py            # Django 管理腳本
    ├── db.sqlite3           # SQLite 資料庫
    │
    ├── mysite/              # 專案設定
    │   ├── settings.py      # Django 設定（已整合 .env）
    │   ├── urls.py          # 路由配置
    │   └── wsgi.py          # WSGI 入口
    │
    └── polls/               # 主要應用
        ├── models.py        # 11 個資料模型
        ├── views.py         # 50+ API 端點
        ├── urls.py          # 路由配置
        ├── api_utils.py     # AI API 工具函數
        ├── tests*.py        # 測試檔案（111 測試）
        │
        ├── templates/polls/ # HTML 模板
        │   └── index.html   # 主要介面（2000+ 行）
        │
        └── migrations/      # 資料庫遷移檔案
```

---

## 🧪 測試指南

### 執行所有測試

```bash
# 進入 Django 專案目錄
cd mysite

# 執行完整測試套件
python manage.py test polls

# 詳細模式（顯示每個測試）
python manage.py test polls -v 2

# 平行執行（加速）
python manage.py test polls --parallel
```

### 執行特定測試模組

```bash
# 測試使用者與訂單功能
python manage.py test polls.tests_user_order -v 2

# 測試 AI 生成功能
python manage.py test polls.tests_gpt_generate -v 2

# 測試語義相似度
python manage.py test polls.tests_sentence_similarity -v 2

# 測試進階規格產出
python manage.py test polls.tests_advanced_spec -v 2
```

### 測試統計

- **總測試數**：111 個
- **通過率**：100%
- **執行時間**：~3.8 秒（單執行緒）
- **測試覆蓋**：
  - ✅ 使用者 CRUD
  - ✅ 訂單管理
  - ✅ AI 文本生成
  - ✅ 語義相似度分析
  - ✅ 權重配置驗證
  - ✅ 進階規格產出三階段
  - ✅ API 端點響應

---

## 🌐 API 端點總覽

### 認證與使用者管理
```
POST   /polls/user/              建立使用者
GET    /polls/user/              列出所有使用者
GET    /polls/user/<id>/         取得使用者詳情
PUT    /polls/user/<id>/         更新使用者
DELETE /polls/user/<id>/         刪除使用者
```

### 訂單管理
```
POST   /polls/order/             建立訂單
GET    /polls/order/             列出所有訂單
GET    /polls/order/<id>/        取得訂單詳情
PUT    /polls/order/<id>/        更新訂單
DELETE /polls/order/<id>/        刪除訂單
```

### AI 規格生成（核心功能）
```
POST   /polls/llm-idea/          AI 想法衍生（產生 3 個方案）
POST   /polls/generate-field/    AI 欄位生成（單一欄位）
POST   /polls/formulation/       Formulation 階段
POST   /polls/discovery/         Discovery 階段
POST   /polls/clarify/           Clarify 階段
POST   /polls/generate_complete_result/  生成完整結果頁面
```

### 配置管理
```
GET/POST  /polls/weight-config/     權重配置
GET/POST  /polls/field-priority/    欄位優先級
GET/POST  /polls/gpt-prompt/        GPT Prompt 配置
GET/POST  /polls/sync-path/         路徑同步配置
```

**完整 API 文件請參閱**：[MANUAL.md](MANUAL.md#api-文件)

---

## 🛠️ 開發工具與技巧

### Django Shell（互動式測試）

```bash
# 啟動 Django Shell
python manage.py shell

# 測試 OpenAI 連線
from polls.api_utils import test_openai_connection
success, message = test_openai_connection()
print(message)

# 測試 Ollama 連線
from polls.api_utils import test_ollama_connection
success, message = test_ollama_connection()
print(message)

# 查詢資料
from polls.models import User
users = User.objects.all()
print(users)
```

### 資料庫管理

```bash
# 建立新的遷移檔案
python manage.py makemigrations

# 執行遷移
python manage.py migrate

# 查看遷移狀態
python manage.py showmigrations

# 重設資料庫（⚠️ 會刪除所有資料）
rm db.sqlite3
rm -r polls/migrations/0*.py
python manage.py makemigrations
python manage.py migrate
```

### 建立管理員帳號

```bash
# 建立超級使用者
python manage.py createsuperuser

# 輸入：
# - Username: admin
# - Email: admin@example.com
# - Password: (輸入兩次)

# 訪問 http://127.0.0.1:8000/admin/
```

### 查看專案設定

```bash
# 檢查環境變數載入狀態
python check_env.py

# 顯示 Django 設定
python manage.py diffsettings
```

---

## 🚨 常見問題與解決方案

### Q1: 執行 `python manage.py runserver` 時出現 ModuleNotFoundError？

**原因**：虛擬環境未啟動或依賴未安裝

**解決方案**：
```bash
# 啟動虛擬環境
source venv/bin/activate

# 重新安裝依賴
pip install Django==5.2.8 python-dotenv==1.0.0

# 如果還有問題，完整重裝
pip install -r requirements.txt
```

### Q2: OpenAI API 回傳 401 Unauthorized？

**原因**：API Key 錯誤或未設定

**解決方案**：
```bash
# 檢查 .env 檔案
cat .env | grep OPENAI_API_KEY

# 確認格式正確
OPENAI_API_KEY=sk-proj-xxxxxxxxxx  # ✅ 正確
OPENAI_API_KEY='sk-proj-xxx'      # ❌ 錯誤（不要加引號）

# 重新啟動伺服器使環境變數生效
python manage.py runserver
```

### Q3: 找不到 .env 檔案？

**原因**：未從範本建立

**解決方案**：
```bash
# 複製範本
cp .env.example .env

# 編輯檔案
nano .env

# 或使用圖形介面編輯
open .env
```

### Q4: Ollama 連線失敗？

**原因**：Ollama 服務未啟動

**解決方案**：
```bash
# 檢查 Ollama 是否安裝
ollama --version

# 如果未安裝（macOS）
brew install ollama

# 啟動 Ollama 服務
ollama serve

# 在新終端視窗下載模型
ollama pull llama2

# 測試連線
curl http://localhost:11434/api/generate -d '{
  "model": "llama2",
  "prompt": "Hello"
}'
```

### Q5: 資料庫遷移錯誤？

**原因**：遷移檔案衝突或不一致

**解決方案**：
```bash
# 方法 1：假遷移（如果已手動建立資料庫）
python manage.py migrate --fake

# 方法 2：完全重設（⚠️ 會刪除所有資料）
rm db.sqlite3
rm -r polls/migrations/0*.py
python manage.py makemigrations polls
python manage.py migrate
```

### Q6: 測試失敗？

**原因**：資料庫狀態不一致或依賴缺失

**解決方案**：
```bash
# 重新執行遷移
python manage.py migrate

# 清除測試資料庫
python manage.py flush --noinput

# 重新測試
python manage.py test polls -v 2
```

### Q7: AI 生成速度很慢？

**原因**：使用本地 Ollama 或網路延遲

**建議方案**：
1. **切換到 OpenAI API**（速度快但需付費）
2. **使用更小的 Ollama 模型**（如 llama2:7b）
3. **啟用快取機制**（避免重複生成）

### Q8: 前端頁面空白或樣式錯誤？

**原因**：靜態檔案未載入或瀏覽器快取

**解決方案**：
```bash
# 清除瀏覽器快取（Cmd+Shift+R 或 Ctrl+Shift+R）

# 檢查 Django 設定
python manage.py collectstatic --noinput

# 確認模板路徑
python manage.py check --deploy
```

---

## 📊 專案統計

### 程式碼規模
- **總行數**：~12,000+
- **Python 程式碼**：~4,000 行
- **前端程式碼**：~2,000 行（HTML + CSS + JS）
- **測試程式碼**：~1,500 行

### 功能統計
- **資料模型**：11 個（User, Order, WeightConfiguration 等）
- **API 端點**：50+ 個
- **測試案例**：111 個（100% 通過）
- **前端頁面**：5 個主要區塊
- **AI 提示詞**：15+ 個專業 prompts

### 文件統計
- **README**：本檔案（完整指南）
- **使用手冊**：MANUAL.md（API 文件）
- **環境設定**：ENV_SETUP.md（API Key 教學）
- **完成報告**：11 份階段性報告
- **待辦清單**：12 個已完成任務

---

## 🎯 使用情境範例

### 情境 1：快速驗證產品想法

```
1. 開啟「AI 想法衍生」
2. 輸入：「我想做一個線上課程平台」
3. AI 生成三個方案：
   - 方案 A：傳統錄播課程平台
   - 方案 B：互動直播教學平台
   - 方案 C：AI 個人化學習系統
4. 選擇最符合的方案
5. 一鍵生成完整規格書
6. 直接拿去給 AI Coding 工具使用
```

**時間**：5-10 分鐘  
**輸出**：完整 DBML + Gherkin + API 規格

### 情境 2：團隊協作規格討論

```
1. PM 輸入初步需求到「進階規格產出」
2. Formulation 自動萃取資料模型和功能
3. Discovery 發現 15 個需要釐清的問題
4. 團隊逐一回答問題
5. Clarify 即時更新規格
6. 下載最終規格文件（DBML + Gherkin）
7. 開發團隊依據規格進行開發
```

**時間**：30-60 分鐘  
**輸出**：經過團隊討論確認的完整規格

### 情境 3：重構舊專案文件

```
1. 將舊專案的 README 或需求文件貼入
2. Formulation 自動反推資料結構
3. Discovery 發現文件中的矛盾與遺漏
4. 補充缺失資訊
5. 產生標準化規格文件
6. 作為重構的參考基準
```

**時間**：20-40 分鐘  
**輸出**：標準化的 DBML + Gherkin 文件

---

## 🚀 下一步行動清單

### 立即開始（5 分鐘）
- [x] ✅ 閱讀本 README
- [ ] 🔧 設定環境變數（參考 [ENV_SETUP.md](ENV_SETUP.md)）
- [ ] ✅ 執行測試確認環境
- [ ] 🚀 啟動伺服器
- [ ] 🎨 訪問 http://127.0.0.1:8000/polls/

### 深入了解（30 分鐘）
- [ ] 📖 閱讀 [MANUAL.md](MANUAL.md) 使用手冊
- [ ] 🧪 試用「AI 想法衍生」功能
- [ ] 📋 試用「規格生成器」功能
- [ ] 🚀 試用「進階規格產出」完整流程

### 進階使用（1 小時）
- [ ] ⚖️ 設定自己的權重配置方案
- [ ] 🎯 調整 GPT Prompt 客製化輸出
- [ ] 🧪 執行完整測試套件
- [ ] 📚 查看專案完成報告

---

## 📞 更多資源

### 文件連結
- **[ENV_SETUP.md](ENV_SETUP.md)** - 環境變數完整設定指南
- **[MANUAL.md](MANUAL.md)** - 使用手冊與 API 文件
- **[PROJECT_COMPLETION_SUMMARY.md](docs/schedule-mustupdate/report/PROJECT_COMPLETION_SUMMARY.md)** - 專案完成總覽

### 外部資源
- **OpenAI API 文件**：https://platform.openai.com/docs
- **Ollama 文件**：https://ollama.ai/
- **Django 文件**：https://docs.djangoproject.com/
- **DBML 語法**：https://dbml.dbdiagram.io/docs/
- **Gherkin 語法**：https://cucumber.io/docs/gherkin/

---

## 📄 授權與貢獻

本專案為內部開發專案，版權所有。

---

**最後更新**：2025年11月7日  
**版本**：v2.0.0  
**狀態**：✅ 生產就緒  
**維護者**：專案團隊  

---

## 💬 結語

這個專案的核心理念是：**讓 AI 更懂你的需求**。

在 AI Coding 時代，寫程式已經不是最難的部分，最難的是如何清楚表達你的需求。這個工具就是要解決這個問題——快速將模糊想法轉化為結構化規格書，讓 AI 可以更精準地幫你實現需求。

希望這個工具能夠加速你的開發流程，減少溝通成本，提升產品品質！🚀

---

### 🔑 環境設定（必讀！）
- **[ENV_SETUP.md](ENV_SETUP.md)** - 環境變數完整設定指南
  - 如何取得 OpenAI API Key
  - 如何使用免費的 Ollama 本地 LLM
  - API Key 安全最佳實踐

### 📖 使用手冊
- **[MANUAL.md](MANUAL.md)** - 完整使用手冊
  - 功能使用指南
  - API 完整文件（50+ 端點）
  - 常見問題 FAQ
  - 開發工具說明

### 📊 專案報告
- **[PROJECT_COMPLETION_SUMMARY.md](docs/schedule-mustupdate/report/PROJECT_COMPLETION_SUMMARY.md)** - 專案完成總覽
  - 12 個階段完成狀態
  - 111 個測試案例（100% 通過）
  - 技術堆疊與架構說明

---

## 🎯 主要功能

### ✨ 核心功能
- 📝 **自動規格生成** - 根據專案需求自動生成規格文件
- 🤖 **AI 輔助** - 支援 OpenAI GPT-4 或本地 Ollama
- 🔍 **語義相似度分析** - 智能檢測重複需求
- ⚖️ **權重配置管理** - 視覺化權重編輯器
- 🎯 **欄位優先級配置** - 拖放式優先級管理
- 📊 **Ticket 評分系統** - 自動計算加權分數

### 🛠️ 管理功能
- 👤 **使用者管理** - 完整 CRUD + 密碼加密
- 📦 **訂單管理** - 訂單狀態追蹤
- 💬 **聊天會話管理** - AI 對話記錄
- 📤 **檔案上傳** - 支援 .xlsx 檔案
- 🔗 **路徑同步配置** - 雲端同步設定
- 🧠 **FAISS 向量索引** - 快速語義搜尋

---

## 🔧 技術堆疊

- **後端**: Django 5.2.8
- **資料庫**: SQLite3（開發）/ PostgreSQL（生產）
- **AI 服務**: OpenAI API / Ollama
- **語義分析**: Sentence Transformers
- **前端**: HTML5 + CSS3 + JavaScript（Vanilla）
- **測試**: Django TestCase（111 測試，100% 通過）

---

## 📦 專案結構

```
Django/
├── .env                        # 環境變數（需自行建立）
├── .env.example                # 環境變數範例
├── .gitignore                  # Git 忽略檔案
├── requirements.txt            # Python 依賴
├── check_env.py               # 環境檢查腳本
├── ENV_SETUP.md               # 環境設定指南 ⭐
├── MANUAL.md                  # 使用手冊 ⭐
├── venv/                      # 虛擬環境
├── docs/                      # 文件目錄
│   └── schedule-mustupdate/
│       ├── report/           # 完成報告（11 份）
│       └── plan/
│           └── finish/       # 已完成任務（12 個）
└── mysite/                    # Django 專案
    ├── manage.py
    ├── db.sqlite3            # SQLite 資料庫
    ├── mysite/               # 專案設定
    │   └── settings.py       # 已整合環境變數
    └── polls/                # 主要應用
        ├── models.py         # 11 個資料模型
        ├── views.py          # 50+ API 端點
        ├── urls.py           # 路由配置
        ├── api_utils.py      # API 工具函數 ⭐
        ├── tests*.py         # 測試檔案（111 測試）
        └── templates/        # HTML 模板
```

---

## 🧪 測試

```bash
# 執行所有測試
cd mysite
python manage.py test polls

# 執行特定測試
python manage.py test polls.tests_user_order -v 2
python manage.py test polls.tests_gpt_generate -v 2
python manage.py test polls.tests_sentence_similarity -v 2

# 平行測試（加速）
python manage.py test polls --parallel
```

**測試統計**：
- 總測試數：111
- 通過率：100%
- 執行時間：~3.8 秒

---

## 🌐 API 端點概覽

### 認證與使用者
- `POST /polls/user/` - 建立使用者
- `GET /polls/user/` - 列出所有使用者
- `GET /polls/user/<id>/` - 取得使用者詳情
- `PUT /polls/user/<id>/` - 更新使用者
- `DELETE /polls/user/<id>/` - 刪除使用者

### AI 服務
- `POST /polls/generate-specification/` - 生成規格文件
- `POST /polls/retry-ai/` - 重試 AI 生成
- `POST /polls/sentence-similarity/` - 語義相似度分析
- `POST /polls/gpt-generate/` - GPT 文本生成

### 配置管理
- `GET/POST /polls/weight-config/` - 權重配置
- `GET/POST /polls/field-priority/` - 欄位優先級
- `GET/POST /polls/gpt-prompt/` - GPT Prompt 配置

**完整 API 文件**：請參閱 [MANUAL.md](MANUAL.md#api-文件)

---

## 🔑 API Key 設定

### 選項 1：OpenAI API（推薦）

1. 取得 API Key：https://platform.openai.com/api-keys
2. 編輯 `.env` 檔案：
   ```bash
   OPENAI_API_KEY=sk-your-actual-openai-api-key-here
   OPENAI_MODEL=gpt-4
   ```
3. 安裝套件：
   ```bash
   pip install openai
   ```

### 選項 2：Ollama 本地 LLM（免費）

1. 安裝 Ollama：
   ```bash
   brew install ollama  # macOS
   ```
2. 下載模型並啟動：
   ```bash
   ollama pull llama2
   ollama serve
   ```
3. 編輯 `.env` 檔案：
   ```bash
   OLLAMA_API_URL=http://localhost:11434
   OLLAMA_MODEL=llama2
   ```

**詳細設定**：請參閱 [ENV_SETUP.md](ENV_SETUP.md)

---

## 📝 環境變數範例

```bash
# Django 設定
DJANGO_SECRET_KEY=your-secret-key
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1

# OpenAI API
OPENAI_API_KEY=sk-your-key-here
OPENAI_MODEL=gpt-4
OPENAI_TEMPERATURE=0.7

# Ollama（可選）
OLLAMA_API_URL=http://localhost:11434
OLLAMA_MODEL=llama2

# Sentence Transformers
SENTENCE_TRANSFORMER_MODEL=paraphrase-MiniLM-L6-v2
```

完整設定請參考 [.env.example](.env.example)

---

## 🎨 前端頁面

### 主頁面
http://127.0.0.1:8000/polls/
- 規格生成表單
- 即時驗證
- 載入動畫
- 重試功能

### 權重配置管理
http://127.0.0.1:8000/polls/weight-config-page/
- 視覺化權重編輯
- 總和驗證（100%）
- Ticket 評分計算器

### 欄位優先級配置
http://127.0.0.1:8000/polls/field-priority-page/
- 視覺化 / JSON 雙模式
- 拖放排序
- 必填/選填標籤

### Admin 管理介面
http://127.0.0.1:8000/admin/
- 管理所有資料模型
- 需要超級使用者帳號

---

## 🛠️ 開發工具

### Django Shell
```bash
python manage.py shell

# 測試 API
from polls.api_utils import test_openai_connection
success, message = test_openai_connection()
print(message)
```

### 環境檢查
```bash
python check_env.py
```

### 資料庫管理
```bash
# 建立遷移
python manage.py makemigrations

# 執行遷移
python manage.py migrate

# 建立超級使用者
python manage.py createsuperuser
```

---

## 🚨 常見問題

### Q: 執行測試時出現錯誤？
```bash
# 確認虛擬環境已啟動
source venv/bin/activate

# 重新安裝依賴
pip install -r requirements.txt

# 執行遷移
python manage.py migrate

# 再次測試
python manage.py test polls
```

### Q: OpenAI API 回傳 401 錯誤？
檢查 `.env` 中的 `OPENAI_API_KEY` 是否正確設定。

### Q: 找不到 .env 檔案？
```bash
cp .env.example .env
open .env  # 編輯並填入 API Key
```

### Q: 如何重設資料庫？
```bash
rm db.sqlite3
rm -r polls/migrations/0*.py
python manage.py makemigrations
python manage.py migrate
```

**更多問題**：請參閱 [MANUAL.md](MANUAL.md#常見問題)

---

## 📊 專案統計

- **程式碼行數**: ~10,000+
- **資料模型**: 11 個
- **API 端點**: 50+
- **測試案例**: 111 個（100% 通過）
- **前端頁面**: 3 個
- **完成報告**: 11 份
- **開發時間**: Phase 1 完整執行

---

## 🎯 下一步

1. ✅ **設定環境變數** - 參考 [ENV_SETUP.md](ENV_SETUP.md)
2. ✅ **執行測試** - `python manage.py test polls`
3. ✅ **啟動伺服器** - `python manage.py runserver`
4. ✅ **瀏覽文件** - 閱讀 [MANUAL.md](MANUAL.md)
5. 🚀 **開始使用** - 訪問 http://127.0.0.1:8000/polls/

---

## 📄 授權

本專案為內部開發專案。

---

## 📞 聯絡資訊

如有任何問題，請參考：
- [使用手冊](MANUAL.md)
- [環境設定指南](ENV_SETUP.md)
- [專案完成總覽](docs/schedule-mustupdate/report/PROJECT_COMPLETION_SUMMARY.md)

---

**最後更新**: 2025年11月7日  
**版本**: v1.0.0  
**狀態**: ✅ 生產就緒（需設定 API Key）
