import json
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ValidationError
from .models import TB_1, WeightConfiguration, FieldPriorityConfiguration
from .models import SentenceDatabase, GPTPromptConfiguration, SyncPathConfiguration
from .models import ChatSession, CategoryMemory, UploadedFile, User, Order


# User CRUD API
@csrf_exempt
def user_list(request):
    if request.method == 'GET':
        users = User.objects.all()
        data = [
            {
                'id': u.id,
                'username': u.username,
                'email': u.email,
                'created_at': u.created_at,
            } for u in users
        ]
        return JsonResponse({'users': data})
    elif request.method == 'POST':
        try:
            payload = json.loads(request.body.decode())
            user = User(
                username=payload.get('username', ''),
                email=payload.get('email', ''),
                password=payload.get('password', ''),
            )
            user.clean()
            user.save()
            return JsonResponse({'result': 'created', 'id': user.id}, status=201)
        except ValidationError as e:
            return JsonResponse({'error': str(e)}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)


@csrf_exempt
def user_detail(request, user_id):
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return JsonResponse({'error': 'Not found'}, status=404)

    if request.method == 'GET':
        data = {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'created_at': user.created_at,
        }
        return JsonResponse(data)
    elif request.method == 'PUT':
        try:
            payload = json.loads(request.body.decode())
            user.username = payload.get('username', user.username)
            user.email = payload.get('email', user.email)
            if 'password' in payload:
                user.password = payload['password']
            user.clean()
            user.save()
            return JsonResponse({'result': 'updated'}, status=200)
        except ValidationError as e:
            return JsonResponse({'error': str(e)}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    elif request.method == 'DELETE':
        user.delete()
        return JsonResponse({'result': 'deleted'}, status=204)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)


# Order CRUD API
@csrf_exempt
def order_list(request):
    if request.method == 'GET':
        orders = Order.objects.all()
        data = [
            {
                'id': o.id,
                'user_id': o.user.id,
                'product_name': o.product_name,
                'amount': o.amount,
                'status': o.status,
                'created_at': o.created_at,
            } for o in orders
        ]
        return JsonResponse({'orders': data})
    elif request.method == 'POST':
        try:
            payload = json.loads(request.body.decode())
            user_id = payload.get('user_id')
            if not user_id:
                return JsonResponse({'error': 'user_id 必填'}, status=400)
            
            user = User.objects.get(id=user_id)
            order = Order(
                user=user,
                product_name=payload.get('product_name', ''),
                amount=payload.get('amount', 0),
                status=payload.get('status', 'pending'),
            )
            order.clean()
            order.save()
            return JsonResponse(
                {'result': 'created', 'id': order.id},
                status=201
            )
        except User.DoesNotExist:
            return JsonResponse({'error': 'User not found'}, status=404)
        except ValidationError as e:
            return JsonResponse({'error': str(e)}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)


@csrf_exempt
def order_detail(request, order_id):
    try:
        order = Order.objects.get(id=order_id)
    except Order.DoesNotExist:
        return JsonResponse({'error': 'Not found'}, status=404)

    if request.method == 'GET':
        data = {
            'id': order.id,
            'user_id': order.user.id,
            'product_name': order.product_name,
            'amount': order.amount,
            'status': order.status,
            'created_at': order.created_at,
        }
        return JsonResponse(data)
    elif request.method == 'PUT':
        try:
            payload = json.loads(request.body.decode())
            if 'user_id' in payload:
                user = User.objects.get(id=payload['user_id'])
                order.user = user
            order.product_name = payload.get(
                'product_name', order.product_name
            )
            order.amount = payload.get('amount', order.amount)
            order.status = payload.get('status', order.status)
            order.clean()
            order.save()
            return JsonResponse({'result': 'updated'}, status=200)
        except User.DoesNotExist:
            return JsonResponse({'error': 'User not found'}, status=404)
        except ValidationError as e:
            return JsonResponse({'error': str(e)}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    elif request.method == 'DELETE':
        order.delete()
        return JsonResponse({'result': 'deleted'}, status=204)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)


# 雲端同步路徑配置 CRUD API
@csrf_exempt
def sync_path_list(request):
    if request.method == 'GET':
        items = SyncPathConfiguration.objects.all()
        data = [
            {
                'id': i.id,
                'path': i.path,
                'updated_at': i.updated_at,
            } for i in items
        ]
        return JsonResponse({'paths': data})
    elif request.method == 'POST':
        try:
            payload = json.loads(request.body.decode())
            name = payload.get('name', '').strip()
            path = payload.get('path', '').strip()
            if not name:
                return JsonResponse({'error': 'name 必須為非空字串'}, status=400)
            item = SyncPathConfiguration(name=name, path=path)
            try:
                item.clean()
            except ValidationError as e:
                return JsonResponse({'error': str(e)}, status=400)
            item.save()
            return JsonResponse({'result': 'created', 'id': item.id}, status=201)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)


@csrf_exempt
def sync_path_detail(request, path_id):
    try:
        item = SyncPathConfiguration.objects.get(id=path_id)
    except SyncPathConfiguration.DoesNotExist:
        return JsonResponse({'error': 'Not found'}, status=404)

    if request.method == 'GET':
        data = {
            'id': item.id,
            'path': item.path,
            'updated_at': item.updated_at,
        }
        return JsonResponse(data)
    elif request.method == 'PUT':
        try:
            payload = json.loads(request.body.decode())
            name = payload.get('name', item.name).strip()
            path = payload.get('path', item.path).strip()
            if not name:
                return JsonResponse({'error': 'name 必須為非空字串'}, status=400)
            item.name = name
            item.path = path
            try:
                item.clean()
            except ValidationError as e:
                return JsonResponse({'error': str(e)}, status=400)
            item.save()
            return JsonResponse({'result': 'updated'}, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    elif request.method == 'DELETE':
        item.delete()
        return JsonResponse({}, status=204)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)


# 聊天會話 CRUD API
@csrf_exempt
def chat_session_list(request):
    if request.method == 'GET':
        items = ChatSession.objects.all()
        data = [
            {
                'session_id': i.session_id,
                'title': i.title,
                'messages': i.messages,
                'created_at': i.created_at,
                'updated_at': i.updated_at,
            } for i in items
        ]
        return JsonResponse({'sessions': data})
    elif request.method == 'POST':
        try:
            payload = json.loads(request.body.decode())
            session_id = payload.get('session_id', '').strip()
            title = payload.get('title', '').strip()
            messages = payload.get('messages', [])
            if not session_id:
                return JsonResponse(
                    {'error': 'session_id 必須為非空字串'}, status=400
                )
            item = ChatSession(
                session_id=session_id, title=title, messages=messages
            )
            try:
                item.clean()
            except ValidationError as e:
                return JsonResponse({'error': str(e)}, status=400)
            item.save()
            return JsonResponse(
                {'result': 'created', 'session_id': item.session_id},
                status=201
            )
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)


@csrf_exempt
def chat_session_detail(request, session_id):
    try:
        item = ChatSession.objects.get(session_id=session_id)
    except ChatSession.DoesNotExist:
        return JsonResponse({'error': 'Not found'}, status=404)

    if request.method == 'GET':
        data = {
            'session_id': item.session_id,
            'title': item.title,
            'messages': item.messages,
            'created_at': item.created_at,
            'updated_at': item.updated_at,
        }
        return JsonResponse(data)
    elif request.method == 'PUT':
        try:
            payload = json.loads(request.body.decode())
            title = payload.get('title', item.title).strip()
            messages = payload.get('messages', item.messages)
            item.title = title
            item.messages = messages
            try:
                item.clean()
            except ValidationError as e:
                return JsonResponse({'error': str(e)}, status=400)
            item.save()
            return JsonResponse({'result': 'updated'}, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    elif request.method == 'DELETE':
        item.delete()
        return JsonResponse({}, status=204)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)


# AI分類記憶 CRUD API
@csrf_exempt
def category_memory_list(request):
    if request.method == 'GET':
        items = CategoryMemory.objects.all()
        data = [
            {
                'id': i.id,
                'configuration_item': i.configuration_item,
                'category': i.category,
                'created_at': i.created_at,
                'updated_at': i.updated_at,
            } for i in items
        ]
        return JsonResponse({'memories': data})
    elif request.method == 'POST':
        try:
            payload = json.loads(request.body.decode())
            config_item = payload.get('configuration_item', '').strip()
            category = payload.get('category', '').strip()
            if not config_item:
                return JsonResponse(
                    {'error': 'configuration_item 必須為非空字串'},
                    status=400
                )
            if not category:
                return JsonResponse(
                    {'error': 'category 必須為非空字串'}, status=400
                )
            item = CategoryMemory(
                configuration_item=config_item, category=category
            )
            try:
                item.clean()
            except ValidationError as e:
                return JsonResponse({'error': str(e)}, status=400)
            item.save()
            return JsonResponse(
                {'result': 'created', 'id': item.id}, status=201
            )
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)


@csrf_exempt
def category_memory_detail(request, memory_id):
    try:
        item = CategoryMemory.objects.get(id=memory_id)
    except CategoryMemory.DoesNotExist:
        return JsonResponse({'error': 'Not found'}, status=404)

    if request.method == 'GET':
        data = {
            'id': item.id,
            'configuration_item': item.configuration_item,
            'category': item.category,
            'created_at': item.created_at,
            'updated_at': item.updated_at,
        }
        return JsonResponse(data)
    elif request.method == 'PUT':
        try:
            payload = json.loads(request.body.decode())
            config_item = payload.get(
                'configuration_item', item.configuration_item
            ).strip()
            category = payload.get('category', item.category).strip()
            if not config_item:
                return JsonResponse(
                    {'error': 'configuration_item 必須為非空字串'},
                    status=400
                )
            if not category:
                return JsonResponse(
                    {'error': 'category 必須為非空字串'}, status=400
                )
            item.configuration_item = config_item
            item.category = category
            try:
                item.clean()
            except ValidationError as e:
                return JsonResponse({'error': str(e)}, status=400)
            item.save()
            return JsonResponse({'result': 'updated'}, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    elif request.method == 'DELETE':
        item.delete()
        return JsonResponse({}, status=204)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)


# 上傳檔案記錄 CRUD API
@csrf_exempt
def uploaded_file_list(request):
    if request.method == 'GET':
        items = UploadedFile.objects.all()
        data = [
            {
                'id': i.id,
                'filename': i.filename,
                'stored_filename': i.stored_filename,
                'upload_time': i.upload_time,
                'file_size': i.file_size,
                'file_path': i.file_path,
            } for i in items
        ]
        return JsonResponse({'files': data})
    elif request.method == 'POST':
        try:
            payload = json.loads(request.body.decode())
            filename = payload.get('filename', '').strip()
            stored_filename = payload.get('stored_filename', '').strip()
            file_size = payload.get('file_size', 0)
            file_path = payload.get('file_path', 'uploads/').strip()
            if not filename:
                return JsonResponse(
                    {'error': 'filename 必須為非空字串'}, status=400
                )
            item = UploadedFile(
                filename=filename,
                stored_filename=stored_filename,
                file_size=file_size,
                file_path=file_path
            )
            try:
                item.clean()
            except ValidationError as e:
                return JsonResponse({'error': str(e)}, status=400)
            item.save()
            return JsonResponse(
                {'result': 'created', 'id': item.id}, status=201
            )
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)


@csrf_exempt
def uploaded_file_detail(request, file_id):
    try:
        item = UploadedFile.objects.get(id=file_id)
    except UploadedFile.DoesNotExist:
        return JsonResponse({'error': 'Not found'}, status=404)

    if request.method == 'GET':
        data = {
            'id': item.id,
            'filename': item.filename,
            'stored_filename': item.stored_filename,
            'upload_time': item.upload_time,
            'file_size': item.file_size,
            'file_path': item.file_path,
        }
        return JsonResponse(data)
    elif request.method == 'DELETE':
        item.delete()
        return JsonResponse({}, status=204)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)


# FAISS 索引管理 API（模擬版）
@csrf_exempt
def faiss_index_status(request):
    """查詢 FAISS 索引狀態"""
    if request.method == 'GET':
        import os
        base_path = 'faiss_data/'
        index_file = os.path.join(base_path, 'kb_index.faiss')
        metadata_file = os.path.join(base_path, 'kb_metadata.json')
        texts_file = os.path.join(base_path, 'kb_texts.pkl')
        
        status = {
            'index_exists': os.path.exists(index_file),
            'metadata_exists': os.path.exists(metadata_file),
            'texts_exists': os.path.exists(texts_file),
            'dimension': 384,
            'index_type': 'IndexFlatL2 + IndexIDMap',
            'record_count': 0  # 模擬值
        }
        return JsonResponse(status)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)


@csrf_exempt
def faiss_index_rebuild(request):
    """重建 FAISS 索引（模擬）"""
    if request.method == 'POST':
        import os
        base_path = 'faiss_data/'
        os.makedirs(base_path, exist_ok=True)
        
        # 模擬建立檔案
        index_file = os.path.join(base_path, 'kb_index.faiss')
        metadata_file = os.path.join(base_path, 'kb_metadata.json')
        texts_file = os.path.join(base_path, 'kb_texts.pkl')
        
        # 寫入空檔案模擬重建
        with open(index_file, 'w') as f:
            f.write('FAISS_INDEX_MOCK')
        with open(metadata_file, 'w') as f:
            f.write('{}')
        with open(texts_file, 'w') as f:
            f.write('TEXTS_MOCK')
        
        return JsonResponse({
            'result': 'rebuilt',
            'dimension': 384,
            'files_created': 3
        }, status=201)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)


@csrf_exempt
def faiss_index_sync(request):
    """同步 FAISS 索引與 Ticket（模擬）"""
    if request.method == 'POST':
        from .models import Ticket
        ticket_count = Ticket.objects.count()
        
        return JsonResponse({
            'result': 'synced',
            'tickets_synced': ticket_count,
            'dimension': 384
        }, status=200)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)


# GPT提示詞配置 CRUD API
@csrf_exempt
def gpt_prompt_list(request):
    if request.method == 'GET':
        items = GPTPromptConfiguration.objects.all()
        data = [
            {
                'id': i.id,
                'task_type': i.task_type,
                'prompt': i.prompt,
                'model': i.model,
                'updated_at': i.updated_at,
            } for i in items
        ]
        return JsonResponse({'prompts': data})
    elif request.method == 'POST':
        try:
            payload = json.loads(request.body.decode())
            item = GPTPromptConfiguration(
                task_type=payload.get('task_type', 'custom'),
                prompt=payload.get('prompt', ''),
                model=payload.get('model', 'gpt-3.5-turbo'),
            )
            try:
                item.clean()
            except ValidationError as e:
                return JsonResponse({'error': str(e)}, status=400)
            item.save()
            return JsonResponse({'result': 'created', 'id': item.id})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)


@csrf_exempt
def gpt_prompt_detail(request, prompt_id):
    try:
        item = GPTPromptConfiguration.objects.get(id=prompt_id)
    except GPTPromptConfiguration.DoesNotExist:
        return JsonResponse({'error': 'Not found'}, status=404)

    if request.method == 'GET':
        data = {
            'id': item.id,
            'task_type': item.task_type,
            'prompt': item.prompt,
            'model': item.model,
            'updated_at': item.updated_at,
        }
        return JsonResponse(data)
    elif request.method == 'PUT':
        try:
            payload = json.loads(request.body.decode())
            item.task_type = payload.get('task_type', item.task_type)
            item.prompt = payload.get('prompt', item.prompt)
            item.model = payload.get('model', item.model)
            try:
                item.clean()
            except ValidationError as e:
                return JsonResponse({'error': str(e)}, status=400)
            item.save()
            return JsonResponse({'result': 'updated'})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    elif request.method == 'DELETE':
        item.delete()
        return JsonResponse({'result': 'deleted'})
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)

  
@csrf_exempt
def weight_config_list(request):
    if request.method == 'GET':
        configs = WeightConfiguration.objects.all()
        data = [
            {
                'id': c.id,
                'name': c.name,
                'score_a': c.score_a,
                'score_b': c.score_b,
                'score_c': c.score_c,
                'score_d': c.score_d,
            } for c in configs
        ]
        return JsonResponse({'configs': data})
    elif request.method == 'POST':
        try:
            payload = json.loads(request.body.decode())
            config = WeightConfiguration(
                name=payload.get('name', ''),
                score_a=payload.get('score_a', 0.25),
                score_b=payload.get('score_b', 0.25),
                score_c=payload.get('score_c', 0.25),
                score_d=payload.get('score_d', 0.25),
            )
            config.clean()
            config.save()
            return JsonResponse({'result': 'created', 'id': config.id})
        except ValidationError as e:
            return JsonResponse({'error': str(e)}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)


@csrf_exempt
def sentence_db_list(request):
    if request.method == 'GET':
        items = SentenceDatabase.objects.all()
        data = [
            {
                'id': i.id,
                'user': i.user,
                'sentence': i.sentence,
                'category': i.category,
                'embedding': i.embedding,
                'created_at': i.created_at,
                'updated_at': i.updated_at,
            } for i in items
        ]
        return JsonResponse({'sentences': data})
    elif request.method == 'POST':
        try:
            payload = json.loads(request.body.decode())
            item = SentenceDatabase(
                user=payload.get('user', ''),
                sentence=payload.get('sentence', ''),
                category=payload.get('category', ''),
                embedding=payload.get('embedding', []),
            )
            item.clean()
            item.save()
            return JsonResponse({'result': 'created', 'id': item.id})
        except ValidationError as e:
            return JsonResponse({'error': str(e)}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)


@csrf_exempt
def sentence_db_detail(request, sentence_id):
    try:
        item = SentenceDatabase.objects.get(id=sentence_id)
    except SentenceDatabase.DoesNotExist:
        return JsonResponse({'error': 'Not found'}, status=404)

    if request.method == 'GET':
        data = {
            'id': item.id,
            'user': item.user,
            'sentence': item.sentence,
            'category': item.category,
            'embedding': item.embedding,
            'created_at': item.created_at,
            'updated_at': item.updated_at,
        }
        return JsonResponse(data)
    elif request.method == 'PUT':
        try:
            payload = json.loads(request.body.decode())
            item.user = payload.get('user', item.user)
            item.sentence = payload.get('sentence', item.sentence)
            item.category = payload.get('category', item.category)
            item.embedding = payload.get('embedding', item.embedding)
            item.clean()
            item.save()
            return JsonResponse({'result': 'updated'})
        except ValidationError as e:
            return JsonResponse({'error': str(e)}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    elif request.method == 'DELETE':
        item.delete()
        return JsonResponse({'result': 'deleted'})
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)


@csrf_exempt
def sentence_similarity_api(request):
    """
    語意相似度檢測 API
    模擬 paraphrase-MiniLM-L6-v2 模型的語意相似度計算
    實際專案應使用 sentence-transformers 套件
    """
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
    try:
        payload = json.loads(request.body.decode())
        sentence1 = payload.get('sentence1', '').strip()
        sentence2 = payload.get('sentence2', '').strip()
        threshold = payload.get('threshold', 0.7)
        
        if not sentence1 or not sentence2:
            return JsonResponse(
                {'error': '缺少必要參數：sentence1, sentence2'},
                status=400
            )
        
        # 模擬語意相似度計算
        # 實際應使用：
        # from sentence_transformers import SentenceTransformer, util
        # model = SentenceTransformer('paraphrase-MiniLM-L6-v2')
        # embeddings = model.encode([sentence1, sentence2])
        # similarity = util.cos_sim(embeddings[0], embeddings[1]).item()
        
        # 簡化模擬：基於詞彙重疊計算相似度
        words1 = set(sentence1.lower().split())
        words2 = set(sentence2.lower().split())
        
        if not words1 or not words2:
            similarity = 0.0
        else:
            intersection = len(words1.intersection(words2))
            union = len(words1.union(words2))
            similarity = intersection / union if union > 0 else 0.0
        
        is_similar = similarity >= threshold
        
        return JsonResponse({
            'sentence1': sentence1,
            'sentence2': sentence2,
            'similarity': round(similarity, 4),
            'threshold': threshold,
            'is_similar': is_similar,
            'method': 'simulated (word overlap)',
            'note': '實際專案應使用 paraphrase-MiniLM-L6-v2 模型'
        })
        
    except json.JSONDecodeError:
        return JsonResponse(
            {'error': 'Invalid JSON'},
            status=400
        )
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

  
@csrf_exempt
def weight_config_detail(request, config_id):
    try:
        config = WeightConfiguration.objects.get(id=config_id)
    except WeightConfiguration.DoesNotExist:
        return JsonResponse({'error': 'Not found'}, status=404)

    if request.method == 'GET':
        data = {
            'id': config.id,
            'name': config.name,
            'score_a': config.score_a,
            'score_b': config.score_b,
            'score_c': config.score_c,
            'score_d': config.score_d,
        }
        return JsonResponse(data)
    elif request.method == 'PUT':
        try:
            payload = json.loads(request.body.decode())
            config.name = payload.get('name', config.name)
            config.score_a = payload.get('score_a', config.score_a)
            config.score_b = payload.get('score_b', config.score_b)
            config.score_c = payload.get('score_c', config.score_c)
            config.score_d = payload.get('score_d', config.score_d)
            config.clean()
            config.save()
            return JsonResponse({'result': 'updated'})
        except ValidationError as e:
            return JsonResponse({'error': str(e)}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    elif request.method == 'DELETE':
        config.delete()
        return JsonResponse({'result': 'deleted'})
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)
  

@csrf_exempt
def generate_specification_api(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    try:
        payload = json.loads(request.body.decode())
        
        # 驗證必填參數
        user_id = payload.get('user_id')
        order_id = payload.get('order_id')
        spec_params = payload.get('spec_params')
        
        if user_id is None or order_id is None or spec_params is None:
            return JsonResponse(
                {
                    'status': 'error',
                    'error': '缺少必要參數：user_id, order_id, spec_params'
                },
                status=400
            )
        
        # 驗證 spec_params 必須是 dict
        if not isinstance(spec_params, dict):
            return JsonResponse(
                {'status': 'error', 'error': 'spec_params 必須是 JSON 物件'},
                status=400
            )
        
        # 模擬規格產生邏輯
        result = {
            'status': 'success',
            'error': None,
            'specification': {
                'user_id': user_id,
                'order_id': order_id,
                'params': spec_params,
                'generated': True
            }
        }
        return JsonResponse(result, status=200)
        
    except json.JSONDecodeError:
        return JsonResponse(
            {'status': 'error', 'error': 'Invalid JSON'},
            status=400
        )
    except Exception as e:
        return JsonResponse(
            {'status': 'error', 'error': str(e)},
            status=500
        )
  
  
@csrf_exempt
def retry_ai_api(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
  
    try:
        payload = json.loads(request.body.decode())
        task_id = payload.get('task_id')
        
        if task_id is None:
            return JsonResponse(
                {'status': 'error', 'error': '缺少必要參數：task_id'},
                status=400
            )
        
        # 模擬任務不存在（task_id >= 100）
        if task_id >= 100:
            return JsonResponse(
                {'status': 'error', 'error': f'Task {task_id} not found'},
                status=404
            )
        
        # 模擬服務錯誤（task_id < 0）
        if task_id < 0:
            return JsonResponse(
                {'status': 'error', 'error': 'AI service internal error'},
                status=500
            )
        
        # 成功重試
        result = {
            'status': 'success',
            'error': None,
            'task_id': task_id,
            'retry_result': 'completed'
        }
        return JsonResponse(result, status=200)
        
    except json.JSONDecodeError:
        return JsonResponse(
            {'status': 'error', 'error': 'Invalid JSON'},
            status=400
        )
    except Exception as e:
        return JsonResponse(
            {'status': 'error', 'error': str(e)},
            status=500
        )


@csrf_exempt
def field_priority_list(request):
    if request.method == 'GET':
        configs = FieldPriorityConfiguration.objects.all()
        data = [
            {
                'id': c.id,
                'name': c.name,
                'field_order': c.field_order,
            } for c in configs
        ]
        return JsonResponse({'configs': data})
    elif request.method == 'POST':
        try:
            payload = json.loads(request.body.decode())
            config = FieldPriorityConfiguration(
                name=payload.get('name', ''),
                field_order=payload.get('field_order', []),
            )
            config.clean()
            config.save()
            return JsonResponse({'result': 'created', 'id': config.id})
        except ValidationError as e:
            return JsonResponse({'error': str(e)}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)


@csrf_exempt
def field_priority_detail(request, config_id):
    try:
        config = FieldPriorityConfiguration.objects.get(id=config_id)
    except FieldPriorityConfiguration.DoesNotExist:
        return JsonResponse({'error': 'Not found'}, status=404)

    if request.method == 'GET':
        data = {
            'id': config.id,
            'name': config.name,
            'field_order': config.field_order,
        }
        return JsonResponse(data)
    elif request.method == 'PUT':
        try:
            payload = json.loads(request.body.decode())
            config.name = payload.get('name', config.name)
            config.field_order = payload.get('field_order', config.field_order)
            config.clean()
            config.save()
            return JsonResponse({'result': 'updated'})
        except ValidationError as e:
            return JsonResponse({'error': str(e)}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    elif request.method == 'DELETE':
        config.delete()
        return JsonResponse({'result': 'deleted'})
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)
# Create your views here.


def index(request):
    if request.method == 'POST':
  
        name = request.POST.get('name', None)
        age = request.POST.get('age', None)
        obj = TB_1.objects.create(name=name, age=age, candy_or_cookie='0')
        obj.save()
        user_data = TB_1.objects.get(name="Adam")
        request.session['isLogin'] = True
        return render(request, './polls/index.html', {'user_data': user_data})
    return render(request, './polls/index.html')
  
  
def spec_generator(request):
  
    context = {
        'result': '結果將會顯示在這裡...',
        'project_goal': '',
        'core_features': '',
        'technical_constraints': '',
        'target_audience': '',
        'spec_background': '',
        'spec_goal': '',
        'spec_model': '',
        'spec_feature': '',
        'spec_flow': '',
        'spec_api': '',
        'spec_test': '',
        'spec_glossary': '',
        'form_error': '',
    }
  
    if request.method == 'POST':
        project_goal = request.POST.get('project_goal', '')
        core_features = request.POST.get('core_features', '')
        technical_constraints = request.POST.get('technical_constraints', '')
        target_audience = request.POST.get('target_audience', '')
    else:
        project_goal = ''
        core_features = ''
        technical_constraints = ''
        target_audience = ''

    context.update({
        'project_goal': project_goal,
        'core_features': core_features,
        'technical_constraints': technical_constraints,
        'target_audience': target_audience,
    })
    # 章節內容佔位（即使欄位未填寫也要顯示章節區塊）
    context['spec_background'] = f"背景說明：本專案旨在... (根據 {project_goal})"
    context['spec_goal'] = f"目標：{project_goal}"
    context['spec_model'] = "資料模型：尚未串接 DBML，預設空白。"
    context['spec_feature'] = f"功能規格：{core_features}"
    context['spec_flow'] = "流程圖：尚未串接 Mermaid，預設空白。"
    context['spec_api'] = f"API 規格：技術限制 {technical_constraints}"
    context['spec_test'] = "測試案例：尚未串接 Gherkin，預設空白。"
    context['spec_glossary'] = "術語表：尚未整理，預設空白。"

    if not all([
        project_goal,
        core_features,
        technical_constraints,
        target_audience
    ]):  # 條件檢查
        context['form_error'] = '請填寫所有欄位'
        return render(request, 'polls/index.html', context)
    
    try:
        # 組合 Prompt
        system_prompt = """你是一個專業的軟體規格文件生成助手。請根據用戶提供的資訊，生成一份完整的軟體規格文件。

**重要規則：**
1. 嚴格按照指定格式輸出，不要添加任何額外的說明、備註或問候語
2. 每個章節必須以 "==== 章節名稱 ====" 開頭
3. 直接輸出內容，不要用括號說明、不要用「以下是...」這類開場白
4. Mermaid 流程圖必須用完整的 ```mermaid 代碼塊包裹
5. 不要在內容中添加任何 emoji
6. 資料模型、功能規格、API 規格請使用適當的換行，每個項目或區塊之間空一行

**輸出格式：**

==== 背景說明 ====
[直接寫背景內容，分段描述，段落之間空一行]

==== 目標 ====
[直接列出目標項目，使用 "1. " "2. " 編號，每個目標換行]

==== 資料模型 ====
[直接寫 DBML 代碼，用 ```dbml 代碼塊包裹，表格之間空一行]

範例：
```dbml
Table users {
  id integer [primary key]
  username varchar
  email varchar
}

Table posts {
  id integer [primary key]
  user_id integer [ref: > users.id]
  content text
}
```

==== 功能規格 ====
[直接寫 Gherkin 格式的功能描述，每個 Feature 之間空一行，每個 Scenario 之間也要空一行]

範例：
```gherkin
Feature: 使用者登入

Scenario: 成功登入
  Given 使用者在登入頁面
  When 輸入正確的帳號密碼
  Then 應該導向首頁

Scenario: 密碼錯誤
  Given 使用者在登入頁面
  When 輸入錯誤的密碼
  Then 應該顯示錯誤訊息

Feature: 發布文章

Scenario: 成功發布
  Given 使用者已登入
  When 填寫文章內容並發布
  Then 應該顯示成功訊息
```

==== 流程圖 ====
```mermaid
graph TD
    [直接寫 Mermaid 流程圖代碼]
```

==== API 規格 ====
[直接列出 API 端點和規格，每個 API 之間空一行]

範例：
POST /api/login
- 請求：{"username": "string", "password": "string"}
- 回應：{"token": "string", "user": {...}}

GET /api/posts
- 請求：無
- 回應：[{"id": 1, "title": "string", ...}]
"""
        
        user_input = f"""
專案目標: {project_goal}
核心功能: {core_features}
技術限制: {technical_constraints}
目標使用者: {target_audience}
"""
  
        # 呼叫 Ollama Cloud API
        from polls.api_utils import call_ollama_api
        
        ai_response = call_ollama_api(
            prompt=system_prompt,
            user_input=user_input
        )
        
        # 解析 AI 回應到各個章節
        sections = {}
        current_section = None
        current_content = []
        
        for line in ai_response.split('\n'):
            if line.strip().startswith('====') and line.strip().endswith('===='):
                if current_section:
                    sections[current_section] = '\n'.join(current_content).strip()
                current_section = line.strip().replace('=', '').strip()
                current_content = []
            else:
                current_content.append(line)
        
        if current_section:
            sections[current_section] = '\n'.join(current_content).strip()
        
        # 將解析的內容填入 context
        context['spec_background'] = sections.get('背景說明', f"背景說明：本專案旨在{project_goal}")
        context['spec_goal'] = sections.get('目標', f"目標：{project_goal}")
        context['spec_model'] = sections.get('資料模型', "資料模型：尚未生成")
        context['spec_feature'] = sections.get('功能規格', f"功能規格：{core_features}")
        context['spec_flow'] = sections.get('流程圖', "流程圖：尚未生成")
        context['spec_api'] = sections.get('API 規格', f"API 規格：技術限制 {technical_constraints}")
        context['spec_test'] = "測試案例：尚未生成"
        context['spec_glossary'] = "術語表：尚未整理"
        
        context['result'] = ai_response
        
    except Exception as e:
        context['form_error'] = f"AI 服務暫時無法使用，請稍後重試 ({e})"
        # 即使失敗也保持表單數據
        context['spec_background'] = f"背景說明：本專案旨在{project_goal}"
        context['spec_goal'] = f"目標：{project_goal}"
        context['spec_model'] = "資料模型：尚未生成"
        context['spec_feature'] = f"功能規格：{core_features}"
        context['spec_flow'] = "流程圖：尚未生成"
        context['spec_api'] = f"API 規格：技術限制 {technical_constraints}"
    
    return render(request, 'polls/index.html', context)


def weight_config_page(request):
    """權重配置管理頁面"""
    return render(request, 'polls/weight_config.html')


def field_priority_page(request):
    """欄位優先順序配置頁面"""
    return render(request, 'polls/field_priority.html')


@csrf_exempt
def gpt_generate_api(request):
    """
    GPT AI 服務調用 API
    使用 GPTPromptConfiguration 中的提示詞與模型
    模擬 OpenAI/Ollama API 調用
    """
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
    try:
        payload = json.loads(request.body.decode())
        task_type = payload.get('task_type', 'custom')
        user_input = payload.get('input', '').strip()
        custom_prompt = payload.get('prompt')
        
        if not user_input:
            return JsonResponse(
                {'error': '缺少必要參數：input'},
                status=400
            )
        
        # 從資料庫獲取提示詞配置
        try:
            if custom_prompt:
                prompt_text = custom_prompt
                model_name = 'custom'
            else:
                config = GPTPromptConfiguration.objects.get(
                    task_type=task_type
                )
                prompt_text = config.prompt
                model_name = config.model
        except GPTPromptConfiguration.DoesNotExist:
            return JsonResponse(
                {'error': f'未找到 task_type={task_type} 的配置'},
                status=404
            )
        
        # 組合完整提示詞
        full_prompt = f"{prompt_text}\n\n使用者輸入：{user_input}"
        
        # 模擬 AI 生成
        # 實際應使用：
        # import openai
        # response = openai.ChatCompletion.create(
        #     model=model_name,
        #     messages=[{"role": "user", "content": full_prompt}]
        # )
        # generated_text = response.choices[0].message.content
        
        generated_text = (
            f"[模擬 AI 回應]\n"
            f"任務類型：{task_type}\n"
            f"模型：{model_name}\n\n"
            f"根據輸入「{user_input}」，AI 生成以下內容：\n\n"
            f"這是一個模擬的 AI 回應。實際專案應串接 OpenAI API 或 Ollama 等 LLM 服務。\n"
            f"提示詞：{full_prompt[:50]}..."
        )
        
        return JsonResponse({
            'task_type': task_type,
            'model': model_name,
            'input': user_input,
            'output': generated_text,
            'prompt_used': prompt_text,
            'method': 'simulated',
            'note': '實際專案應使用 OpenAI API 或 Ollama'
        })
        
    except json.JSONDecodeError:
        return JsonResponse(
            {'error': 'Invalid JSON'},
            status=400
        )
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
def llm_ideas_api(request):
    """
    AI 想法衍生 API
    接收使用者的想法，使用 Ollama API 異步生成三個不同的衍生想法
    """
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
    try:
        payload = json.loads(request.body.decode())
        idea = payload.get('idea', '').strip()
        
        if not idea:
            return JsonResponse(
                {'error': '請輸入想法'},
                status=400
            )
        
        # 呼叫 Ollama API 生成想法
        from polls.api_utils import call_ollama_api
        import concurrent.futures
        
        # 三個不同角度的 prompt
        prompts = [
            # 第一個想法:技術/工具角度
            f"""你是一個技術專家。請從「技術實現」或「工具應用」的角度，
針對以下想法提供一個具體的延伸方案。

原始想法：{idea}

要求：
1. 聚焦在技術架構、開發工具、技術棧選擇
2. 提供具體可執行的技術方案
3. 只輸出一個想法，不要編號
4. 直接開始描述，不要有「以下是...」等開場白
5. **字數限制：300字以內**""",
            
            # 第二個想法：應用場景角度
            f"""你是一個產品經理。請從「應用場景」或「使用情境」的角度，
針對以下想法提供一個具體的延伸方案。

原始想法：{idea}

要求：
1. 聚焦在實際應用場景、目標用戶、使用流程
2. 描述具體的使用情境和價值
3. 只輸出一個想法，不要編號
4. 直接開始描述，不要有「以下是...」等開場白
5. **字數限制：300字以內**""",
            
            # 第三個想法：創新/改進角度
            f"""你是一個創新顧問。請從「創新突破」或「流程改進」的角度，
針對以下想法提供一個具體的延伸方案。

原始想法：{idea}

要求：
1. 聚焦在創新點、優化方向、差異化特色
2. 提供具有創新性的改進建議
3. 只輸出一個想法，不要編號
4. 直接開始描述，不要有「以下是...」等開場白
5. **字數限制：300字以內**"""
        ]
        
        def call_api_with_retry(prompt_text):
            """呼叫 API 並處理錯誤"""
            try:
                return call_ollama_api(
                    prompt=prompt_text,
                    user_input=""
                )
            except Exception as e:
                return f"[生成失敗] {str(e)}"
        
        try:
            # 使用 ThreadPoolExecutor 異步並行呼叫三次 API
            ideas = []
            with concurrent.futures.ThreadPoolExecutor(
                max_workers=3
            ) as executor:
                # 提交三個任務
                future_to_prompt = {
                    executor.submit(call_api_with_retry, prompt): i
                    for i, prompt in enumerate(prompts)
                }
                
                # 收集結果（按順序）
                results = [None, None, None]
                for future in concurrent.futures.as_completed(
                    future_to_prompt
                ):
                    index = future_to_prompt[future]
                    try:
                        results[index] = future.result().strip()
                    except Exception as e:
                        results[index] = (
                            f"[想法 {index + 1} 生成失敗] {str(e)}"
                        )
                
                ideas = results
            
            # 過濾空結果
            ideas = [
                idea for idea in ideas
                if idea and not idea.startswith('[生成失敗')
            ]
            
            # 如果全部失敗，返回模擬回應
            if len(ideas) == 0:
                ideas = [
                    f"從技術角度：基於「{idea}」，可以考慮採用模組化架構設計，配合容器化部署提升可擴展性。",
                    f"從應用角度：將「{idea}」應用於實際業務場景，建立完整的用戶體驗流程和反饋機制。",
                    f"從創新角度：對「{idea}」進行顛覆式思考，引入 AI 自動化或數據驅動決策提升效能。"
                ]
            
            # 確保有三個想法（如果某些失敗，用預設補充）
            while len(ideas) < 3:
                ideas.append(f"延伸想法 {len(ideas) + 1}：基於「{idea}」的進一步探索...")
            
            return JsonResponse({
                'success': True,
                'ideas': ideas[:3],
                'method': 'parallel_api_calls'
            })
            
        except Exception as e:
            # 如果並行呼叫失敗，返回模擬回應
            return JsonResponse({
                'success': True,
                'ideas': [
                    f"技術方案：基於「{idea}」，可以考慮建立一個系統化的技術架構，採用微服務設計模式。",
                    f"應用場景：從「{idea}」延伸，可以針對特定用戶群體設計完整的使用流程和體驗優化。",
                    f"創新突破：將「{idea}」與新興技術結合，例如 AI、區塊鏈或物聯網，創造差異化價值。"
                ],
                'note': f'API 異步呼叫失敗 ({str(e)})，這是模擬回應'
            })
        
    except json.JSONDecodeError:
        return JsonResponse(
            {'error': 'Invalid JSON'},
            status=400
        )
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
def generate_field_api(request):
    """
    根據選中的想法為單個欄位生成內容
    """
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
    try:
        payload = json.loads(request.body.decode())
        field = payload.get('field', '')
        idea = payload.get('idea', '').strip()
        prompt = payload.get('prompt', '').strip()
        
        if not idea:
            return JsonResponse(
                {'error': '缺少想法內容'},
                status=400
            )
        
        if not prompt:
            return JsonResponse(
                {'error': '缺少 prompt'},
                status=400
            )
        
        # 呼叫 Ollama API
        from polls.api_utils import call_ollama_api
        
        try:
            content = call_ollama_api(
                prompt=prompt,
                user_input=""
            ).strip()
            
            return JsonResponse({
                'success': True,
                'field': field,
                'content': content
            })
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': f'AI 生成失敗：{str(e)}'
            }, status=500)
        
    except json.JSONDecodeError:
        return JsonResponse(
            {'error': 'Invalid JSON'},
            status=400
        )
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


# ============================================
# 進階規格產出 API (Formulation → Discovery → Clarify)
# ============================================

@csrf_exempt
def formulation_api(request):
    """
    Formulation 階段: 從原始規格文本萃取資料模型 (DBML) 和功能模型 (Gherkin)
    依照 formulation-rules.md 規則執行
    """
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
    try:
        payload = json.loads(request.body.decode())
        spec_text = payload.get('spec_text', '').strip()
        
        if not spec_text:
            return JsonResponse({'error': '缺少規格文本'}, status=400)
        
        # 載入 formulation-rules.md 規則
        formulation_rules = """
# 核心原則：無腦補或任意假設原則
嚴格遵守原始規格文本內容，如果需求中沒有明確寫出的欄位、規則、條件或行為，就不要加入。不要擅自假設、推測或補充任何需求中不存在的內容。

# 資料模型萃取規則 (DBML 格式)

## A. 識別「實體 (Entity)」
- 只萃取規格中明確提到的實體
- 實體名稱使用規格中的術語，不要自行創造
- 不要添加規格中未提及的實體

## B. 萃取實體的「屬性 (Attribute)」
- 只萃取規格中明確提到或可直接推導的屬性
- 每個屬性必須指定資料型別：int, long, float, bool, string
- 每個屬性必須有 note 說明其定義與用途
- 如果規格中有提到屬性的限制條件（如 > 0, >= 0, 必須唯一等），在 note 中明確標註
- 不要添加規格中沒有提到的「預留欄位」或「可能需要的欄位」

## C. 標註「跨屬性不變條件」
- 在實體的 Note 中條列跨屬性不變條件
- 例如：總額 = 單價 × 數量
- 只記錄規格中明確提到的約束，不要臆測

## D. 識別實體之間的「關係 (Relationship)」
- 只標註規格中明確提到的關聯關係
- 使用 DBML 的 ref 語法描述關聯
- 明確標示關聯類型（一對一、一對多、多對多）

## E. 記錄實體的整體說明
- 在 Table 的 Note 中簡述此實體的用途

# 功能模型萃取規則 (Gherkin 格式)

## A. 萃取「功能 (Feature)」
- 每個功能都是使用者與系統的請求交互點，若沒有明確交互時機則不被視為功能
- 只萃取規格中明確提到的功能，不要推測「可能需要的功能」
- 功能命名應清晰且反映使用者意圖

## B. 萃取功能的「規則 (Rule)」
- 每個前置條件 or 後置條件都必須為一條獨立的 Rule
- Rule 必須原子化，分割到不可分割為止，每一個 Rule 只驗證一件事
- 只萃取規格中明確提到的規則，不要添加「合理的驗證」
- 規則描述必須可驗證，避免使用模糊的形容詞

## C. 萃取規則的「例子 (Example)」
- 使用 Gherkin 語法 (Given-When-Then) 描述此 Example
- 如果無法從文本中找到任何例子，則在 Rule 下標記 #TODO
- 不要編造例子或假設測試情境
- 每個 Example 至少都有 "When step"，When 與該 Feature 的系統交互相關
"""
        
        # 建立 Formulation 提示詞 - 資料模型
        dbml_prompt = f"""你是一個專業的需求分析師。請依照以下規則從規格文本中萃取資料模型 (Data Model)，並輸出為 DBML 格式。

{formulation_rules}

## 原始規格文本
{spec_text}

## 輸出要求
請嚴格依照上述規則萃取資料模型，輸出為標準 DBML 格式。

**重要**: 
- 只輸出 DBML 代碼本身，不要包含任何說明文字或前綴
- 不要使用 markdown code block 標記 (```dbml)
- 直接從 Table 開始輸出
- 每個 Table 必須有 Note 說明用途
- 每個 Column 必須有 note 說明定義
- 使用 ref 語法描述實體關係

範例格式:
Table User {{
  id int [pk]
  username string [note: "使用者名稱，必須唯一"]
  email string [note: "電子郵件"]
  
  Note: "系統使用者實體"
}}

Table Order {{
  id int [pk]
  user_id int [ref: > User.id, note: "訂單所屬使用者"]
  total float [note: "訂單總額，必須 >= 0"]
  
  Note: "訂單實體。不變條件: total = sum(OrderItem.price * OrderItem.quantity)"
}}
"""
        
        # 建立 Formulation 提示詞 - 功能模型  
        gherkin_prompt = f"""你是一個專業的需求分析師。請依照以下規則從規格文本中萃取功能模型 (Functional Model)，並輸出為 Gherkin 格式。

{formulation_rules}

## 原始規格文本
{spec_text}

## 輸出要求
請嚴格依照上述規則萃取功能模型，輸出為標準 Gherkin Language 格式。

**重要**: 
- 只輸出 Gherkin 代碼本身，不要包含任何說明文字或前綴
- 不要使用 markdown code block 標記 (```gherkin)
- 使用英文 keyword (Feature, Rule, Example, Given, When, Then, And)
- 主要內容使用繁體中文
- 階層結構: Feature > Rule > Example
- 每個 Example 必須有 When step
- 如果規則沒有例子，標記 #TODO

範例格式:
Feature: 使用者註冊

  Rule: 註冊時必須提供使用者名稱
    Example: 成功註冊
      Given 系統已啟動
      When 使用者提供使用者名稱「張三」和密碼「pass123」進行註冊
      Then 系統建立新使用者帳號
      And 使用者名稱為「張三」

  Rule: 使用者名稱必須唯一
    Example: 拒絕重複的使用者名稱
      Given 系統中已存在使用者名稱「張三」
      When 使用者嘗試以使用者名稱「張三」註冊
      Then 操作失敗
      And 系統顯示錯誤訊息「使用者名稱已存在」
"""
        
        # 呼叫 Ollama API 生成 DBML
        from polls.api_utils import call_ollama_api
        
        try:
            dbml_content = call_ollama_api(
                prompt=dbml_prompt,
                user_input=""
            ).strip()
            
            # 移除可能的 markdown code block 標記
            if dbml_content.startswith('```'):
                lines = dbml_content.split('\n')
                # 移除第一行和最後一行
                if lines[-1].strip() == '```':
                    dbml_content = '\n'.join(lines[1:-1])
                else:
                    dbml_content = '\n'.join(lines[1:])
            
            # 呼叫 Ollama API 生成 Gherkin
            gherkin_content = call_ollama_api(
                prompt=gherkin_prompt,
                user_input=""
            ).strip()
            
            # 移除可能的 markdown code block 標記
            if gherkin_content.startswith('```'):
                lines = gherkin_content.split('\n')
                if lines[-1].strip() == '```':
                    gherkin_content = '\n'.join(lines[1:-1])
                else:
                    gherkin_content = '\n'.join(lines[1:])
            
            return JsonResponse({
                'success': True,
                'dbml': dbml_content,
                'gherkin': gherkin_content
            })
            
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': f'Formulation 執行失敗：{str(e)}'
            }, status=500)
        
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
def discovery_api(request):
    """
    Discovery 階段: 掃描 DBML 和 Gherkin 規格,識別歧義與遺漏
    執行 A1-A6 (資料模型), B1-B5 (功能模型) 檢查清單
    """
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
    try:
        payload = json.loads(request.body.decode())
        dbml_content = payload.get('dbml', '').strip()
        gherkin_content = payload.get('gherkin', '').strip()
        
        if not dbml_content or not gherkin_content:
            return JsonResponse({'error': '缺少 DBML 或 Gherkin 內容'}, status=400)
        
        # 建立 Discovery 提示詞
        discovery_prompt = f"""你是一個專業的規格品質檢查專家。請依照以下檢查清單掃描規格,識別需要釐清的項目。

## 檢查清單

### A. 資料模型檢查 (DBML)

A1. 實體完整性
- 所有核心業務概念是否都已建模為實體？
- 實體命名是否清晰且無歧義？

A2. 屬性定義
- 每個屬性是否都有明確的資料型別？
- 每個屬性是否都有充足的定義說明？

A3. 屬性值邊界條件
- 數值屬性的範圍限制是否明確（>=、<=）？
- 特殊值處理是否已定義（空值、零、負值）？

A4. 跨屬性不變條件
- 屬性間的計算關係是否明確？

A5. 關係與唯一性
- 實體間的關聯關係是否完整？
- 主鍵與唯一性規則是否明確？

A6. 生命週期與狀態
- 具有狀態的實體是否定義了所有可能狀態？
- 狀態轉換規則是否完整？

### B. 功能模型檢查 (Gherkin)

B1. 功能識別
- 所有使用者與系統的交互點是否都已識別為功能？
- 功能命名是否清晰？

B2. 規則完整性
- 每個功能是否至少有一條規則？
- 規則是否已原子化？
- 前置條件和後置條件是否完整？

B3. 例子覆蓋度
- 每條規則是否至少有一個 Example？
- 缺少 Example 的規則是否已標記 #TODO？

B4. 邊界條件覆蓋
- 是否涵蓋臨界值案例（剛好達標、差一點、超過）？
- 不同值域的資料分類是否都有對應 Example？

B5. 錯誤與異常處理
- 前置條件失敗時的行為是否明確？
- 異常情況是否都有對應的規則與 Example？

## 當前規格

### DBML 資料模型
```dbml
{dbml_content}
```

### Gherkin 功能模型
```gherkin
{gherkin_content}
```

## 輸出要求

請以 JSON 格式輸出釐清項目清單。每個釐清項目包含:
- id: 編號
- priority: 優先級 (High/Medium/Low)
- location: 定位 (ERM: 實體.屬性 或 Feature: 功能名 → Rule: 規則)
- question: 釐清問題
- options: 選項陣列,每個選項包含 key (A/B/C/Short) 和 text

**重要**: 
- 只輸出 JSON 陣列,不要包含任何說明文字
- 不要使用 markdown code block 標記
- 直接從 [ 開始輸出
- 如果沒有發現需要釐清的項目,返回空陣列 []
- 優先識別 High 優先級的問題(影響核心功能或資料建模)

範例格式:
[
  {{
    "id": 1,
    "priority": "High",
    "location": "ERM: User 實體 → email 屬性",
    "question": "email 是否必須唯一？",
    "options": [
      {{"key": "A", "text": "是，email 必須唯一"}},
      {{"key": "B", "text": "否，允許重複 email"}}
    ]
  }}
]
"""
        
        # 呼叫 Ollama API
        from polls.api_utils import call_ollama_api
        
        try:
            result = call_ollama_api(
                prompt=discovery_prompt,
                user_input=""
            ).strip()
            
            # 移除可能的 markdown code block 標記
            if result.startswith('```'):
                lines = result.split('\n')
                if lines[-1].strip() == '```':
                    result = '\n'.join(lines[1:-1])
                else:
                    result = '\n'.join(lines[1:])
            
            # 解析 JSON
            try:
                clarification_items = json.loads(result)
                
                # 計算統計
                total = len(clarification_items)
                high = len([item for item in clarification_items if item.get('priority') == 'High'])
                medium = len([item for item in clarification_items if item.get('priority') == 'Medium'])
                low = len([item for item in clarification_items if item.get('priority') == 'Low'])
                
                return JsonResponse({
                    'success': True,
                    'items': clarification_items,
                    'statistics': {
                        'total': total,
                        'high': high,
                        'medium': medium,
                        'low': low
                    }
                })
                
            except json.JSONDecodeError as je:
                return JsonResponse({
                    'success': False,
                    'error': f'AI 返回的內容無法解析為 JSON: {str(je)}\n原始內容: {result[:200]}'
                }, status=500)
            
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': f'Discovery 執行失敗：{str(e)}'
            }, status=500)
        
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
def generate_complete_result_api(request):
    """
    生成完整規格結果的 API
    輸入: DBML 和 Gherkin 內容
    輸出: 背景說明、專案目標、流程圖、API 規格
    """
    if request.method != 'POST':
        return JsonResponse({'error': 'Only POST method is allowed'}, status=405)
    
    try:
        payload = json.loads(request.body)
        
        # 取得輸入參數
        dbml_content = payload.get('dbml', '').strip()
        gherkin_content = payload.get('gherkin', '').strip()
        
        # 參數驗證
        if not dbml_content or not gherkin_content:
            return JsonResponse({
                'success': False,
                'error': '缺少必要參數：dbml 和 gherkin 都是必填項'
            }, status=400)
        
        try:
            # 導入 API 工具
            from polls.api_utils import call_ollama_api
            
            # 1. 生成背景說明
            background_prompt = f"""你是一個專業的技術文件撰寫專家。請根據以下規格生成簡潔的背景說明（2-3 句話）。

當前規格:
### DBML 資料模型
```dbml
{dbml_content}
```

### Gherkin 功能模型
```gherkin
{gherkin_content}
```

請直接輸出背景說明內容，不要包含任何標題或 markdown 標記。"""

            background = call_ollama_api(prompt=background_prompt, user_input="")
            background = background.strip()
            
            # 2. 生成專案目標
            goals_prompt = f"""你是一個專業的產品經理。請根據以下規格列出 3-5 個核心專案目標。

當前規格:
### DBML 資料模型
```dbml
{dbml_content}
```

### Gherkin 功能模型
```gherkin
{gherkin_content}
```

請以有編號的清單格式輸出（例如：1. ... 2. ...），不要包含任何標題。"""

            goals = call_ollama_api(prompt=goals_prompt, user_input="")
            goals = goals.strip()
            
            # 3. 生成流程圖 (Mermaid)
            flowchart_prompt = f"""你是一個流程圖設計專家。請根據以下規格生成 Mermaid 流程圖代碼。

當前規格:
### DBML 資料模型
```dbml
{dbml_content}
```

### Gherkin 功能模型
```gherkin
{gherkin_content}
```

**重要規則**：
1. 只輸出 Mermaid 語法，不要包含 ```mermaid 標記
2. 直接從 graph 或 flowchart 開始
3. 節點標籤使用英文或簡短中文（不超過 10 個字）
4. 箭頭標籤（條件分支）請使用英文，例如：
   - 使用 -->|Yes| 而不是 -->|是|
   - 使用 -->|No| 而不是 -->|否|
   - 使用 -->|Success| 而不是 -->|成功|
5. 避免使用特殊符號：/ \\ : " ' 等
6. 節點 ID 使用簡單的字母數字組合（A, B, C 或 step1, step2）
7. 使用基本圖形：方括號表示方形、圓括號表示圓角、大括號表示菱形

**範例格式**：
graph TD
    A[Start] --> B{{Check Auth}}
    B -->|Yes| C[Load Data]
    B -->|No| D[Show Login]
    C --> E[Display]

請只輸出符合以上規則的 Mermaid 代碼。"""

            flowchart = call_ollama_api(prompt=flowchart_prompt, user_input="")
            flowchart = flowchart.strip()
            
            # 移除可能的 code block 標記
            if flowchart.startswith('```'):
                lines = flowchart.split('\n')
                flowchart = '\n'.join(lines[1:-1] if lines[-1].strip() == '```' else lines[1:])
                flowchart = flowchart.strip()
            
            # 4. 生成 API 規格
            api_spec_prompt = f"""你是一個 API 設計專家。請根據以下規格生成 RESTful API 規格文件。

當前規格:
### DBML 資料模型
```dbml
{dbml_content}
```

### Gherkin 功能模型
```gherkin
{gherkin_content}
```

請以 Markdown 格式輸出，包含：
- 端點路徑和方法
- 描述
- 請求參數
- 回應格式
- 狀態碼

不要包含 # API 規格 這樣的大標題。"""

            api_spec = call_ollama_api(prompt=api_spec_prompt, user_input="")
            api_spec = api_spec.strip()
            
            # 返回完整結果
            return JsonResponse({
                'success': True,
                'background': background,
                'goals': goals,
                'flowchart': flowchart,
                'api_spec': api_spec
            })
            
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': f'生成完整結果失敗：{str(e)}'
            }, status=500)
        
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

