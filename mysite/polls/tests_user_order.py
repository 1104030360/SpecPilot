import json
from django.test import TestCase, Client
from django.urls import reverse
from .models import User, Order


class UserAPITest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_create_valid_user(self):
        url = reverse('user-list')
        data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'password123'
        }
        response = self.client.post(
            url,
            data=json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 201)
        result = response.json()
        self.assertIn('id', result)
        
        # 驗證資料庫
        user = User.objects.get(id=result['id'])
        self.assertEqual(user.username, 'testuser')
        self.assertEqual(user.email, 'test@example.com')
        # 密碼應該被 hash
        self.assertTrue(user.password.startswith('pbkdf2_'))

    def test_create_user_empty_username(self):
        url = reverse('user-list')
        data = {
            'username': '',
            'email': 'test@example.com',
            'password': 'password123'
        }
        response = self.client.post(
            url,
            data=json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)
        result = response.json()
        self.assertIn('error', result)

    def test_get_user_list(self):
        User.objects.create(
            username='user1',
            email='user1@example.com',
            password='password1'
        )
        User.objects.create(
            username='user2',
            email='user2@example.com',
            password='password2'
        )
        
        url = reverse('user-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        result = response.json()
        self.assertIn('users', result)
        self.assertEqual(len(result['users']), 2)

    def test_get_user_detail(self):
        user = User.objects.create(
            username='testuser',
            email='test@example.com',
            password='password123'
        )
        
        url = reverse('user-detail', args=[user.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        result = response.json()
        self.assertEqual(result['username'], 'testuser')
        self.assertEqual(result['email'], 'test@example.com')

    def test_update_user(self):
        user = User.objects.create(
            username='testuser',
            email='test@example.com',
            password='password123'
        )
        
        url = reverse('user-detail', args=[user.id])
        data = {
            'username': 'updateduser',
            'email': 'updated@example.com'
        }
        response = self.client.put(
            url,
            data=json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        
        # 驗證資料庫
        user.refresh_from_db()
        self.assertEqual(user.username, 'updateduser')
        self.assertEqual(user.email, 'updated@example.com')

    def test_delete_user(self):
        user = User.objects.create(
            username='testuser',
            email='test@example.com',
            password='password123'
        )
        
        url = reverse('user-detail', args=[user.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)
        
        # 驗證資料庫
        self.assertEqual(User.objects.filter(id=user.id).count(), 0)


class OrderAPITest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create(
            username='testuser',
            email='test@example.com',
            password='password123'
        )

    def test_create_valid_order(self):
        url = reverse('order-list')
        data = {
            'user_id': self.user.id,
            'product_name': 'Product A',
            'amount': 5,
            'status': 'pending'
        }
        response = self.client.post(
            url,
            data=json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 201)
        result = response.json()
        self.assertIn('id', result)
        
        # 驗證資料庫
        order = Order.objects.get(id=result['id'])
        self.assertEqual(order.product_name, 'Product A')
        self.assertEqual(order.amount, 5)
        self.assertEqual(order.user.id, self.user.id)

    def test_create_order_missing_user_id(self):
        url = reverse('order-list')
        data = {
            'product_name': 'Product A',
            'amount': 5
        }
        response = self.client.post(
            url,
            data=json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)

    def test_create_order_invalid_user(self):
        url = reverse('order-list')
        data = {
            'user_id': 99999,
            'product_name': 'Product A',
            'amount': 5
        }
        response = self.client.post(
            url,
            data=json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 404)

    def test_create_order_invalid_amount(self):
        url = reverse('order-list')
        data = {
            'user_id': self.user.id,
            'product_name': 'Product A',
            'amount': 0
        }
        response = self.client.post(
            url,
            data=json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)

    def test_get_order_list(self):
        Order.objects.create(
            user=self.user,
            product_name='Product A',
            amount=5
        )
        Order.objects.create(
            user=self.user,
            product_name='Product B',
            amount=3
        )
        
        url = reverse('order-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        result = response.json()
        self.assertIn('orders', result)
        self.assertEqual(len(result['orders']), 2)

    def test_get_order_detail(self):
        order = Order.objects.create(
            user=self.user,
            product_name='Product A',
            amount=5
        )
        
        url = reverse('order-detail', args=[order.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        result = response.json()
        self.assertEqual(result['product_name'], 'Product A')
        self.assertEqual(result['amount'], 5)

    def test_update_order(self):
        order = Order.objects.create(
            user=self.user,
            product_name='Product A',
            amount=5
        )
        
        url = reverse('order-detail', args=[order.id])
        data = {
            'product_name': 'Product B',
            'amount': 10,
            'status': 'completed'
        }
        response = self.client.put(
            url,
            data=json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        
        # 驗證資料庫
        order.refresh_from_db()
        self.assertEqual(order.product_name, 'Product B')
        self.assertEqual(order.amount, 10)
        self.assertEqual(order.status, 'completed')

    def test_delete_order(self):
        order = Order.objects.create(
            user=self.user,
            product_name='Product A',
            amount=5
        )
        
        url = reverse('order-detail', args=[order.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)
        
        # 驗證資料庫
        self.assertEqual(Order.objects.filter(id=order.id).count(), 0)
