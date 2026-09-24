# ⚡ ElecCatalog - Electronic Components Catalog

موقع كتالوج المكونات الإلكترونية الكامل مبني بـ Django.

## 📁 هيكل المشروع

```
eleccatalog_project/
├── manage.py
├── requirements.txt
├── eleccatalog_project/          # إعدادات المشروع
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── catalog/                       # تطبيق الكتالوج
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── models.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── templates/                     # قوالب HTML
│   ├── base.html
│   ├── home.html
│   ├── categories.html
│   ├── products.html
│   ├── product_detail.html
│   ├── about.html
│   ├── contact.html
│   └── search_results.html
├── static/                        # ملفات CSS/JS/Images
└── media/                         # ملفات المستخدمين (صور، PDF)
```

## 🚀 طريقة التشغيل

### 1. تثبيت المتطلبات
```bash
pip install -r requirements.txt
```

### 2. تشغيل الترحيلات
```bash
python manage.py makemigrations
python manage.py migrate
```

### 3. إنشاء Superuser
```bash
python manage.py createsuperuser
```

### 4. تشغيل الخادم
```bash
python manage.py runserver
```

### 5. فتح الموقع
- الموقع: http://127.0.0.1:8000/
- لوحة الإدارة: http://127.0.0.1:8000/admin/

## 📋 المميزات

- ✅ تصميم احترافي داكن (Dark Theme)
- ✅ Responsive بالكامل
- ✅ دعم اللغة العربية (RTL)
- ✅ Bootstrap 5
- ✅ بحث متقدم
- ✅ تصفية المنتجات
- ✅ Pagination
- ✅ لوحة إدارة كاملة
- ✅ نموذج تواصل
- ✅ Datasheet PDF
- ✅ Pinout Diagram

## 🔧 النماذج (Models)

| النموذج | الوصف |
|---------|-------|
| Category | تصنيفات المكونات |
| Product | المنتجات / المكونات |
| Specification | المواصفات الفنية |
| ContactMessage | رسائل التواصل |

## 🌐 الروابط

| الرابط | الوصف |
|--------|-------|
| `/` | الرئيسية |
| `/categories/` | التصنيفات |
| `/category/<slug>/` | منتجات التصنيف |
| `/products/` | جميع المنتجات |
| `/product/<slug>/` | تفاصيل المنتج |
| `/about/` | عن الشركة |
| `/contact/` | التواصل |
| `/search/?q=...` | البحث |
| `/admin/` | لوحة الإدارة |

## ⚠️ ملاحظات الأمان

قبل النشر في Production:
1. غيّر `SECRET_KEY` في `settings.py`
2. ضبط `DEBUG = False`
3. أضف domain في `ALLOWED_HOSTS`
4. استخدم قاعدة بيانات PostgreSQL
5. اضبط إعدادات Static/Media بشكل صحيح
