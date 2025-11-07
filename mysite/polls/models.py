from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.hashers import make_password


# User 核心實體
class User(models.Model):
    username = models.CharField(
        max_length=64, unique=True, help_text="使用者名稱"
    )
    email = models.EmailField(
        max_length=128, unique=True, help_text="電子郵件"
    )
    password = models.CharField(max_length=128, help_text="密碼 hash")
    created_at = models.DateTimeField(auto_now_add=True, help_text="建立時間")

    def clean(self):
        if not self.username or not isinstance(self.username, str):
            raise ValidationError('username 必須為非空字串')
        if not self.email or not isinstance(self.email, str):
            raise ValidationError('email 必須為非空字串')
        if not self.password or not isinstance(self.password, str):
            raise ValidationError('password 必須為非空字串')

    def save(self, *args, **kwargs):
        # 如果密碼未 hash，則進行 hash
        if self.password and not self.password.startswith('pbkdf2_'):
            self.password = make_password(self.password)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.username} ({self.email})"

    class Meta:
        verbose_name_plural = "使用者"


# Order 核心實體
class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', '待處理'),
        ('processing', '處理中'),
        ('completed', '已完成'),
        ('cancelled', '已取消'),
    ]

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, help_text="下單者"
    )
    product_name = models.CharField(max_length=128, help_text="商品名稱")
    amount = models.IntegerField(help_text="數量")
    status = models.CharField(
        max_length=32, choices=STATUS_CHOICES, default='pending',
        help_text="訂單狀態"
    )
    created_at = models.DateTimeField(auto_now_add=True, help_text="訂單建立時間")

    def clean(self):
        if not self.product_name or not isinstance(self.product_name, str):
            raise ValidationError('product_name 必須為非空字串')
        if self.amount is None or self.amount <= 0:
            raise ValidationError('amount 必須大於 0')

    def __str__(self):
        return f"Order #{self.id}: {self.product_name} x{self.amount}"

    class Meta:
        verbose_name_plural = "訂單"
        ordering = ['-created_at']


class WeightConfiguration(models.Model):
    name = models.CharField(max_length=50, unique=True)
    score_a = models.FloatField(default=0.25)
    score_b = models.FloatField(default=0.25)
    score_c = models.FloatField(default=0.25)
    score_d = models.FloatField(default=0.25)
    updated_at = models.DateTimeField(auto_now=True)

    def clean(self):
        total = self.score_a + self.score_b + self.score_c + self.score_d
        if not (0 <= self.score_a <= 1 and
                0 <= self.score_b <= 1 and
                0 <= self.score_c <= 1 and
                0 <= self.score_d <= 1):
            raise ValidationError('所有分數必須介於 0~1 之間')
        if abs(total - 1.0) > 1e-6:
            raise ValidationError('分數總和必須等於 1.0')

    def __str__(self):
        return (
            f"{self.name}: A={self.score_a}, B={self.score_b}, "
            f"C={self.score_c}, D={self.score_d}"
        )


class Ticket(models.Model):

    title = models.CharField(max_length=100)
    desc = models.TextField(blank=True)
    value_a = models.FloatField(default=0)
    value_b = models.FloatField(default=0)
    value_c = models.FloatField(default=0)
    value_d = models.FloatField(default=0)
    score = models.FloatField(default=0)
    weight_config = models.ForeignKey(
        WeightConfiguration,
        on_delete=models.SET_NULL,
        null=True
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def calculate_score(self):
        if not self.weight_config:
            return None
        self.score = (
            self.value_a * self.weight_config.score_a +
            self.value_b * self.weight_config.score_b +
            self.value_c * self.weight_config.score_c +
            self.value_d * self.weight_config.score_d
        )
        return self.score

    def save(self, *args, **kwargs):
        self.calculate_score()
        super().save(*args, **kwargs)


class TB_1(models.Model):
    name = models.CharField(max_length=64)
    age = models.IntegerField()
    MY_CHOICES = [
        ('0', '糖果'),
        ('1', '餅乾'),
        ]
    candy_or_cookie = models.CharField(
            max_length=1,
            choices=MY_CHOICES,
            default='0',
        )
    _time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-_time']
        verbose_name = "用戶資料庫"
        verbose_name_plural = "用戶資料庫"


class FieldPriorityConfiguration(models.Model):
    name = models.CharField(max_length=100, unique=True)
    field_order = models.JSONField(default=list)
    updated_at = models.DateTimeField(auto_now=True)

    def clean(self):
        if not isinstance(self.field_order, list):
            raise ValidationError('field_order 必須是 JSON 陣列格式')
        if not all(isinstance(f, str) for f in self.field_order):
            raise ValidationError('field_order 每個元素必須是字串')

    def __str__(self):
        return f"{self.name}: {self.field_order}"

    class Meta:
        verbose_name_plural = "欄位優先順序配置"


# 語句資料庫模型
class SentenceDatabase(models.Model):
    user = models.CharField(max_length=64, help_text="用戶標識")
    sentence = models.TextField(help_text="語句內容")
    category = models.CharField(max_length=64, blank=True, help_text="分類")
    embedding = models.JSONField(default=list, blank=True, help_text="語意向量")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def clean(self):
        if not isinstance(self.embedding, list):
            raise ValidationError('embedding 必須是 JSON 陣列格式')
        if not all(isinstance(x, (float, int)) for x in self.embedding):
            raise ValidationError('embedding 必須為數值陣列')

    def __str__(self):
        return f"{self.user}: {self.sentence[:20]}... ({self.category})"

    class Meta:
        verbose_name_plural = "語句資料庫"


# GPT提示詞配置模型
class GPTPromptConfiguration(models.Model):
    TASK_CHOICES = [
        ('classification', '分類'),
        ('generation', '生成'),
        ('summarization', '摘要'),
        ('custom', '自訂'),
    ]
    task_type = models.CharField(
        max_length=32, choices=TASK_CHOICES, default='custom'
    )
    prompt = models.TextField(help_text="提示詞內容")
    model = models.CharField(
        max_length=64, default='gpt-3.5-turbo', help_text="模型名稱"
    )
    updated_at = models.DateTimeField(auto_now=True)

    def clean(self):
        if not self.prompt or not isinstance(self.prompt, str):
            raise ValidationError('prompt 必須為非空字串')
        if not self.model or not isinstance(self.model, str):
            raise ValidationError('model 必須為非空字串')

    def __str__(self):
        return f"{self.task_type}: {self.model}"

    class Meta:
        verbose_name_plural = "GPT提示詞配置"


# 雲端同步路徑配置模型
class SyncPathConfiguration(models.Model):
    name = models.CharField(max_length=100, unique=True, help_text="路徑名稱")
    path = models.CharField(max_length=256, unique=True, help_text="同步路徑")
    updated_at = models.DateTimeField(auto_now=True)

    def clean(self):
        import os
        if not self.name or not isinstance(self.name, str):
            raise ValidationError('name 必須為非空字串')
        if not self.path or not isinstance(self.path, str):
            raise ValidationError('path 必須為非空字串')
        # 路徑可寫入驗證
        if not os.path.exists(self.path):
            raise ValidationError('路徑不存在')
        if not os.access(self.path, os.W_OK):
            raise ValidationError('路徑不可寫入')

    def __str__(self):
        return f"{self.name}: {self.path}"

    class Meta:
        verbose_name_plural = "雲端同步路徑配置"


# 聊天會話管理模型
class ChatSession(models.Model):
    session_id = models.CharField(
        max_length=64, unique=True, primary_key=True, help_text="會話ID"
    )
    title = models.CharField(max_length=200, help_text="會話標題")
    messages = models.JSONField(default=list, help_text="對話訊息陣列")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def clean(self):
        if not isinstance(self.messages, list):
            raise ValidationError('messages 必須是 JSON 陣列格式')
        for msg in self.messages:
            if not isinstance(msg, dict):
                raise ValidationError('每個訊息必須是 JSON 物件')
            if 'role' not in msg or 'content' not in msg:
                raise ValidationError(
                    '每個訊息必須包含 role 與 content 欄位'
                )
            if msg['role'] not in ['user', 'assistant', 'system']:
                raise ValidationError(
                    'role 必須是 user, assistant 或 system'
                )

    def __str__(self):
        return f"{self.session_id}: {self.title}"

    class Meta:
        verbose_name_plural = "聊天會話"


# AI分類記憶模型
class CategoryMemory(models.Model):
    configuration_item = models.CharField(
        max_length=200, help_text="配置項名稱"
    )
    category = models.CharField(max_length=100, help_text="AI生成的分類名稱")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def clean(self):
        if not self.configuration_item or not isinstance(
            self.configuration_item, str
        ):
            raise ValidationError('configuration_item 必須為非空字串')
        if not self.category or not isinstance(self.category, str):
            raise ValidationError('category 必須為非空字串')

    def __str__(self):
        return f"{self.configuration_item}: {self.category}"

    class Meta:
        verbose_name_plural = "AI分類記憶"
        unique_together = [['configuration_item', 'category']]


# 上傳檔案記錄模型
class UploadedFile(models.Model):
    filename = models.CharField(max_length=255, help_text="原始檔案名稱")
    stored_filename = models.CharField(
        max_length=255, help_text="儲存檔案名稱"
    )
    upload_time = models.DateTimeField(
        auto_now_add=True, help_text="上傳時間"
    )
    file_size = models.IntegerField(help_text="檔案大小(bytes)")
    file_path = models.CharField(
        max_length=255, default='uploads/', help_text="檔案儲存路徑"
    )

    def clean(self):
        MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MiB
        if not self.filename.endswith('.xlsx'):
            raise ValidationError('僅接受 .xlsx 格式檔案')
        if self.file_size > MAX_FILE_SIZE:
            raise ValidationError(
                f'檔案大小不可超過 {MAX_FILE_SIZE} bytes (10MiB)'
            )
        if not self.file_path or not isinstance(self.file_path, str):
            raise ValidationError('file_path 必須為非空字串')

    def __str__(self):
        return f"{self.filename} ({self.file_size} bytes)"

    class Meta:
        verbose_name_plural = "上傳檔案記錄"
