from django import forms
from .models import ContactMessage, Wilaya


class ContactForm(forms.ModelForm):
    """نموذج التواصل"""

    SUBJECT_CHOICES = [
        ('', 'اختر الموضوع'),
        ('inquiry', 'استفسار عام'),
        ('product', 'استفسار عن منتج'),
        ('order', 'طلب منتج'),
        ('technical', 'دعم فني'),
        ('partnership', 'شراكة'),
        ('other', 'أخرى'),
    ]

    full_name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control-custom',
            'placeholder': 'أدخل اسمك الكامل'
        }),
        label='الاسم الكامل',
        required=True
    )

    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control-custom',
            'placeholder': 'example@email.com'
        }),
        label='البريد الإلكتروني',
        required=True
    )

    phone = forms.CharField(
        max_length=20,
        widget=forms.TextInput(attrs={
            'class': 'form-control-custom',
            'placeholder': '+966 50 000 0000'
        }),
        label='رقم الهاتف',
        required=False
    )

    subject = forms.ChoiceField(
        choices=SUBJECT_CHOICES,
        widget=forms.Select(attrs={
            'class': 'form-control-custom'
        }),
        label='الموضوع',
        required=True
    )

    product_reference = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control-custom',
            'placeholder': 'أدخل رقم المنتج أو المرجع إن وجد'
        }),
        label='المنتج المطلوب (اختياري)',
        required=False
    )

    message = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control-custom',
            'placeholder': 'اكتب رسالتك هنا...',
            'rows': 5
        }),
        label='الرسالة',
        required=True
    )

    class Meta:
        model = ContactMessage
        fields = [
            'full_name',
            'email',
            'phone',
            'subject',
            'product_reference',
            'message'
        ]