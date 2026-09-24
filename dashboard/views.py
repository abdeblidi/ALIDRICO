from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count, Sum, Q
from django.db.models.functions import TruncMonth
from django.utils import timezone
from decimal import Decimal
import json
import calendar
from django.contrib.admin.views.decorators import staff_member_required
from catalog.models import (
    Product,
    Category,
    Subcategory,
    ContactMessage,
    CartOrder,
    CartOrderItem,
)
from .forms import LoginForm


def login_view(request):
    """صفحة تسجيل الدخول"""
    if request.user.is_authenticated:
        return redirect('dashboard:home')

    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)

        if form.is_valid():
            user = form.get_user()
            login(request, user)

            next_url = request.GET.get(
                'next',
                'dashboard:home'
            )

            return redirect(next_url)

        else:
            messages.error(
                request,
                'اسم المستخدم أو كلمة المرور غير صحيحة'
            )

    else:
        form = LoginForm()

    return render(
        request,
        'dashboard/login.html',
        {'form': form}
    )


def logout_view(request):
    """تسجيل الخروج"""
    logout(request)

    messages.success(
        request,
        'تم تسجيل الخروج بنجاح'
    )

    return redirect('dashboard:login')


@staff_member_required (login_url='dashboard:login')
def home(request):
    """الصفحة الرئيسية للـ Dashboard"""

    # =====================================================
    # KPIs
    # =====================================================

    total_products = Product.objects.count()

    total_categories = Category.objects.count()

    total_subcategories = Subcategory.objects.count()

    unread_messages = ContactMessage.objects.filter(
        is_read=False
    ).count()

    featured_products_count = Product.objects.filter(
        is_featured=True
    ).count()

    # =====================================================
    # Chart data
    # =====================================================

    categories_with_counts = Category.objects.annotate(
        product_count=Count('products')
    ).filter(
        product_count__gt=0
    ).order_by(
        '-product_count'
    )[:10]

    chart_labels = json.dumps(
        [cat.name for cat in categories_with_counts]
    )

    chart_data = json.dumps(
        [cat.product_count for cat in categories_with_counts]
    )

    # =====================================================
    # Latest products
    # =====================================================

    latest_products = Product.objects.select_related(
        'category'
    ).order_by(
        '-created_at'
    )[:10]

    # =====================================================
    # Latest messages
    # =====================================================

    latest_messages = ContactMessage.objects.order_by(
        '-created_at'
    )[:8]

    # =====================================================
    # Inactive products
    # =====================================================

    inactive_products = Product.objects.filter(
        is_active=False
    ).select_related(
        'category'
    )[:10]

    # =====================================================
    # Context
    # =====================================================

    context = {
        'total_products': total_products,
        'total_categories': total_categories,
        'total_subcategories': total_subcategories,
        'unread_messages': unread_messages,
        'featured_products_count': featured_products_count,
        'chart_labels': chart_labels,
        'chart_data': chart_data,
        'latest_products': latest_products,
        'latest_messages': latest_messages,
        'inactive_products': inactive_products,
        'user': request.user,
    }

    return render(
        request,
        'dashboard/dashboard.html',
        context
    )


@staff_member_required (login_url='dashboard:login')
def subcategories(request):
    """عرض التصنيفات الفرعية داخل لوحة التحكم."""

    subcategories_list = Subcategory.objects.select_related(
        'category'
    ).annotate(
        product_count=Count(
            'products',
            filter=Q(products__is_active=True)
        )
    ).order_by(
        'category__name',
        'name'
    )

    return render(
        request,
        'dashboard/subcategories.html',
        {
            'subcategories': subcategories_list,
        }
    )


@login_required(login_url='dashboard:login')
def order_statistics(request):
    """إحصائيات الطلبات والمبيعات - المبيعات تعتمد على الطلبات المكتملة فقط."""

    # =====================================================
    # ALL CART ORDERS
    # =====================================================

    cart_orders = CartOrder.objects.all()

    # جميع الطلبات
    total_orders = cart_orders.count()

    # =====================================================
    # ORDER STATUS
    # =====================================================

    new_orders = cart_orders.filter(
        status='new'
    ).count()

    processing_orders = cart_orders.filter(
        status='processing'
    ).count()

    completed_orders = cart_orders.filter(
        status='completed'
    ).count()

    cancelled_orders = cart_orders.filter(
        status='cancelled'
    ).count()

    # =====================================================
    # COMPLETED ORDERS ONLY
    # =====================================================

    completed_cart_orders = cart_orders.filter(
        status='completed'
    )

    completed_cart_items = CartOrderItem.objects.filter(
        order__in=completed_cart_orders
    )

    # =====================================================
    # SALES
    # =====================================================

    products_revenue = completed_cart_orders.aggregate(
        total=Sum('products_total')
    )['total'] or Decimal('0')

    delivery_revenue = completed_cart_orders.aggregate(
        total=Sum('delivery_price')
    )['total'] or Decimal('0')

    total_revenue = products_revenue

    # =====================================================
    # DAILY SALES
    # =====================================================

    today = timezone.localdate()

    daily_revenue = completed_cart_orders.filter(
        created_at__date=today
    ).aggregate(
        total=Sum('products_total')
    )['total'] or Decimal('0')

    # =====================================================
    # PRODUCTS SOLD
    # =====================================================

    products_sold = completed_cart_items.aggregate(
        total=Sum('quantity')
    )['total'] or 0

    # عدد المنتجات المختلفة التي بيعت
    unique_products_sold = completed_cart_items.values(
        'product'
    ).distinct().count()

    # =====================================================
    # PRODUCTS STATISTICS
    # =====================================================

    products_statistics = (
        completed_cart_items
        .values(
            'product__id',
            'product__name',
            'product__part_number',
        )
        .annotate(
            total_quantity=Sum('quantity'),
            total_revenue=Sum('total_price'),
        )
        .order_by('-total_quantity')
    )

    # =====================================================
    # ORDERS DETAILS
    # =====================================================

    orders_details = []

    orders_with_items = completed_cart_orders.prefetch_related(
        'items__product'
    )

    for order in orders_with_items:

        order_quantity = 0
        order_products = []

        for item in order.items.all():

            order_quantity += item.quantity

            order_products.append({
                'name': item.product.name,
                'part_number': item.product.part_number,
                'quantity': item.quantity,
                'unit_price': item.product_price,
                'total_price': item.total_price,
            })

        orders_details.append({
            'id': order.id,
            'customer_name': order.full_name,
            'status': order.status,
            'created_at': order.created_at,
            'products_count': order_quantity,
            'products': order_products,
            'products_total': order.products_total,
            'delivery_price': order.delivery_price,
            'total_price': order.total_price,
        })

    # =====================================================
    # CURRENT MONTH DAILY STATISTICS
    # =====================================================

    today = timezone.localdate()

    days_in_month = calendar.monthrange(
        today.year,
        today.month
    )[1]

    current_month_orders = completed_cart_orders.filter(
        created_at__year=today.year,
        created_at__month=today.month
    )

    daily_order_counts = {
        row['created_at__date']: row['count']
        for row in current_month_orders
        .values('created_at__date')
        .annotate(count=Count('id'))
    }

    daily_sales_totals = {
        row['created_at__date']: row['total'] or Decimal('0')
        for row in current_month_orders
        .values('created_at__date')
        .annotate(total=Sum('products_total'))
    }

    daily_labels = []
    daily_orders = []
    daily_revenue = []

    for day in range(1, days_in_month + 1):

        day_key = today.replace(day=day)

        daily_labels.append(
            day_key.strftime('%d/%m/%Y')
        )

        daily_orders.append(
            daily_order_counts.get(
                day_key,
                0
            )
        )

        daily_revenue.append(
            float(
                daily_sales_totals.get(
                    day_key,
                    Decimal('0')
                )
            )
        )


    # =====================================================
    # MONTHLY STATISTICS
    # =====================================================

    month_starts = []

    year = today.year
    month = today.month

    for _ in range(12):

        month_starts.append(
            (year, month)
        )

        month -= 1

        if month == 0:
            month = 12
            year -= 1

    month_starts.reverse()

    monthly_order_counts = {
        (
            row['month'].year,
            row['month'].month
        ): row['count']

        for row in completed_cart_orders
        .annotate(
            month=TruncMonth('created_at')
        )
        .values('month')
        .annotate(
            count=Count('id')
        )
    }

    monthly_sales_totals = {
        (
            row['month'].year,
            row['month'].month
        ): row['total'] or Decimal('0')

        for row in completed_cart_orders
        .annotate(
            month=TruncMonth('created_at')
        )
        .values('month')
        .annotate(
            total=Sum('products_total')
        )
    }

    monthly_labels = []
    monthly_orders = []
    monthly_revenue = []

    for y, m in month_starts:

        monthly_labels.append(
            f'{m:02d}/{y}'
        )

        monthly_orders.append(
            monthly_order_counts.get(
                (y, m),
                0
            )
        )

        monthly_revenue.append(
            float(
                monthly_sales_totals.get(
                    (y, m),
                    Decimal('0')
                )
            )
        )

    # =====================================================
    # TODAY'S REVENUE ONLY
    # =====================================================

    daily_revenue_total = daily_sales_totals.get(
        today,
        Decimal('0')
    )

    # =====================================================
    # CONTEXT
    # =====================================================

    context = {

        # -----------------------------------------------
        # Orders
        # -----------------------------------------------

        'total_orders': total_orders,

        # -----------------------------------------------
        # Revenue
        # -----------------------------------------------

        'total_revenue': f'{total_revenue:,.2f}',

        'products_revenue': f'{products_revenue:,.2f}',

        'daily_revenue_total': f'{daily_revenue_total:,.2f}',

        'delivery_revenue': f'{delivery_revenue:,.2f}',

        # -----------------------------------------------
        # Status
        # -----------------------------------------------

        'new_orders': new_orders,

        'processing_orders': processing_orders,

        'completed_orders': completed_orders,

        'cancelled_orders': cancelled_orders,

        # -----------------------------------------------
        # Products
        # -----------------------------------------------

        'products_sold': products_sold,

        'unique_products_sold': unique_products_sold,

        'products_statistics': products_statistics,

        'orders_details': orders_details,

        # -----------------------------------------------
        # Current Month Daily Statistics
        # -----------------------------------------------

        'current_month': today.strftime('%m/%Y'),

        'daily_labels': json.dumps(
            daily_labels,
            ensure_ascii=False
        ),

        'daily_orders': json.dumps(
            daily_orders
        ),

        'daily_revenue': json.dumps(
            daily_revenue
        ),

        # -----------------------------------------------
        # Monthly Statistics
        # -----------------------------------------------

        'monthly_labels': json.dumps(
            monthly_labels,
            ensure_ascii=False
        ),

        'monthly_orders': json.dumps(
            monthly_orders
        ),

        'monthly_revenue': json.dumps(
            monthly_revenue
        ),
    }

    return render(
        request,
        'dashboard/order_statistics.html',
        context
    )