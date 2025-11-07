#!/usr/bin/env python
"""
檢查環境變數設定腳本
執行方式：python check_env.py
"""
import os
import sys
from pathlib import Path

# 添加專案路徑
BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR / 'mysite'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')

import django
django.setup()

from django.conf import settings
from polls.api_utils import check_api_keys, test_openai_connection, test_ollama_connection


def print_header(text):
    """印出標題"""
    print("\n" + "=" * 60)
    print(f" {text}")
    print("=" * 60)


def print_status(name, status, details=""):
    """印出狀態"""
    symbol = "✅" if status else "❌"
    print(f"{symbol} {name}")
    if details:
        print(f"   {details}")


def main():
    print_header("Django 專案環境變數檢查")
    
    # 1. 檢查 .env 檔案
    env_file = BASE_DIR / '.env'
    print_status(
        ".env 檔案",
        env_file.exists(),
        f"路徑: {env_file}" if env_file.exists() else "請建立 .env 檔案"
    )
    
    # 2. 檢查 Django 基本設定
    print_header("Django 基本設定")
    print_status(
        "SECRET_KEY",
        bool(settings.SECRET_KEY),
        f"已設定 ({settings.SECRET_KEY[:20]}...)"
    )
    print_status(
        "DEBUG 模式",
        settings.DEBUG,
        "已啟用" if settings.DEBUG else "已關閉"
    )
    print_status(
        "ALLOWED_HOSTS",
        bool(settings.ALLOWED_HOSTS),
        f"{', '.join(settings.ALLOWED_HOSTS)}"
    )
    
    # 3. 檢查 API Keys
    print_header("API Keys 設定")
    api_status = check_api_keys()
    
    # OpenAI
    openai_configured = api_status['openai']['configured']
    print_status(
        "OpenAI API Key",
        openai_configured,
        api_status['openai']['key'] if openai_configured else "未設定"
    )
    if openai_configured:
        print(f"   模型: {api_status['openai']['model']}")
    
    # Ollama
    ollama_configured = api_status['ollama']['configured']
    print_status(
        "Ollama 設定",
        ollama_configured,
        f"{api_status['ollama']['key']} @ {api_status['ollama']['host']} "
        f"({api_status['ollama']['model']})" if ollama_configured
        else "未設定"
    )
    
    # Sentence Transformer
    print_status(
        "Sentence Transformer",
        True,
        api_status['sentence_transformer']['model']
    )
    
    # 4. 測試 API 連接
    print_header("API 連接測試")
    
    # 測試 OpenAI
    if openai_configured:
        print("正在測試 OpenAI API 連接...")
        try:
            success, message = test_openai_connection()
            print_status("OpenAI API", success, message)
        except Exception as e:
            print_status("OpenAI API", False, f"錯誤: {str(e)}")
    else:
        print("⏭️  跳過 OpenAI 測試（未設定 API Key）")
    
    # 測試 Ollama
    if ollama_configured:
        print("\n正在測試 Ollama API 連接...")
        try:
            success, message = test_ollama_connection()
            print_status("Ollama API", success, message)
        except Exception as e:
            print_status("Ollama API", False, f"錯誤: {str(e)}")
    else:
        print("⏭️  跳過 Ollama 測試（未設定 API Key）")
    
    # 5. 其他設定
    print_header("其他設定")
    print_status(
        "FAISS 索引路徑",
        True,
        settings.FAISS_INDEX_PATH
    )
    print_status(
        "上傳檔案路徑",
        True,
        settings.UPLOAD_PATH
    )
    print_status(
        "最大上傳大小",
        True,
        f"{settings.MAX_UPLOAD_SIZE / 1024 / 1024:.1f} MB"
    )
    
    # 6. 總結
    print_header("總結")
    
    critical_issues = []
    if not env_file.exists():
        critical_issues.append("未找到 .env 檔案")
    if not openai_configured:
        critical_issues.append("OpenAI API Key 未設定（如需使用真實 AI 服務）")
    
    if critical_issues:
        print("\n⚠️  發現以下需要注意的項目：")
        for issue in critical_issues:
            print(f"   • {issue}")
        print("\n建議：")
        print("   1. 複製 .env.example 為 .env")
        print("   2. 在 .env 中設定 OPENAI_API_KEY")
        print("   3. 或使用 Ollama 本地 LLM（無需 API Key）")
    else:
        print("\n✅ 所有設定檢查完成！")
    
    print("\n" + "=" * 60)
    print("執行 'python manage.py runserver' 啟動專案")
    print("=" * 60 + "\n")


if __name__ == '__main__':
    main()
