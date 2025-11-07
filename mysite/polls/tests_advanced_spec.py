"""
進階規格產出功能測試
測試 Formulation API 和 Discovery API
"""
import json
from django.test import TestCase, Client
from django.urls import reverse
from unittest.mock import patch, MagicMock


class FormulationAPITest(TestCase):
    """測試 Formulation API"""
    
    def setUp(self):
        self.client = Client()
        self.url = '/polls/formulation/'
        self.test_spec = """
我想做一個餐廳點餐系統。
客人可以瀏覽菜單、將菜品加入訂單。
每道菜品都有名稱、價格、類別。
訂單必須記錄客人資訊、訂購時間、總額。
"""
    
    @patch('polls.api_utils.call_ollama_api')
    def test_formulation_success(self, mock_ollama):
        """測試成功的 Formulation 請求"""
        # Mock Ollama API 返回
        mock_ollama.side_effect = [
            # DBML 返回
            """Table MenuItem {
  id int [pk]
  name string [note: "菜品名稱"]
  price float [note: "價格，必須 >= 0"]
  category string [note: "類別"]
  
  Note: "菜單項目實體"
}

Table Order {
  id int [pk]
  customer_name string [note: "客人姓名"]
  order_time string [note: "訂購時間"]
  total float [note: "訂單總額，必須 >= 0"]
  
  Note: "訂單實體"
}""",
            # Gherkin 返回
            """Feature: 瀏覽菜單

  Rule: 客人可以查看所有菜品
    Example: 成功瀏覽菜單
      Given 系統中存在菜品
      When 客人開啟菜單頁面
      Then 系統顯示所有菜品列表

Feature: 將菜品加入訂單

  Rule: 客人可以選擇菜品並加入訂單
    Example: 成功加入菜品
      Given 菜品「宮保雞丁」存在於菜單中
      When 客人將「宮保雞丁」加入訂單
      Then 訂單中包含「宮保雞丁」"""
        ]
        
        # 發送請求
        response = self.client.post(
            self.url,
            data=json.dumps({'spec_text': self.test_spec}),
            content_type='application/json'
        )
        
        # 驗證回應
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertTrue(data['success'])
        self.assertIn('Table MenuItem', data['dbml'])
        self.assertIn('Table Order', data['dbml'])
        self.assertIn('Feature: 瀏覽菜單', data['gherkin'])
        self.assertIn('Feature: 將菜品加入訂單', data['gherkin'])
        
    def test_formulation_missing_spec_text(self):
        """測試缺少 spec_text 參數"""
        response = self.client.post(
            self.url,
            data=json.dumps({}),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.content)
        self.assertIn('error', data)
        
    def test_formulation_invalid_json(self):
        """測試無效的 JSON"""
        response = self.client.post(
            self.url,
            data='invalid json',
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.content)
        self.assertIn('error', data)
        
    def test_formulation_method_not_allowed(self):
        """測試不允許的 HTTP 方法"""
        response = self.client.get(self.url)
        
        self.assertEqual(response.status_code, 405)
        
    @patch('polls.api_utils.call_ollama_api')
    def test_formulation_removes_code_blocks(self, mock_ollama):
        """測試自動移除 markdown code block 標記"""
        # Mock 返回包含 code block 標記的內容
        mock_ollama.side_effect = [
            """```dbml
Table Test {
  id int
}
```""",
            """```gherkin
Feature: Test
```"""
        ]
        
        response = self.client.post(
            self.url,
            data=json.dumps({'spec_text': self.test_spec}),
            content_type='application/json'
        )
        
        data = json.loads(response.content)
        # 驗證 code block 標記已移除
        self.assertNotIn('```dbml', data['dbml'])
        self.assertNotIn('```gherkin', data['gherkin'])
        self.assertIn('Table Test', data['dbml'])
        self.assertIn('Feature: Test', data['gherkin'])


class DiscoveryAPITest(TestCase):
    """測試 Discovery API"""
    
    def setUp(self):
        self.client = Client()
        self.url = '/polls/discovery/'
        self.test_dbml = """Table MenuItem {
  id int [pk]
  name string [note: "菜品名稱"]
  price float [note: "價格"]
}"""
        self.test_gherkin = """Feature: 瀏覽菜單

  Rule: 客人可以查看所有菜品
    #TODO"""
    
    @patch('polls.api_utils.call_ollama_api')
    def test_discovery_success(self, mock_ollama):
        """測試成功的 Discovery 請求"""
        # Mock Ollama API 返回釐清項目
        mock_ollama.return_value = json.dumps([
            {
                "id": 1,
                "priority": "High",
                "location": "ERM: MenuItem → price 屬性",
                "question": "price 是否可以是負值？",
                "options": [
                    {"key": "A", "text": "不可以，必須 >= 0"},
                    {"key": "B", "text": "可以"}
                ]
            },
            {
                "id": 2,
                "priority": "Medium",
                "location": "Feature: 瀏覽菜單 → Rule: 客人可以查看所有菜品",
                "question": "此規則缺少 Example，應補充哪種情境？",
                "options": [
                    {"key": "A", "text": "成功瀏覽菜單"},
                    {"key": "B", "text": "菜單為空時的處理"},
                    {"key": "Short", "text": "其他情境"}
                ]
            }
        ])
        
        # 發送請求
        response = self.client.post(
            self.url,
            data=json.dumps({
                'dbml': self.test_dbml,
                'gherkin': self.test_gherkin
            }),
            content_type='application/json'
        )
        
        # 驗證回應
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertTrue(data['success'])
        self.assertEqual(len(data['items']), 2)
        self.assertEqual(data['statistics']['total'], 2)
        self.assertEqual(data['statistics']['high'], 1)
        self.assertEqual(data['statistics']['medium'], 1)
        self.assertEqual(data['statistics']['low'], 0)
        
    def test_discovery_missing_parameters(self):
        """測試缺少必要參數"""
        # 缺少 gherkin
        response = self.client.post(
            self.url,
            data=json.dumps({'dbml': self.test_dbml}),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 400)
        
        # 缺少 dbml
        response = self.client.post(
            self.url,
            data=json.dumps({'gherkin': self.test_gherkin}),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 400)
        
    @patch('polls.api_utils.call_ollama_api')
    def test_discovery_empty_result(self, mock_ollama):
        """測試無釐清項目的情況"""
        # Mock 返回空陣列
        mock_ollama.return_value = '[]'
        
        response = self.client.post(
            self.url,
            data=json.dumps({
                'dbml': self.test_dbml,
                'gherkin': self.test_gherkin
            }),
            content_type='application/json'
        )
        
        data = json.loads(response.content)
        self.assertTrue(data['success'])
        self.assertEqual(len(data['items']), 0)
        self.assertEqual(data['statistics']['total'], 0)
        
    @patch('polls.api_utils.call_ollama_api')
    def test_discovery_invalid_json_response(self, mock_ollama):
        """測試 AI 返回無效 JSON 的處理"""
        # Mock 返回無效 JSON
        mock_ollama.return_value = 'This is not valid JSON'
        
        response = self.client.post(
            self.url,
            data=json.dumps({
                'dbml': self.test_dbml,
                'gherkin': self.test_gherkin
            }),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 500)
        data = json.loads(response.content)
        self.assertFalse(data['success'])
        self.assertIn('無法解析為 JSON', data['error'])
        
    def test_discovery_method_not_allowed(self):
        """測試不允許的 HTTP 方法"""
        response = self.client.get(self.url)
        
        self.assertEqual(response.status_code, 405)


class IntegrationTest(TestCase):
    """整合測試: Formulation → Discovery 流程"""
    
    def setUp(self):
        self.client = Client()
        self.test_spec = """
我想做一個簡單的待辦事項系統。
用戶可以新增、編輯、刪除待辦事項。
每個待辦事項有標題、描述、狀態(待辦/完成)。
"""
    
    @patch('polls.api_utils.call_ollama_api')
    def test_formulation_to_discovery_workflow(self, mock_ollama):
        """測試 Formulation → Discovery 完整流程"""
        # 第一階段: Formulation
        mock_ollama.side_effect = [
            # DBML
            """Table TodoItem {
  id int [pk]
  title string [note: "標題"]
  description string [note: "描述"]
  status string [note: "狀態：待辦或完成"]
}""",
            # Gherkin
            """Feature: 管理待辦事項

  Rule: 用戶可以新增待辦事項
    Example: 成功新增
      Given 用戶已登入
      When 用戶新增待辦事項「買菜」
      Then 系統建立新的待辦事項""",
            # Discovery 結果
            json.dumps([
                {
                    "id": 1,
                    "priority": "High",
                    "location": "ERM: TodoItem → status 屬性",
                    "question": "status 的有效值為何？",
                    "options": [
                        {"key": "A", "text": "「待辦」和「完成」兩種"},
                        {"key": "B", "text": "可以有其他狀態"},
                        {"key": "Short", "text": "請列出所有可能值"}
                    ]
                }
            ])
        ]
        
        # Step 1: Formulation
        formulation_response = self.client.post(
            '/polls/formulation/',
            data=json.dumps({'spec_text': self.test_spec}),
            content_type='application/json'
        )
        
        self.assertEqual(formulation_response.status_code, 200)
        formulation_data = json.loads(formulation_response.content)
        self.assertTrue(formulation_data['success'])
        
        # Step 2: Discovery (使用 Formulation 的結果)
        discovery_response = self.client.post(
            '/polls/discovery/',
            data=json.dumps({
                'dbml': formulation_data['dbml'],
                'gherkin': formulation_data['gherkin']
            }),
            content_type='application/json'
        )
        
        self.assertEqual(discovery_response.status_code, 200)
        discovery_data = json.loads(discovery_response.content)
        self.assertTrue(discovery_data['success'])
        self.assertGreater(len(discovery_data['items']), 0)
        
        # 驗證釐清項目的結構
        first_item = discovery_data['items'][0]
        self.assertIn('id', first_item)
        self.assertIn('priority', first_item)
        self.assertIn('location', first_item)
        self.assertIn('question', first_item)
        self.assertIn('options', first_item)


class CompleteResultAPITest(TestCase):
    """測試完整結果生成 API"""
    
    def setUp(self):
        self.client = Client()
        self.url = '/polls/generate_complete_result/'
        self.test_dbml = """Table User {
  id int [pk]
  name string [note: "用戶名稱"]
  email string [note: "電子郵件"]
}"""
        self.test_gherkin = """Feature: 用戶註冊
  Rule: 電子郵件必須唯一
    Example: 成功註冊
      Given 系統中沒有 "test@example.com" 的用戶
      When 用戶使用 "test@example.com" 註冊
      Then 註冊成功"""
    
    @patch('polls.api_utils.call_ollama_api')
    def test_generate_complete_result_success(self, mock_ollama):
        """測試成功生成完整結果"""
        # Mock AI 返回不同部分的內容
        mock_ollama.side_effect = [
            # 背景說明
            "本系統是一個用戶管理平台，提供用戶註冊和登入功能。",
            # 專案目標
            "1. 實現用戶註冊功能\n2. 確保電子郵件唯一性\n3. 提供基本的用戶管理",
            # 流程圖 (Mermaid)
            """graph LR
    A[用戶輸入資料] --> B{檢查郵件}
    B -->|唯一| C[註冊成功]
    B -->|重複| D[顯示錯誤]""",
            # API 規格
            """### POST /api/users/register
**描述**: 註冊新用戶
**請求參數**:
- name (string): 用戶名稱
- email (string): 電子郵件
**回應**:
- 200: 註冊成功
- 400: 郵件已存在"""
        ]
        
        response = self.client.post(
            self.url,
            data=json.dumps({
                'dbml': self.test_dbml,
                'gherkin': self.test_gherkin
            }),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        
        # 驗證返回結構
        self.assertTrue(data['success'])
        self.assertIn('background', data)
        self.assertIn('goals', data)
        self.assertIn('flowchart', data)
        self.assertIn('api_spec', data)
        
        # 驗證內容不為空
        self.assertGreater(len(data['background']), 0)
        self.assertGreater(len(data['goals']), 0)
        self.assertGreater(len(data['flowchart']), 0)
        self.assertGreater(len(data['api_spec']), 0)
        
        # 驗證流程圖包含 Mermaid 語法
        self.assertIn('graph', data['flowchart'])
    
    @patch('polls.api_utils.call_ollama_api')
    def test_generate_complete_result_missing_parameters(self, mock_ollama):
        """測試缺少必要參數"""
        # 缺少 gherkin
        response = self.client.post(
            self.url,
            data=json.dumps({'dbml': self.test_dbml}),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.content)
        self.assertFalse(data['success'])
        self.assertIn('error', data)
    
    @patch('polls.api_utils.call_ollama_api')
    def test_generate_complete_result_ai_error(self, mock_ollama):
        """測試 AI 呼叫失敗"""
        mock_ollama.side_effect = Exception("AI service error")
        
        response = self.client.post(
            self.url,
            data=json.dumps({
                'dbml': self.test_dbml,
                'gherkin': self.test_gherkin
            }),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 500)
        data = json.loads(response.content)
        self.assertFalse(data['success'])
        self.assertIn('error', data)
    
    def test_generate_complete_result_method_not_allowed(self):
        """測試不支援的 HTTP 方法"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 405)


class CompleteResultIntegrationTest(TestCase):
    """測試完整流程: Formulation → Discovery → Complete Result"""
    
    def setUp(self):
        self.client = Client()
        self.test_spec = """
我想做一個部落格系統。
用戶可以發表文章、留言。
每篇文章有標題、內容、作者、發布時間。
"""
    
    @patch('polls.api_utils.call_ollama_api')
    def test_full_workflow(self, mock_ollama):
        """測試從 Formulation 到完整結果的完整流程"""
        mock_ollama.side_effect = [
            # Formulation: DBML
            """Table Article {
  id int [pk]
  title string [note: "標題"]
  content string [note: "內容"]
  author string [note: "作者"]
  publish_time string [note: "發布時間"]
}""",
            # Formulation: Gherkin
            """Feature: 發表文章
  Rule: 標題不可為空
    Example: 成功發表
      Given 用戶已登入
      When 用戶填寫標題和內容
      Then 文章發表成功""",
            # Discovery
            json.dumps([{"id": 1, "priority": "High", "location": "Article", "question": "測試", "options": []}]),
            # Complete Result: 背景
            "部落格系統用於內容發布和互動。",
            # Complete Result: 目標
            "1. 發表文章\n2. 管理留言",
            # Complete Result: 流程圖
            "graph TD\nA[開始] --> B[結束]",
            # Complete Result: API
            "POST /api/articles"
        ]
        
        # Step 1: Formulation
        formulation_response = self.client.post(
            '/polls/formulation/',
            data=json.dumps({'spec_text': self.test_spec}),
            content_type='application/json'
        )
        formulation_data = json.loads(formulation_response.content)
        self.assertTrue(formulation_data['success'])
        
        # Step 2: Discovery
        discovery_response = self.client.post(
            '/polls/discovery/',
            data=json.dumps({
                'dbml': formulation_data['dbml'],
                'gherkin': formulation_data['gherkin']
            }),
            content_type='application/json'
        )
        discovery_data = json.loads(discovery_response.content)
        self.assertTrue(discovery_data['success'])
        
        # Step 3: Generate Complete Result
        complete_response = self.client.post(
            '/polls/generate_complete_result/',
            data=json.dumps({
                'dbml': formulation_data['dbml'],
                'gherkin': formulation_data['gherkin']
            }),
            content_type='application/json'
        )
        complete_data = json.loads(complete_response.content)
        
        self.assertEqual(complete_response.status_code, 200)
        self.assertTrue(complete_data['success'])
        self.assertIn('background', complete_data)
        self.assertIn('goals', complete_data)
        self.assertIn('flowchart', complete_data)
        self.assertIn('api_spec', complete_data)
