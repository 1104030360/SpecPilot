"""
API 工具函數
提供 OpenAI、Ollama 和 Sentence Transformers 的整合函數
"""
import os
from django.conf import settings


def get_openai_client():
    """
    取得 OpenAI 客戶端
    
    使用方式：
        from polls.api_utils import call_openai_api
        
        result = call_openai_api(
            prompt="Classify this text",
            user_input="This is a great product!"
        )
    """
    try:
        import openai
        openai.api_key = settings.OPENAI_API_KEY
        return openai
    except ImportError:
        raise ImportError(
            "請先安裝 openai: pip install openai\n"
            "並在 .env 中設定 OPENAI_API_KEY"
        )


def call_openai_api(prompt, user_input, model=None, temperature=None, max_tokens=None):
    """
    呼叫 OpenAI API
    
    參數：
        prompt: 系統提示詞
        user_input: 使用者輸入
        model: 模型名稱（預設從 settings 讀取）
        temperature: 溫度參數（預設從 settings 讀取）
        max_tokens: 最大 token 數（預設從 settings 讀取）
    
    回傳：
        str: AI 生成的文本
    
    範例：
        result = call_openai_api(
            prompt="You are a helpful assistant",
            user_input="What is Django?",
            model="gpt-4",
            temperature=0.7
        )
    """
    if not settings.OPENAI_API_KEY:
        raise ValueError(
            "未設定 OPENAI_API_KEY\n"
            "請在 .env 檔案中設定：OPENAI_API_KEY=your-api-key"
        )
    
    openai = get_openai_client()
    
    response = openai.ChatCompletion.create(
        model=model or settings.OPENAI_MODEL,
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": user_input}
        ],
        temperature=temperature or settings.OPENAI_TEMPERATURE,
        max_tokens=max_tokens or settings.OPENAI_MAX_TOKENS
    )
    
    return response.choices[0].message.content


def call_ollama_api(prompt, user_input, model=None):
    """
    呼叫 Ollama Cloud API
    
    參數：
        prompt: 系統提示詞
        user_input: 使用者輸入
        model: 模型名稱（預設從 settings 讀取）
    
    回傳：
        str: AI 生成的文本
    
    範例：
        result = call_ollama_api(
            prompt="You are a helpful assistant",
            user_input="What is Django?",
            model="gpt-oss:120b"
        )
    """
    try:
        from ollama import Client
    except ImportError:
        raise ImportError(
            "請先安裝 ollama: pip install ollama\n"
            "並在 .env 中設定 OLLAMA_API_KEY 和 OLLAMA_HOST"
        )
    
    if not settings.OLLAMA_API_KEY:
        raise ValueError(
            "未設定 OLLAMA_API_KEY\n"
            "請在 .env 檔案中設定：OLLAMA_API_KEY=your-api-key"
        )
    
    client = Client(
        host=settings.OLLAMA_HOST,
        headers={'Authorization': 'Bearer ' + settings.OLLAMA_API_KEY}
    )
    
    model_name = model or settings.OLLAMA_MODEL
    
    messages = [
        {
            'role': 'system',
            'content': prompt,
        },
        {
            'role': 'user',
            'content': user_input,
        },
    ]
    
    try:
        # 使用串流方式接收回應
        full_response = ""
        for part in client.chat(model_name, messages=messages, stream=True):
            full_response += part['message']['content']
        
        return full_response
    except Exception as e:
        raise ConnectionError(
            f"無法連接到 Ollama API ({settings.OLLAMA_HOST})\n"
            f"錯誤訊息：{str(e)}"
        )


def get_sentence_transformer_model():
    """
    取得 Sentence Transformer 模型
    
    使用方式：
        from polls.api_utils import calculate_sentence_similarity
        
        similarity = calculate_sentence_similarity(
            "用戶可以登入系統",
            "使用者能夠登入平台"
        )
    """
    try:
        from sentence_transformers import SentenceTransformer
        model = SentenceTransformer(settings.SENTENCE_TRANSFORMER_MODEL)
        return model
    except ImportError:
        raise ImportError(
            "請先安裝 sentence-transformers:\n"
            "pip install sentence-transformers"
        )


def calculate_sentence_similarity(sentence1, sentence2):
    """
    使用 Sentence Transformers 計算語義相似度
    
    參數：
        sentence1: 第一個句子
        sentence2: 第二個句子
    
    回傳：
        float: 相似度分數（0-1 之間）
    
    範例：
        similarity = calculate_sentence_similarity(
            "用戶可以登入系統",
            "使用者能夠登入平台"
        )
        print(f"相似度: {similarity:.2f}")
    """
    from sklearn.metrics.pairwise import cosine_similarity
    
    model = get_sentence_transformer_model()
    embeddings = model.encode([sentence1, sentence2])
    similarity = cosine_similarity([embeddings[0]], [embeddings[1]])[0][0]
    
    return float(similarity)


def check_api_keys():
    """
    檢查所有 API Key 是否已設定
    
    回傳：
        dict: 各項 API 的設定狀態
    
    使用方式：
        from polls.api_utils import check_api_keys
        
        status = check_api_keys()
        if not status['openai']['configured']:
            print("請設定 OpenAI API Key")
    """
    openai_key = (settings.OPENAI_API_KEY[:10] + '...'
                  if settings.OPENAI_API_KEY else None)
    ollama_key = (settings.OLLAMA_API_KEY[:10] + '...'
                  if settings.OLLAMA_API_KEY else None)
    
    status = {
        'openai': {
            'configured': bool(settings.OPENAI_API_KEY),
            'key': openai_key,
            'model': settings.OPENAI_MODEL
        },
        'ollama': {
            'configured': bool(settings.OLLAMA_API_KEY),
            'key': ollama_key,
            'host': settings.OLLAMA_HOST,
            'model': settings.OLLAMA_MODEL
        },
        'sentence_transformer': {
            'configured': True,  # 本地模型，不需要 API Key
            'model': settings.SENTENCE_TRANSFORMER_MODEL
        }
    }
    
    return status


def test_openai_connection():
    """
    測試 OpenAI API 連接
    
    回傳：
        tuple: (成功與否, 訊息)
    
    使用方式：
        from polls.api_utils import test_openai_connection
        
        success, message = test_openai_connection()
        print(message)
    """
    try:
        result = call_openai_api(
            prompt="You are a helpful assistant",
            user_input="Say hello",
            max_tokens=10
        )
        return True, f"連接成功！回應：{result}"
    except Exception as e:
        return False, f"連接失敗：{str(e)}"


def test_ollama_connection():
    """
    測試 Ollama API 連接
    
    回傳：
        tuple: (成功與否, 訊息)
    """
    try:
        result = call_ollama_api(
            prompt="You are a helpful assistant",
            user_input="Say hello"
        )
        return True, f"連接成功！回應：{result[:50]}..."
    except Exception as e:
        return False, f"連接失敗：{str(e)}"


# 為了向後兼容，提供模擬函數的別名
def simulate_ai_generation(task_type, model, prompt, user_input):
    """
    模擬 AI 生成（向後兼容）
    如果未設定 OPENAI_API_KEY，則回傳模擬回應
    """
    if settings.OPENAI_API_KEY:
        try:
            return call_openai_api(prompt, user_input, model=model)
        except Exception as e:
            print(f"OpenAI API 呼叫失敗：{e}，使用模擬回應")
    
    # 模擬回應
    return f"""[模擬 AI 回應]
任務類型：{task_type}
模型：{model}

根據輸入「{user_input}」，AI 生成以下內容：

這是一個模擬的 AI 回應。實際專案應串接 OpenAI API 或 Ollama 等 LLM 服務。
提示詞：{prompt}

使用者輸入：{user_input[:50]}{"..." if len(user_input) > 50 else ""}

---
實際部署時，請在 .env 中設定 OPENAI_API_KEY
或啟動 Ollama：ollama serve
"""
