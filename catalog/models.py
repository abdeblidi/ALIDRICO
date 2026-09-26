from django.db import models, transaction
from django.core.exceptions import ValidationError
from django.urls import reverse
from django.utils.text import slugify


class Category(models.Model):
    """Product category"""

    name = models.CharField(
        max_length=100,
        verbose_name="Name"
    )

    slug = models.SlugField(
        unique=True,
        blank=True,
        verbose_name="Slug"
    )

    description = models.TextField(
        blank=True,
        verbose_name="Description"
    )



    image = models.ImageField(
        upload_to='categories/',
        blank=True,
        verbose_name="Image",
        default='products/no image.png'
    )

    is_active = models.BooleanField(
        default=True,
        verbose_name="Active"
    )
    is_featured = models.BooleanField(
    default=False,
    verbose_name="Featured"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Created At"
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Updated At"
    )

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse(
            'category_products',
            kwargs={'slug': self.slug}
        )

    def product_count(self):
        return self.products.filter(
            is_active=True
        ).count()

    product_count.short_description = "Product Count"

    def save(self, *args, **kwargs):

        if not self.slug:
            self.slug = slugify(self.name)

        super().save(*args, **kwargs)


class Subcategory(models.Model):
    """Subcategory belonging to a main product category."""

    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='subcategories',
        verbose_name="Category"
    )

    name = models.CharField(
        max_length=100,
        verbose_name="Name"
    )

    slug = models.SlugField(
        max_length=120,
        verbose_name="Slug"
    )

    is_active = models.BooleanField(
        default=True,
        verbose_name="Active"
    )

    class Meta:
        verbose_name = "Subcategory"
        verbose_name_plural = "Subcategories"
        ordering = ['name']
        constraints = [
            models.UniqueConstraint(
                fields=['category', 'slug'],
                name='unique_subcategory_slug_per_category'
            )
        ]

    def __str__(self):
        return f"{self.category.name} - {self.name}"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Product(models.Model):
    """Electronic component product"""

    name = models.CharField(
        max_length=200,
        verbose_name="Name"
    )

    slug = models.SlugField(
        unique=True,
        verbose_name="Slug",
        max_length=255
    )

    part_number = models.CharField(
        max_length=100,
        verbose_name="Part Number",
        blank=True
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='products',
        verbose_name="Category"
    )

    subcategory = models.ForeignKey(
        Subcategory,
        on_delete=models.SET_NULL,
        related_name='products',
        blank=True,
        null=True,
        verbose_name="Subcategory"
    )

    description = models.TextField(
        verbose_name="Description",blank=True
    )

    short_description = models.CharField(
        max_length=255,
        blank=True,
        verbose_name="Short Description"
    )

    image = models.ImageField(
        upload_to='products/',
        blank=True,
        verbose_name="Product Image",
        default='products/no image.png'
    )

    pinout_image = models.ImageField(
        upload_to='products/pinouts/',
        blank=True,
        verbose_name="Pinout Image",
        default='products/no image.png'
    )

    datasheet = models.FileField(
        upload_to='datasheets/',
        blank=True,
        verbose_name="Datasheet PDF"
    )

    technical_info = models.TextField(
        blank=True,
        verbose_name="Technical Info"
    )

    price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        blank=True,
        verbose_name="Price (DZD)",
        default=0
    )



    quantity = models.PositiveIntegerField(
        default=0,
        verbose_name="Stock Quantity"
    )

    is_featured = models.BooleanField(
        default=False,
        verbose_name="Featured"
    )

    is_active = models.BooleanField(
        default=True,
        verbose_name="Active"
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Created At"
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Updated At"
    )

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.part_number} - {self.name}"

    def get_absolute_url(self):
        return reverse(
            'product_detail',
            kwargs={'slug': self.slug}
        )

def save(self, *args, **kwargs):

    if not self.slug:

        base_slug = slugify(self.name)

        slug = base_slug
        counter = 1

        while Product.objects.filter(
            slug=slug
        ).exists():

            slug = f"{base_slug}-{counter}"
            counter += 1

        self.slug = slug

    if not self.short_description:
        self.short_description = self.description[:250]

    super().save(*args, **kwargs)

   

class SpecificationType(models.Model):
    """Reusable specification name/type."""

    name = models.CharField(
        max_length=100,
        unique=True,
        verbose_name="Name"
    )

    class Meta:
        verbose_name = "Specification Type"
        verbose_name_plural = "Specification Types"
        ordering = ['name']

    def __str__(self):
        return self.name


class Specification(models.Model):
    """Product technical specification"""

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='specifications',
        verbose_name="Product"
    )

    # This keeps the reusable specification name separate from the
    # product-specific specification record.
    #
    # null=True/blank=True is intentional so existing Specification
    # records continue to work safely before they are synchronized.
    specification_type = models.ForeignKey(
        SpecificationType,
        on_delete=models.PROTECT,
        related_name='specifications',
        null=True,
        blank=True,
        verbose_name="Specification Type"
    )

    # Kept for backward compatibility with the existing database/data.
    # It is synchronized with specification_type when the record is saved.
    name = models.CharField(
        max_length=100,
        verbose_name="Name"
    )

    value = models.CharField(
        max_length=255,
        verbose_name="Value"
    )

    order = models.PositiveIntegerField(
        default=0,
        verbose_name="Order"
    )

    class Meta:
        verbose_name = "Specification"
        verbose_name_plural = "Specifications"
        ordering = ['order', 'id']

    def __str__(self):
        return f"{self.name}: {self.value}"

    def save(self, *args, **kwargs):
        # Make sure every specification name also exists as a reusable
        # SpecificationType. Existing rows are synchronized the first
        # time they are saved; no existing specification data is deleted.
        if self.specification_type_id:
            self.name = self.specification_type.name
        elif self.name:
            specification_type, _ = SpecificationType.objects.get_or_create(
                name=self.name.strip()
            )
            self.specification_type = specification_type
            self.name = specification_type.name

        super().save(*args, **kwargs)


class Wilaya(models.Model):
    """Algerian wilaya and delivery price"""

    name = models.CharField(
        max_length=100,
        unique=True,
        verbose_name="Wilaya"
    )

    code = models.CharField(
        max_length=10,
        unique=True,
        verbose_name="Wilaya Code"
    )


    is_active = models.BooleanField(
        default=True,
        verbose_name="Active"
    )

    class Meta:
        verbose_name = "Wilaya"
        verbose_name_plural = "Wilayas"
        ordering = ['code']

    def __str__(self):
        return self.name


class Commune(models.Model):
    """Algerian commune belonging to a wilaya."""

    wilaya = models.ForeignKey(
        Wilaya,
        on_delete=models.CASCADE,
        related_name='communes',
        verbose_name="Wilaya"
    )

    name = models.CharField(
        max_length=100,
        verbose_name="Commune"
    )

    delivery_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name="Delivery Price (DZD)"
    )

    is_active = models.BooleanField(
        default=True,
        verbose_name="Active"
    )

    class Meta:
        verbose_name = "Commune"
        verbose_name_plural = "Communes"
        ordering = ['name']

    def __str__(self):
        return f"{self.wilaya.name} - {self.name}"


class CartOrder(models.Model):
    """Customer order created from the shopping cart"""

    STATUS_CHOICES = [
        ('new', 'New'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    # =====================================================
    # Customer Information
    # =====================================================

    full_name = models.CharField(
        max_length=100,
        verbose_name="Customer Name"
    )

    phone = models.CharField(
        max_length=13,
        verbose_name="Phone"
    )

    email = models.EmailField(
        blank=True,
        verbose_name="Email"
    )

    # =====================================================
    # Delivery
    # =====================================================

    wilaya = models.ForeignKey(
        Wilaya,
        on_delete=models.PROTECT,
        related_name='cart_orders',
        verbose_name="Wilaya"
    )
    commune = models.ForeignKey(
        Commune,
        on_delete=models.PROTECT,
        related_name='cart_orders',
        verbose_name="Commune",
        null=True,
        blank=True
    )

    # =====================================================
    # Prices
    # =====================================================

    products_total = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        verbose_name="Products Total (DZD)"
    )

    delivery_price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        verbose_name="Delivery Price (DZD)"
    )

    total_price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        verbose_name="Total Price (DZD)"
    )

    # =====================================================
    # Additional Information
    # =====================================================

    note = models.TextField(
        blank=True,
        verbose_name="Customer Note"
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='new',
        verbose_name="Status"
    )

    is_read = models.BooleanField(
        default=False,
        verbose_name="Read"
    )

    # =====================================================
    # Dates
    # =====================================================

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        verbose_name = "Cart Order"
        verbose_name_plural = "Cart Orders"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.full_name} - Cart Order #{self.pk}"

    def save(self, *args, **kwargs):
        """
        Save the cart order.

        When an existing order changes status, synchronize the stock
        state of all its items.
        """

        with transaction.atomic():

            super().save(*args, **kwargs)

            if self.pk:
                for item in self.items.select_related('product').all():
                    item.save()


class CartOrderItem(models.Model):
    """A single product inside a cart order"""

    order = models.ForeignKey(
        CartOrder,
        on_delete=models.CASCADE,
        related_name='items',
        verbose_name="Cart Order"
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.PROTECT,
        related_name='cart_order_items',
        verbose_name="Product"
    )

    quantity = models.PositiveIntegerField(
        verbose_name="Quantity"
    )

    product_price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        verbose_name="Product Unit Price (DZD)"
    )

    total_price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        verbose_name="Item Total Price (DZD)"
    )

    stock_deducted = models.BooleanField(
        default=False,
        editable=False,
        verbose_name="Stock Deducted"
    )

    class Meta:
        verbose_name = "Cart Order Item"
        verbose_name_plural = "Cart Order Items"
        ordering = ['id']

    def __str__(self):
        return (
            f"Order #{self.order_id} - "
            f"{self.product.name} - "
            f"{self.quantity}"
        )

    def save(self, *args, **kwargs):

        with transaction.atomic():

            product = Product.objects.select_for_update().get(
                pk=self.product_id
            )

            old_quantity = 0
            old_stock_deducted = False

            if self.pk:
                old_item = CartOrderItem.objects.get(
                    pk=self.pk
                )

                old_quantity = old_item.quantity
                old_stock_deducted = old_item.stock_deducted

            self.product_price = product.price or 0
            self.total_price = self.product_price * self.quantity

            order_status = self.order.status

            # =================================================
            # Active Order
            # =================================================

            if order_status in [
                'new',
                'processing',
                'completed'
            ]:

                if not old_stock_deducted:

                    if product.quantity < self.quantity:

                        raise ValidationError(
                            f"Not enough stock. "
                            f"Available: {product.quantity}. "
                            f"Requested: {self.quantity}."
                        )

                    product.quantity -= self.quantity

                    product.save(
                        update_fields=[
                            'quantity',
                            'updated_at'
                        ]
                    )

                    self.stock_deducted = True

                else:

                    difference = self.quantity - old_quantity

                    if difference > 0:

                        if product.quantity < difference:

                            raise ValidationError(
                                f"Not enough stock. "
                                f"Available: {product.quantity}. "
                                f"Additional requested: {difference}."
                            )

                        product.quantity -= difference

                        product.save(
                            update_fields=[
                                'quantity',
                                'updated_at'
                            ]
                        )

                    elif difference < 0:

                        product.quantity += abs(difference)

                        product.save(
                            update_fields=[
                                'quantity',
                                'updated_at'
                            ])

                    self.stock_deducted = True

            # =================================================
            # Cancelled Order
            # =================================================

            elif order_status == 'cancelled':

                if old_stock_deducted:

                    product.quantity += old_quantity

                    product.save(
                        update_fields=[
                            'quantity',
                            'updated_at'
                        ]
                    )

                self.stock_deducted = False

            super().save(*args, **kwargs)


class ContactMessage(models.Model):
    """Contact form message"""

    SUBJECT_CHOICES = [
        ('inquiry', 'General Inquiry'),
        ('product', 'Product Inquiry'),
        ('order', 'Product Order'),
        ('technical', 'Technical Support'),
        ('partnership', 'Partnership'),
        ('other', 'Other'),
    ]

    full_name = models.CharField(
        max_length=100,
        verbose_name="Full Name"
    )

    email = models.EmailField(
        verbose_name="Email"
    )

    phone = models.CharField(
        max_length=20,
        blank=True,
        verbose_name="Phone"
    )

    subject = models.CharField(
        max_length=50,
        choices=SUBJECT_CHOICES,
        verbose_name="Subject"
    )

    product_reference = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="Product Reference"
    )

    message = models.TextField(
        verbose_name="Message"
    )

    is_read = models.BooleanField(
        default=False,
        verbose_name="Read"
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Created At"
    )

    class Meta:
        verbose_name = "Contact Message"
        verbose_name_plural = "Contact Messages"
        ordering = ['-created_at']

    def __str__(self):
        return (
            f"{self.full_name} - "
            f"{self.get_subject_display()}"
        )
class ProductImage(models.Model):
    """Additional image for a product"""

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='additional_images',
        verbose_name="Product"
    )

    image = models.ImageField(
        upload_to='products/',
        verbose_name="Additional Image"
    )

    class Meta:
        verbose_name = "Product Image"
        verbose_name_plural = "Product Images"
        ordering = ['id']

    def __str__(self):
        return f"{self.product.name} - Image #{self.pk}"