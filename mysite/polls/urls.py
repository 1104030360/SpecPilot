from django.urls import path
from . import views

urlpatterns = [
    path('', views.spec_generator, name='spec_generator'),
    path('weight-config-page/', views.weight_config_page, name='weight_config_page'),
    path('field-priority-page/', views.field_priority_page, name='field_priority_page'),
    path('generate-specification/', views.generate_specification_api, name='generate_specification_api'),
    path('retry-ai/', views.retry_ai_api, name='retry_ai_api'),
    path('user/', views.user_list, name='user-list'),
    path('user/<int:user_id>/', views.user_detail, name='user-detail'),
    path('order/', views.order_list, name='order-list'),
    path('order/<int:order_id>/', views.order_detail, name='order-detail'),
    path('weight-config/', views.weight_config_list, name='weight_config_list'),
    path('weight-config/<int:config_id>/', views.weight_config_detail, name='weight_config_detail'),
    path(
        'field-priority/',
        views.field_priority_list,
        name='field_priority_list'
    ),
    path(
        'field-priority/<int:config_id>/',
        views.field_priority_detail,
        name='field_priority_detail'
    ),
    path('sentence-db/', views.sentence_db_list, name='sentence_db_list'),
    path('sentence-db/<int:sentence_id>/', views.sentence_db_detail, name='sentence_db_detail'),
    path('sentence-similarity/', views.sentence_similarity_api, name='sentence_similarity_api'),
    path('gpt-prompt/', views.gpt_prompt_list, name='gpt_prompt_list'),
    path('gpt-prompt/<int:prompt_id>/', views.gpt_prompt_detail, name='gpt_prompt_detail'),
    path('gpt-generate/', views.gpt_generate_api, name='gpt_generate_api'),
    path('llm-ideas/', views.llm_ideas_api, name='llm_ideas_api'),
    path('generate-field/', views.generate_field_api, name='generate_field_api'),
    # 進階規格產出 API
    path('formulation/', views.formulation_api, name='formulation_api'),
    path('discovery/', views.discovery_api, name='discovery_api'),
    path('generate_complete_result/', views.generate_complete_result_api, name='generate_complete_result_api'),
    path('sync-path/', views.sync_path_list, name='sync-path-list'),
    path('sync-path/<int:path_id>/', views.sync_path_detail, name='sync-path-detail'),
    path('chat-session/', views.chat_session_list, name='chat-session-list'),
    path('chat-session/<str:session_id>/', views.chat_session_detail, name='chat-session-detail'),
    path('category-memory/', views.category_memory_list, name='category-memory-list'),
    path('category-memory/<int:memory_id>/', views.category_memory_detail, name='category-memory-detail'),
    path('uploaded-file/', views.uploaded_file_list, name='uploaded-file-list'),
    path('uploaded-file/<int:file_id>/', views.uploaded_file_detail, name='uploaded-file-detail'),
    path('faiss-index/status/', views.faiss_index_status, name='faiss-index-status'),
    path('faiss-index/rebuild/', views.faiss_index_rebuild, name='faiss-index-rebuild'),
    path('faiss-index/sync/', views.faiss_index_sync, name='faiss-index-sync'),
]
