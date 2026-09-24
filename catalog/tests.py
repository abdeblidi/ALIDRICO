from django.test import TestCase, Client
from django.urls import reverse
from .models import Category, Product, ContactMessage


class CategoryModelTest(TestCase):
    """اختبارات نموذج التصنيف"""

    def setUp(self):
        self.category = Category.objects.create(
            name='Diodes',
            slug='diodes',
            description='تصنيف الديودات'
        )

    def test_category_creation(self):
        self.assertEqual(self.category.name, 'Diodes')
        self.assertEqual(self.category.slug, 'diodes')

    def test_category_str(self):
        self.assertEqual(str(self.category), 'Diodes')

    def test_category_absolute_url(self):
        self.assertEqual(
            self.category.get_absolute_url(),
            reverse('catalog:category_products', kwargs={'slug': 'diodes'})
        )


class ProductModelTest(TestCase):
    """اختبارات نموذج المنتج"""

    def setUp(self):
        self.category = Category.objects.create(name='Diodes', slug='diodes')
        self.product = Product.objects.create(
            name='1N4007 Diode',
            part_number='1N4007',
            category=self.category,
            description='ديود عام الاستخدام',
            short_description='ديود 1000V 1A'
        )

    def test_product_creation(self):
        self.assertEqual(self.product.name, '1N4007 Diode')
        self.assertEqual(self.product.part_number, '1N4007')

    def test_product_str(self):
        self.assertEqual(str(self.product), '1N4007 - 1N4007 Diode')

    def test_product_absolute_url(self):
        self.assertEqual(
            self.product.get_absolute_url(),
            reverse('catalog:product_detail', kwargs={'slug': self.product.slug})
        )


class ViewTest(TestCase):
    """اختبارات العروض"""

    def setUp(self):
        self.client = Client()
        self.category = Category.objects.create(name='Diodes', slug='diodes')
        self.product = Product.objects.create(
            name='1N4007 Diode',
            part_number='1N4007',
            category=self.category,
            description='Test description',
            short_description='Test short'
        )

    def test_home_view(self):
        response = self.client.get(reverse('catalog:home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')

    def test_categories_view(self):
        response = self.client.get(reverse('catalog:categories'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'categories.html')

    def test_products_view(self):
        response = self.client.get(reverse('catalog:products'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'products.html')

    def test_product_detail_view(self):
        response = self.client.get(
            reverse('catalog:product_detail', kwargs={'slug': self.product.slug})
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'product_detail.html')

    def test_about_view(self):
        response = self.client.get(reverse('catalog:about'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'about.html')

    def test_contact_view_get(self):
        response = self.client.get(reverse('catalog:contact'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'contact.html')

    def test_contact_view_post(self):
        data = {
            'full_name': 'Test User',
            'email': 'test@example.com',
            'phone': '+966500000000',
            'subject': 'inquiry',
            'message': 'Test message'
        }
        response = self.client.post(reverse('catalog:contact'), data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(ContactMessage.objects.count(), 1)

    def test_search_view(self):
        response = self.client.get(reverse('catalog:search'), {'q': '1N4007'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'search_results.html')
