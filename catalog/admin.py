from django.contrib import admin
from django import forms
from django.urls import reverse
from django.utils.html import format_html
from decimal import Decimal

from .models import (
    Category,
    Subcategory,
    Product,
    ProductImage,
    SpecificationType,
    Specification,
    Wilaya,
    Commune,
    CartOrder,
    CartOrderItem,
)


class ProductPriceSelect(forms.Select):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.price_map = {}

    def create_option(
        self,
        name,
        value,
        label,
        selected,
        index,
        subindex=None,
        attrs=None
    ):
        option = super().create_option(
            name,
            value,
            label,
            selected,
            index,
            subindex=subindex,
            attrs=attrs,
        )

        if value not in (None, '', '__empty__'):

            try:

                product_id = int(str(value))

                if product_id not in self.price_map:

                    product = Product.objects.filter(
                        pk=product_id
                    ).only('price').first()

                    if product:
                        self.price_map[product_id] = (
                            product.price or Decimal('0')
                        )

                if product_id in self.price_map:

                    option['attrs']['data-price'] = str(
                        self.price_map[product_id]
                    )

            except (TypeError, ValueError):
                pass

        return option


class WilayaSelect(forms.Select):
    """Wilaya selector.

    Delivery price belongs to Commune, not Wilaya.
    """

    pass


class CommuneDeliverySelect(forms.Select):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.delivery_map = {}

    def create_option(
        self,
        name,
        value,
        label,
        selected,
        index,
        subindex=None,
        attrs=None
    ):
        option = super().create_option(
            name,
            value,
            label,
            selected,
            index,
            subindex=subindex,
            attrs=attrs,
        )

        if value not in (None, '', '__empty__'):
            try:
                commune_id = int(str(value))

                if commune_id not in self.delivery_map:
                    commune = Commune.objects.filter(
                        pk=commune_id
                    ).only('delivery_price', 'wilaya_id').first()

                    if commune:
                        self.delivery_map[commune_id] = {
                            'delivery_price': commune.delivery_price or Decimal('0'),
                            'wilaya_id': commune.wilaya_id,
                        }

                if commune_id in self.delivery_map:
                    data = self.delivery_map[commune_id]

                    # Show only the Commune name in the dropdown.
                    commune = Commune.objects.filter(
                        pk=commune_id
                    ).only('name').first()

                    if commune:
                        option['label'] = commune.name

                    # Used by JavaScript to filter by Wilaya.
                    option['attrs']['data-wilaya'] = str(
                        data['wilaya_id']
                    )

                    # Used by JavaScript to calculate delivery price.
                    option['attrs']['data-delivery-price'] = str(
                        data['delivery_price']
                    )

            except (TypeError, ValueError):
                pass

        return option


class CartOrderForm(forms.ModelForm):

    class Meta:

        model = CartOrder

        fields = '__all__'

        widgets = {

            'wilaya': WilayaSelect(),
            'commune': CommuneDeliverySelect(),

            'products_total': forms.NumberInput(
                attrs={
                    'readonly': 'readonly'
                }
            ),

            'delivery_price': forms.NumberInput(
                attrs={
                    'readonly': 'readonly'
                }
            ),

            'total_price': forms.NumberInput(
                attrs={
                    'readonly': 'readonly'
                }
            ),
        }


    def clean(self):
        cleaned_data = super().clean()

        wilaya = cleaned_data.get('wilaya')
        commune = cleaned_data.get('commune')

        if wilaya and commune and commune.wilaya_id != wilaya.id:
            raise forms.ValidationError(
                'The selected commune does not belong to the selected wilaya.'
            )

        if commune:
            cleaned_data['delivery_price'] = (
                commune.delivery_price or Decimal('0')
            )

        return cleaned_data


class CartOrderItemForm(forms.ModelForm):

    class Meta:

        model = CartOrderItem

        fields = '__all__'

        widgets = {

            'product': ProductPriceSelect(),

            'product_price': forms.NumberInput(
                attrs={
                    'readonly': 'readonly'
                }
            ),

            'total_price': forms.NumberInput(
                attrs={
                    'readonly': 'readonly'
                }
            ),
        }


class ProductImageInline(admin.TabularInline):

    model = ProductImage

    extra = 2

    fields = [
        'image',
    ]


class SpecificationInlineForm(forms.ModelForm):

    name = forms.ChoiceField(
        label='Name',
        required=True
    )

    class Meta:
        model = Specification
        fields = [
            'name',
            'value',
            'order'
        ]

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        # The dropdown is built ONLY from SpecificationType.
        type_names = list(
            SpecificationType.objects
            .order_by('name')
            .values_list('name', flat=True)
        )

        choices = [
            (name, name)
            for name in type_names
            if name
        ]

        self.fields['name'].choices = [
            ('', '---------'),
            *choices,
        ]

        # Existing Specification rows keep their current name selected.
        current_name = self.instance.name

        if (
            current_name
            and current_name not in type_names
        ):
            # Keep old data editable until its name is added to
            # SpecificationType. This does not create a new type.
            self.fields['name'].choices.insert(
                1,
                (current_name, current_name)
            )

    def save(self, commit=True):

        instance = super().save(commit=False)

        name = (self.cleaned_data.get('name') or '').strip()

        if name:
            specification_type = (
                SpecificationType.objects
                .filter(name=name)
                .first()
            )

            if not specification_type:
                raise forms.ValidationError(
                    'The selected specification type does not exist.'
                )

            instance.specification_type = specification_type
            instance.name = specification_type.name

        if commit:
            instance.save()

        return instance


class SpecificationInline(admin.TabularInline):

    model = Specification

    form = SpecificationInlineForm

    extra = 3

    fields = [
        'name',
        'value',
        'order'
    ]


@admin.register(SpecificationType)
class SpecificationTypeAdmin(admin.ModelAdmin):

    list_per_page = 20

    list_display = [
        'name'
    ]

    search_fields = [
        'name'
    ]

    ordering = [
        'name'
    ]


@admin.register(Subcategory)
class SubcategoryAdmin(admin.ModelAdmin):

    list_per_page = 20

    list_display = [
        'name',
        'category',
        'is_active',
    ]

    list_filter = [
        'category',
        'is_active',
    ]

    search_fields = [
        'name',
        'category__name',
    ]

    prepopulated_fields = {
        'slug': ('name',)
    }

    list_editable = [
        'is_active',
    ]

    ordering = [
        'category__name',
        'name',
    ]


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):

    list_per_page = 20

    list_display = [
        'name',
        'product_count',
        'is_active',
        'is_featured',
        'created_at'
    ]

    list_filter = [
        'is_active',
        'is_featured',
        'created_at'
    ]

    search_fields = [
        'name',
        'description',
        'subcategory__name'
    ]

    prepopulated_fields = {
        'slug': ('name',)
    }

    list_editable = [
        'is_active',
        'is_featured'
    ]
    def product_count(self, obj):

        return obj.products.filter(
            is_active=True
        ).count()

    product_count.short_description = 'Product Count'


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_per_page = 20
    list_display = [
        'name',
        'part_number',
        'category',
        'subcategory',
        'price',
        'quantity',
        'is_featured',
        'is_active',
        'created_at'
    ]

    list_filter = [
        'category',
        'subcategory',
        'is_featured',
        'is_active',
        'created_at'
    ]

    search_fields = [
        'name',
    ]

    prepopulated_fields = {
        'slug': ('name',)
    }

    list_editable = [
        'quantity',
        'is_featured',
        'is_active'
    ]

    readonly_fields = [
        'created_at',
        'updated_at'
    ]

    inlines = [
        SpecificationInline,
        ProductImageInline,
    ]

    fieldsets = (

        (
            'Basic Info',
            {
                'fields': (
                    'name',
                    'slug',
                    'part_number',
                    'category',
                    'subcategory',
                )
            }
        ),

        (
            'Description',
            {
                'fields': (
                    'short_description',
                    'description'
                )
            }
        ),

        (
            'Files & Images',
            {
                'fields': (
                    'image',
                    'pinout_image',
                    'datasheet'
                )
            }
        ),

        (
            'Technical Info',
            {
                'fields': (
                    'technical_info',
                )
            }
        ),

        (
            'Pricing & Inventory',
            {
                'fields': (
                    'price',
                    'quantity',
                )
            }
        ),

        (
            'Settings',
            {
                'fields': (
                    'is_featured',
                    'is_active',
                    'created_at',
                    'updated_at'
                )
            }
        ),

    )
def get_view_on_site_url(self, obj):
    if obj is None or not obj.pk or not obj.slug:
        return None

    return reverse(
        'catalog:product_detail',
        kwargs={'slug': obj.slug}
    )

@admin.register(Specification)
class SpecificationAdmin(admin.ModelAdmin):

    list_per_page = 20

    list_display = [
        'name',
        'value',
        'product',
        'order'
    ]

    list_filter = [
        'product__category'
    ]

    search_fields = [
        'name',
        'value',
        'product__name'
    ]

    list_editable = [
        'order'
    ]


@admin.register(Wilaya)
class WilayaAdmin(admin.ModelAdmin):

    list_per_page = 20

    list_display = [
        'code',
        'name',
        'is_active'
    ]

    list_filter = [
        'is_active'
    ]

    search_fields = [
        'name'
    ]

    list_editable = [
        'is_active'
    ]

    ordering = [
        'code'
    ]


@admin.register(Commune)
class CommuneAdmin(admin.ModelAdmin):

    list_per_page = 20

    list_display = [
        'name',
        'wilaya',
        'delivery_price',
        'is_active',
    ]

    list_filter = [
        'wilaya',
        'is_active',
    ]

    search_fields = [
        'name',
        'wilaya__name',
    ]

    list_editable = [
        'delivery_price',
        'is_active',
    ]

    ordering = [
        'wilaya__code',
        'name',
    ]


class CartOrderItemInline(admin.TabularInline):

    model = CartOrderItem

    form = CartOrderItemForm

    extra = 1

    fields = [
        'product',
        'quantity',
        'product_price',
        'total_price',
        'stock_deducted',
    ]

    readonly_fields = [
        'stock_deducted',
    ]

    class Media:

        js = (
            'admin/js/cart_order_admin.js',
        )


@admin.register(CartOrder)
class CartOrderAdmin(admin.ModelAdmin):

    list_per_page = 20

    form = CartOrderForm

    class Media:

        js = (
            'admin/js/cart_order_admin.js',
        )

    list_display = [
        'id',
        'customer_name_link',
        'phone',
        'wilaya',
        'commune',
        'products_total',
        'delivery_price',
        'total_price',
        'status',
        'is_read',
        'created_at',
        'delete_link',
    ]

    list_filter = [
        'status',
        'is_read',
        'wilaya',
        'commune',
        'created_at',
    ]

    search_fields = [
        'full_name',
        'phone',
        'email',
        'items__product__name',
        'items__product__part_number',
    ]

    list_editable = [
        'status',
        'is_read',
    ]

    readonly_fields = [
        'created_at',
        'updated_at',
    ]

    inlines = [
        CartOrderItemInline,
    ]

    fieldsets = (

        (
            'Order Information',
            {
                'fields': (
                    'status',
                    'is_read',
                )
            }
        ),

        (
            'Customer Information',
            {
                'fields': (
                    'full_name',
                    'phone',
                    'email',
                )
            }
        ),

        (
            'Delivery',
            {
                'fields': (
                    'wilaya',
                    'commune',
                    'delivery_price',
                )
            }
        ),

        (
            'Prices',
            {
                'fields': (
                    'products_total',
                    'total_price',
                )
            }
        ),

        (
            'Additional Information',
            {
                'fields': (
                    'note',
                )
            }
        ),

        (
            'Dates',
            {
                'fields': (
                    'created_at',
                    'updated_at',
                )
            }
        ),

    )

    def customer_name_link(self, obj):

        url = reverse(
            'admin:catalog_cartorder_change',
            args=[obj.pk]
        )

        return format_html(
            '<a href="{}">{}</a>',
            url,
            obj.full_name
        )

    customer_name_link.short_description = 'Customer Name'

    def delete_link(self, obj):
        url = reverse(
            'admin:catalog_cartorder_delete',
            args=[obj.pk]
        )
        return format_html(
            '<a href="{}" '
            'style="display:inline-block; '
            'background:#dc3545; '
            'color:#fff; '
            'padding:5px 12px; '
            'border-radius:4px; '
            'text-decoration:none; '
            'font-size:12px; '
            'font-weight:600; '
            'line-height:1.4;">'
            'Delete'
            '</a>',
            url
        )

    delete_link.short_description = 'Delete'

    def mark_as_read(self, request, queryset):

        queryset.update(
            is_read=True
        )

    mark_as_read.short_description = 'Mark as Read'

    def mark_as_unread(self, request, queryset):

        queryset.update(
            is_read=False
        )

    mark_as_unread.short_description = 'Mark as Unread'

    def save_formset(
        self,
        request,
        form,
        formset,
        change
    ):

        instances = formset.save(
            commit=False
        )

        for deleted_object in formset.deleted_objects:

            deleted_object.delete()

        for item in instances:

            if item.product_id:

                item.product_price = (
                    item.product.price
                    or Decimal('0')
                )

                item.total_price = (
                    item.product_price
                    * item.quantity
                )

            item.save()

        formset.save_m2m()

        order = form.instance

        products_total = sum(
            (
                item.total_price
                or Decimal('0')
                for item in order.items.all()
            ),
            Decimal('0'),
        )

        delivery_price = (
            order.commune.delivery_price
            if order.commune_id
            else Decimal('0')
        )

        total_price = (
            products_total
            + delivery_price
        )

        CartOrder.objects.filter(
            pk=order.pk
        ).update(
            products_total=products_total,
            delivery_price=delivery_price,
            total_price=total_price,
        )

    actions = [
        mark_as_read,
        mark_as_unread
    ]
