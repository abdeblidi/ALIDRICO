from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Count
from django.db import transaction
from django.urls import reverse
from decimal import Decimal
import json

from .models import (
    Category,
    Subcategory,
    Product,
    ContactMessage,
    Wilaya,
    CartOrder,
    CartOrderItem,
)

def home(request):
    """الصفحة الرئيسية"""

    featured_categories = Category.objects.filter(
        is_active=True,is_featured=True
    )

    featured_products = Product.objects.filter(
        is_active=True,
        is_featured=True
    )[:8]

    context = {
        'featured_categories': featured_categories,
        'featured_products': featured_products,
    }

    return render(
        request,
        'home.html',
        context
    )


def categories_view(request):
    """صفحة التصنيفات"""

    categories = Category.objects.filter(
        is_active=True
    )
    paginator = Paginator(
        categories,
        20
    )  
    categories_page = paginator.get_page(
        request.GET.get('page')
    )


    context = {
        'categories': categories_page ,
    }

    return render(
        request,
        'categories.html',
        context
    )


def category_products(request, slug):
    """منتجات تصنيف معين مع فلترة التصنيف الفرعي."""

    category = get_object_or_404(
        Category,
        slug=slug,
        is_active=True
    )

    products_list = Product.objects.filter(
        category=category,
        is_active=True
    )

    all_categories = Category.objects.filter(
        is_active=True
    )

    subcategories = Subcategory.objects.filter(
        category=category,
        is_active=True
    )

    # =========================
    # Subcategory Filter
    # =========================

    selected_subcategory = request.GET.get(
        'subcategory',
        ''
    )

    if selected_subcategory:
        products_list = products_list.filter(
            subcategory__slug=selected_subcategory,
            subcategory__category=category,
            subcategory__is_active=True
        )

    # =========================
    # Subcategories for dynamic filter
    # =========================

    all_subcategories = Subcategory.objects.filter(
        is_active=True
    ).select_related('category').annotate(
        active_product_count=Count(
            'products',
            filter=Q(products__is_active=True)
        )
    ).order_by(
        'category__name',
        'name'
    )

    subcategories_by_category = {}

    for subcategory in all_subcategories:
        category_slug = subcategory.category.slug

        subcategories_by_category.setdefault(
            category_slug,
            []
        ).append({
            'slug': subcategory.slug,
            'name': subcategory.name,
            'count': subcategory.active_product_count,
        })

    # =========================
    # Package Filter
    # =========================

    selected_packages = []

    # =========================
    # Sorting
    # =========================

    sort = request.GET.get(
        'sort',
        '-created_at'
    )

    allowed_sorts = {
        '-created_at': '-created_at',
        'created_at': 'created_at',
        'name': 'name',
        '-name': '-name',
        'price': 'price',
        '-price': '-price',
    }

    sort_field = allowed_sorts.get(
        sort,
        '-created_at'
    )

    products_list = products_list.order_by(
        sort_field
    )

    # =========================
    # Pagination
    # =========================

    paginator = Paginator(
        products_list,
        20
    )

    page_number = request.GET.get(
        'page'
    )

    products = paginator.get_page(
        page_number
    )

    # =========================
    # Query String
    # =========================

    query_params = request.GET.copy()

    if 'page' in query_params:
        query_params.pop('page')

    query_string = query_params.urlencode()

    # =========================
    # Context
    # =========================

    context = {
        'products': products,

        'current_category': category,

        'all_categories': all_categories,

        'subcategories': subcategories,

        'subcategories_by_category': {
            category.slug: [
                {
                    'slug': subcategory.slug,
                    'name': subcategory.name,
                    'count': subcategory.products.filter(
                        is_active=True
                    ).count(),
                }
                for subcategory in subcategories
            ]
        },

        'selected_categories': [
            category.slug
        ],

        'selected_subcategory': selected_subcategory,

        'subcategories_by_category': subcategories_by_category,

        'selected_packages': selected_packages,

        'current_sort': sort,

        'package_types': [],

        'query_string': query_string,
    }

    return render(
        request,
        'products.html',
        context
    )


def products(request):
    """جميع المنتجات مع الفلاتر والترتيب"""

    # =========================
    # All Active Products
    # =========================

    products_list = Product.objects.filter(
        is_active=True
    )

    # =========================
    # All Categories
    # =========================

    all_categories = Category.objects.filter(
        is_active=True
    )

    # =========================
    # Filter: Category
    # =========================

    selected_categories = request.GET.getlist(
        'category'
    )

    if selected_categories:

        products_list = products_list.filter(
            category__slug__in=selected_categories
        )

    # =========================
    # Filter: Subcategory
    # =========================

    selected_subcategories = request.GET.getlist(
        'subcategory'
    )

    if selected_subcategories:

        products_list = products_list.filter(
            subcategory__slug__in=selected_subcategories,
            subcategory__is_active=True
        )

    # =========================
    # Package Filter
    # =========================

    # لا يوجد package_type في Product حاليًا
    selected_packages = []

    # =========================
    # Sorting
    # =========================

    sort = request.GET.get(
        'sort',
        '-created_at'
    )

    allowed_sorts = {
        '-created_at': '-created_at',
        'created_at': 'created_at',
        'name': 'name',
        '-name': '-name',
        'price': 'price',
        '-price': '-price',
    }

    sort_field = allowed_sorts.get(
        sort,
        '-created_at'
    )

    products_list = products_list.order_by(
        sort_field
    )

    # =========================
    # Pagination
    # =========================

    paginator = Paginator(
        products_list,
        48
    )

    page_number = request.GET.get(
        'page'
    )

    products_page = paginator.get_page(
        page_number
    )

    # =========================
    # Query String
    # =========================

    query_params = request.GET.copy()

    if 'page' in query_params:
        query_params.pop('page')

    if 'package' in query_params:
        query_params.pop('package')

    query_string = query_params.urlencode()

    # =========================
    # Subcategories for dynamic filter
    # =========================

    all_subcategories = Subcategory.objects.filter(
        is_active=True
    ).select_related('category').order_by(
        'category__name',
        'name'
    )

    subcategories_by_category = {}

    for subcategory in all_subcategories:

        category_slug = subcategory.category.slug

        subcategories_by_category.setdefault(
            category_slug,
            []
        ).append({
            'slug': subcategory.slug,
            'name': subcategory.name,
            'count': subcategory.products.filter(
                is_active=True
            ).count(),
        })

    # =========================
    # Context
    # =========================

    context = {
        'products': products_page,

        'all_categories': all_categories,

        'subcategories': [],

        'subcategories_by_category': subcategories_by_category,

        'current_category': None,

        'selected_subcategory': '',

        'selected_categories': selected_categories,

        'selected_subcategories': selected_subcategories,

        'selected_packages': selected_packages,

        'current_sort': sort,

        'package_types': [],

        'query_string': query_string,
    }

    return render(
        request,
        'products.html',
        context
    )


def product_detail(request, slug):
    """تفاصيل منتج"""

    product = get_object_or_404(
        Product,
        slug=slug,
        is_active=True
    )

    related_products = Product.objects.filter(
        category=product.category,
        is_active=True
    ).exclude(
        id=product.id
    )[:4]

    context = {
        'product': product,
        'related_products': related_products,
    }

    return render(
        request,
        'product_detail.html',
        context
    )


# ============================================================
# CART / PANIER
# ============================================================

def _get_cart(request):
    """إرجاع السلة من Session بصيغة {product_id: quantity}."""
    return request.session.get('cart', {})


def cart_add(request, slug):
    """إضافة منتج إلى السلة."""
    if request.method != 'POST':
        return redirect('catalog:product_detail', slug=slug)

    product = get_object_or_404(
        Product,
        slug=slug,
        is_active=True
    )

    if product.quantity <= 0:
        messages.error(
            request,
            'عذرًا، هذا المنتج غير متوفر حاليًا.'
        )
        return redirect(
            'catalog:product_detail',
            slug=product.slug
        )

    try:
        quantity = int(request.POST.get('quantity', 1))
    except (TypeError, ValueError):
        quantity = 1

    if quantity < 1:
        quantity = 1

    if quantity > product.quantity:
        quantity = product.quantity

    cart = _get_cart(request)
    product_id = str(product.id)

    current_quantity = int(cart.get(product_id, 0))
    new_quantity = current_quantity + quantity

    if new_quantity > product.quantity:
        new_quantity = product.quantity

    cart[product_id] = new_quantity

    request.session['cart'] = cart
    request.session.modified = True

    messages.success(
        request,
        'تمت إضافة المنتج إلى السلة.'
    )

    return redirect('catalog:cart')


def cart(request):
    """عرض السلة."""
    cart_data = _get_cart(request)

    product_ids = []
    for product_id in cart_data.keys():
        try:
            product_ids.append(int(product_id))
        except (TypeError, ValueError):
            pass

    products = Product.objects.filter(
        id__in=product_ids,
        is_active=True
    )

    products_by_id = {
        str(product.id): product
        for product in products
    }

    items = []
    total = Decimal('0')
    cart_count = 0
    cleaned_cart = {}

    for product_id, quantity in cart_data.items():

        product = products_by_id.get(str(product_id))

        if not product:
            continue

        try:
            quantity = int(quantity)
        except (TypeError, ValueError):
            continue

        if quantity < 1:
            continue

        if product.quantity <= 0:
            continue

        quantity = min(quantity, product.quantity)

        cleaned_cart[str(product.id)] = quantity

        unit_price = product.price or Decimal('0')
        subtotal = unit_price * quantity

        total += subtotal
        cart_count += quantity

        items.append({
            'product': product,
            'quantity': quantity,
            'unit_price': unit_price,
            'subtotal': subtotal,
        })

    if cleaned_cart != cart_data:
        request.session['cart'] = cleaned_cart
        request.session.modified = True

    return render(
        request,
        'cart.html',
        {
            'items': items,
            'total': total,
            'cart_count': cart_count,
        }
    )


def cart_update(request, product_id):
    """تحديث كمية منتج داخل السلة."""
    if request.method != 'POST':
        return redirect('catalog:cart')

    product = get_object_or_404(
        Product,
        id=product_id,
        is_active=True
    )

    try:
        quantity = int(request.POST.get('quantity', 0))
    except (TypeError, ValueError):
        quantity = 0

    cart_data = _get_cart(request)
    key = str(product.id)

    if quantity <= 0:
        cart_data.pop(key, None)
    elif product.quantity <= 0:
        cart_data.pop(key, None)
    else:
        cart_data[key] = min(quantity, product.quantity)

    request.session['cart'] = cart_data
    request.session.modified = True

    return redirect('catalog:cart')


def cart_remove(request, product_id):
    """حذف منتج من السلة."""
    if request.method != 'POST':
        return redirect('catalog:cart')

    cart_data = _get_cart(request)
    cart_data.pop(str(product_id), None)

    request.session['cart'] = cart_data
    request.session.modified = True

    return redirect('catalog:cart')


def cart_checkout(request):
    """إتمام طلب جميع المنتجات الموجودة في السلة."""

    cart_data = _get_cart(request)

    if not cart_data:
        messages.error(
            request,
            'السلة فارغة.'
        )
        return redirect('catalog:cart')

    product_ids = []
    for product_id in cart_data.keys():
        try:
            product_ids.append(int(product_id))
        except (TypeError, ValueError):
            pass

    products = Product.objects.filter(
        id__in=product_ids,
        is_active=True
    )

    products_by_id = {
        str(product.id): product
        for product in products
    }

    # Build a clean snapshot of the cart.
    items = []
    products_total = Decimal('0')
    cleaned_cart = {}

    for product_id, raw_quantity in cart_data.items():

        product = products_by_id.get(str(product_id))

        if not product:
            messages.error(
                request,
                'أحد المنتجات في السلة لم يعد متوفرًا.'
            )
            return redirect('catalog:cart')

        try:
            quantity = int(raw_quantity)
        except (TypeError, ValueError):
            messages.error(
                request,
                'الكمية الموجودة في السلة غير صحيحة.'
            )
            return redirect('catalog:cart')

        if quantity < 1:
            messages.error(
                request,
                'الكمية الموجودة في السلة غير صحيحة.'
            )
            return redirect('catalog:cart')

        if quantity > product.quantity:
            messages.error(
                request,
                f'الكمية المطلوبة من {product.name} أكبر من المتوفر.'
            )
            return redirect('catalog:cart')

        cleaned_cart[str(product.id)] = quantity

        unit_price = product.price or Decimal('0')
        subtotal = unit_price * quantity
        products_total += subtotal

        items.append({
            'product': product,
            'quantity': quantity,
            'unit_price': unit_price,
            'subtotal': subtotal,
        })

    request.session['cart'] = cleaned_cart
    request.session.modified = True

    wilayas = Wilaya.objects.filter(is_active=True)

    if request.method == 'POST':

        full_name = request.POST.get(
            'full_name',
            ''
        ).strip()

        phone = request.POST.get(
            'phone',
            ''
        ).strip()

        email = request.POST.get(
            'email',
            ''
        ).strip()

        note = request.POST.get(
            'note',
            ''
        ).strip()

        wilaya_id = request.POST.get('wilaya')

        if not full_name or not phone:
            messages.error(
                request,
                'يرجى إدخال الاسم ورقم الهاتف.'
            )
            return render(
                request,
                'cart_checkout.html',
                {
                    'items': items,
                    'products_total': products_total,
                    'wilayas': wilayas,
                    'full_name': full_name,
                    'phone': phone,
                    'email': email,
                    'note': note,
                }
            )

        if not wilaya_id:
            messages.error(
                request,
                'يرجى اختيار الولاية.'
            )
            return render(
                request,
                'cart_checkout.html',
                {
                    'items': items,
                    'products_total': products_total,
                    'wilayas': wilayas,
                    'full_name': full_name,
                    'phone': phone,
                    'email': email,
                    'note': note,
                }
            )

        wilaya = get_object_or_404(
            Wilaya,
            id=wilaya_id,
            is_active=True
        )

        # One delivery fee for the whole cart.
        delivery_price = wilaya.delivery_price or Decimal('0')
        grand_total = products_total + delivery_price

        created_order = None

        try:
            with transaction.atomic():

                # Create one order for the whole cart.
                # CartOrderItem rows represent the products inside it.
                order = CartOrder.objects.create(
                    full_name=full_name,
                    phone=phone,
                    email=email,
                    wilaya=wilaya,
                    products_total=products_total,
                    delivery_price=delivery_price,
                    total_price=grand_total,
                    note=note,
                )

                # Create one CartOrderItem for every product.
                # CartOrderItem.save() handles stock deduction.
                for item in items:
                    product = Product.objects.select_for_update().get(
                        pk=item['product'].pk
                    )

                    if (
                        not product.is_active
                        or product.quantity < item['quantity']
                    ):
                        raise ValueError(
                            f'Insufficient stock for {product.name}.'
                        )

                    CartOrderItem.objects.create(
                        order=order,
                        product=product,
                        quantity=item['quantity'],
                        product_price=product.price or Decimal('0'),
                        total_price=(
                            (product.price or Decimal('0'))
                            * item['quantity']
                        ),
                    )

                created_order = order

        except ValueError:
            messages.error(
                request,
                'تغيرت الكمية المتوفرة لأحد المنتجات. راجع السلة ثم حاول مرة أخرى.'
            )
            return redirect('catalog:cart')

        # Empty the cart only after every order was created successfully.
        request.session['cart'] = {}
        request.session.modified = True

        return render(
            request,
            'cart_order_success.html',
            {
                'order': created_order,
                'orders': [created_order],
                'products_total': products_total,
                'delivery_price': delivery_price,
                'grand_total': grand_total,
            }
        )

    return render(
        request,
        'cart_checkout.html',
        {
            'items': items,
            'products_total': products_total,
            'wilayas': wilayas,
        }
    )

def about(request):
    """صفحة طلب المنتج"""

    return render(
        request,
        'order.html'
    )


def contact(request):
    """صفحة التواصل"""

    if request.method == 'POST':

        form = ContactForm(
            request.POST
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                'تم إرسال رسالتك بنجاح! سنتواصل معك في أقرب وقت.'
            )

            return redirect(
                'catalog:contact'
            )

        else:

            messages.error(
                request,
                'حدث خطأ أثناء إرسال الرسالة. يرجى التحقق من البيانات المدخلة.'
            )

    else:

        form = ContactForm()

    context = {
        'form': form,
    }

    return render(
        request,
        'contact.html',
        context
    )


def search(request):
    """البحث"""

    query = request.GET.get(
        'q',
        ''
    )

    # AJAX autocomplete فقط؛ منطق البحث العادي أسفل هذا الجزء لم يتغير.
    if request.GET.get('suggestions') == '1':
        suggestions = []

        if query.strip():
            suggestion_products = Product.objects.filter(
                Q(name__icontains=query),
                is_active=True
            ).order_by('name')[:15]

            for product in suggestion_products:
                suggestions.append({
                'name': product.name,
                'part_number': product.part_number or '',
                'image': product.image.url if product.image else '',
                'url': reverse(
                    'catalog:product_detail',
                    kwargs={'slug': product.slug}
                ),
            })

        return JsonResponse({'results': suggestions})

    results = []

    results_count = 0

    if query:

        results_list = Product.objects.filter(

            Q(name__icontains=query) ,

            is_active=True

        )

        results_count = results_list.count()

        paginator = Paginator(
            results_list,
            120
        )

        page_number = request.GET.get(
            'page'
        )

        results = paginator.get_page(
            page_number
        )

    context = {
        'query': query,
        'results': results,
        'results_count': results_count,
    }

    return render(
        request,
        'search_results.html',
        context
    )