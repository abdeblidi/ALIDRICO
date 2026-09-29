```text
Django DB schema (11 models)

Category
- id PK
- name varchar(100)
- slug varchar, UNIQUE
- description text NULL/blank
- image image NULL/blank, default='products/no image.png'
- is_active bool default=true
- is_featured bool default=false
- created_at datetime auto_now_add
- updated_at datetime auto_now

Subcategory
- id PK
- category_id FK->Category CASCADE
- name varchar(100)
- slug varchar(120)
- is_active bool default=true
- UNIQUE(category_id, slug)

Product
- id PK
- name varchar(200)
- slug varchar(255), UNIQUE
- part_number varchar(100) blank
- category_id FK->Category CASCADE
- subcategory_id FK->Subcategory SET_NULL, NULL
- description text blank
- short_description varchar(255) blank
- image image blank, default='products/no image.png'
- pinout_image image blank, default='products/no image.png'
- datasheet file blank
- technical_info text blank
- price decimal(12,2) default=0
- quantity positive_int default=0
- is_featured bool default=false
- is_active bool default=true
- created_at datetime auto_now_add
- updated_at datetime auto_now
- save(): auto-generates unique slug; fills short_description from description

SpecificationType
- id PK
- name varchar(100), UNIQUE

Specification
- id PK
- product_id FK->Product CASCADE
- specification_type_id FK->SpecificationType PROTECT, NULL/blank
- name varchar(100)
- value varchar(255)
- order positive_int default=0

Wilaya
- id PK
- name varchar(100), UNIQUE
- code varchar(10), UNIQUE
- is_active bool default=true

Commune
- id PK
- wilaya_id FK->Wilaya CASCADE
- name varchar(100)
- delivery_price decimal(10,2) default=0
- is_active bool default=true

CartOrder
- id PK
- full_name varchar(100)
- phone varchar(13)
- email email blank
- wilaya_id FK->Wilaya PROTECT
- commune_id FK->Commune PROTECT, NULL/blank
- products_total decimal(12,2)
- delivery_price decimal(12,2)
- total_price decimal(12,2)
- note text blank
- status varchar(20): new|processing|completed|cancelled, default=new
- is_read bool default=false
- created_at datetime auto_now_add
- updated_at datetime auto_now
- save(): syncs each item's stock state

CartOrderItem
- id PK
- order_id FK->CartOrder CASCADE
- product_id FK->Product PROTECT
- quantity positive_int
- product_price decimal(12,2)
- total_price decimal(12,2)
- stock_deducted bool default=false
- save(): copies product price, calculates total, deducts/restores stock according to order status

ContactMessage
- id PK
- full_name varchar(100)
- email email
- phone varchar(20) blank
- subject varchar(50): inquiry|product|order|technical|partnership|other
- product_reference varchar(100) blank
- message text
- is_read bool default=false
- created_at datetime auto_now_add

ProductImage
- id PK
- product_id FK->Product CASCADE
- image image

Relationships
Category 1:N Subcategory
Category 1:N Product
Subcategory 1:N Product
Product 1:N Specification
SpecificationType 1:N Specification
Product 1:N ProductImage
Wilaya 1:N Commune
Wilaya 1:N CartOrder
Commune 1:N CartOrder
CartOrder 1:N CartOrderItem
Product 1:N CartOrderItem
```