(function () {
    'use strict';

    function toNumber(value) {
        const number = parseFloat(value);
        return Number.isFinite(number) ? number : 0;
    }

    // =========================================================
    // PRODUCT SEARCH
    // =========================================================

    function setupProductSearch(select) {

        if (
            !select ||
            select.dataset.productSearchReady === '1'
        ) {
            return;
        }

        select.dataset.productSearchReady = '1';

        const wrapper = document.createElement('div');
        wrapper.className = 'product-search-wrapper';
        wrapper.style.position = 'relative';
        wrapper.style.width = '100%';

        const search = document.createElement('input');

        search.type = 'search';
        search.className = 'product-search-input';
        search.placeholder = 'Search product...';
        search.autocomplete = 'off';

        search.style.width = '100%';
        search.style.boxSizing = 'border-box';
        search.style.marginBottom = '5px';

        const results = document.createElement('div');

        results.className = 'product-search-results';
        results.style.display = 'none';
        results.style.position = 'absolute';
        results.style.left = '0';
        results.style.right = '0';
        results.style.top = '100%';
        results.style.maxHeight = '240px';
        results.style.overflowY = 'auto';
        results.style.background = '#fff';
        results.style.border = '1px solid #ccc';
        results.style.zIndex = '9999';
        results.style.boxSizing = 'border-box';

        const parent = select.parentNode;

        parent.insertBefore(wrapper, select);

        wrapper.appendChild(search);
        wrapper.appendChild(select);
        wrapper.appendChild(results);

        select.style.display = 'none';

        const currentOption =
            select.options[select.selectedIndex];

        if (
            currentOption &&
            currentOption.value
        ) {
            search.value =
                currentOption.textContent.trim();
        }

        function getOptions() {

            return Array.from(
                select.options
            ).filter(function (option) {
                return option.value !== '';
            });
        }

        function hideResults() {
            results.style.display = 'none';
        }

        function chooseOption(option) {

            select.value = option.value;

            search.value =
                option.textContent.trim();

            select.dispatchEvent(
                new Event('change', {
                    bubbles: true
                })
            );

            hideResults();
        }

        function renderResults(query) {

            results.innerHTML = '';

            const normalizedQuery =
                query.trim().toLowerCase();

            if (!normalizedQuery) {
                hideResults();
                return;
            }

            const matches =
                getOptions()
                    .filter(function (option) {

                        return option.textContent
                            .trim()
                            .toLowerCase()
                            .includes(
                                normalizedQuery
                            );
                    })
                    .slice(0, 30);

            if (!matches.length) {

                const empty =
                    document.createElement('div');

                empty.textContent =
                    'No product found';

                empty.style.padding = '8px';
                empty.style.color = '#777';

                results.appendChild(empty);

                results.style.display =
                    'block';

                return;
            }

            matches.forEach(function (option) {

                const item =
                    document.createElement('button');

                item.type = 'button';

                item.textContent =
                    option.textContent.trim();

                item.style.display = 'block';
                item.style.width = '100%';
                item.style.padding = '8px 10px';
                item.style.border = '0';
                item.style.borderBottom =
                    '1px solid #eee';
                item.style.background = '#fff';
                item.style.color = '#333';
                item.style.textAlign = 'left';
                item.style.cursor = 'pointer';
                item.style.font = 'inherit';

                item.addEventListener(
                    'mouseenter',
                    function () {
                        item.style.background =
                            '#f0f0f0';
                    }
                );

                item.addEventListener(
                    'mouseleave',
                    function () {
                        item.style.background =
                            '#fff';
                    }
                );

                item.addEventListener(
                    'mousedown',
                    function (event) {

                        event.preventDefault();

                        chooseOption(option);
                    }
                );

                results.appendChild(item);
            });

            results.style.display = 'block';
        }

        search.addEventListener(
            'input',
            function () {
                renderResults(search.value);
            }
        );

        search.addEventListener(
            'focus',
            function () {

                if (search.value.trim()) {
                    renderResults(search.value);
                }
            }
        );

        search.addEventListener(
            'keydown',
            function (event) {

                if (event.key === 'Escape') {

                    hideResults();
                    search.blur();
                }
            }
        );

        document.addEventListener(
            'click',
            function (event) {

                if (!wrapper.contains(event.target)) {
                    hideResults();
                }
            }
        );

        select.addEventListener(
            'change',
            function () {

                const option =
                    select.options[
                        select.selectedIndex
                    ];

                if (
                    option &&
                    option.value
                ) {
                    search.value =
                        option.textContent.trim();

                } else {
                    search.value = '';
                }
            }
        );
    }

    function getProductRows() {

        const productSelects =
            document.querySelectorAll(
                'select[name$="-product"]'
            );

        const rows = [];

        productSelects.forEach(
            function (select) {

                setupProductSearch(select);

                const row =
                    select.closest('tr');

                if (row) {
                    rows.push(row);
                }
            }
        );

        return rows;
    }

    // =========================================================
    // PRODUCT PRICE / ITEM TOTAL
    // =========================================================

    function updateItem(row) {

        const productSelect =
            row.querySelector(
                'select[name$="-product"]'
            );

        const quantityInput =
            row.querySelector(
                'input[name$="-quantity"]'
            );

        const productPriceInput =
            row.querySelector(
                'input[name$="-product_price"]'
            );

        const itemTotalInput =
            row.querySelector(
                'input[name$="-total_price"]'
            );

        const deleteInput =
            row.querySelector(
                'input[name$="-DELETE"]'
            );

        if (
            !productSelect ||
            !quantityInput ||
            !productPriceInput ||
            !itemTotalInput
        ) {
            return 0;
        }

        if (
            deleteInput &&
            deleteInput.checked
        ) {

            productPriceInput.value =
                '0.00';

            itemTotalInput.value =
                '0.00';

            return 0;
        }

        const selectedOption =
            productSelect.options[
                productSelect.selectedIndex
            ];

        let productPrice = 0;

        if (selectedOption) {

            productPrice =
                toNumber(
                    selectedOption.getAttribute(
                        'data-price'
                    )
                );
        }

        const quantity =
            Math.max(
                0,
                parseInt(
                    quantityInput.value || '0',
                    10
                )
            );

        const itemTotal =
            productPrice * quantity;

        productPriceInput.value =
            productSelect.value
                ? productPrice.toFixed(2)
                : '0.00';

        itemTotalInput.value =
            productSelect.value
                ? itemTotal.toFixed(2)
                : '0.00';

        return itemTotal;
    }

    // =========================================================
    // WILAYA → COMMUNE
    // =========================================================

function updateCommunes() {

    const wilayaSelect =
        document.getElementById('id_wilaya');

    const communeSelect =
        document.getElementById('id_commune');

    if (!wilayaSelect || !communeSelect) {
        return;
    }

    const wilayaId =
        String(wilayaSelect.value || '');

    /*
     * نحفظ بيانات جميع البلديات الأصلية مرة واحدة.
     */
    if (!communeSelect._communeData) {

        communeSelect._communeData =
            Array.from(
                communeSelect.options
            )
            .filter(function (option) {
                return option.value !== '';
            })
            .map(function (option) {

                return {
                    value: option.value,

                    text:
                        option.textContent.trim(),

                    wilayaId:
                        String(
                            option.getAttribute(
                                'data-wilaya'
                            ) || ''
                        ),

                    deliveryPrice:
                        option.getAttribute(
                            'data-delivery-price'
                        ) || '0'
                };
            });
    }

    const communeData =
        communeSelect._communeData;

    /*
     * نمسح جميع البلديات الموجودة.
     */
    communeSelect.innerHTML = '';

    /*
     * الخيار الافتراضي.
     */
    const placeholder =
        document.createElement('option');

    placeholder.value = '';

    placeholder.textContent =
        '- Select an option -';

    communeSelect.appendChild(
        placeholder
    );

    /*
     * إذا لم يتم اختيار Wilaya.
     */
    if (!wilayaId) {

        communeSelect.value = '';

        communeSelect.disabled = true;

        updateDeliveryPrice();

        return;
    }

    /*
     * نضيف فقط البلديات التابعة
     * للولاية المختارة.
     */
    let matchingCommunes = 0;

    communeData.forEach(function (commune) {

        if (
            String(commune.wilayaId) !==
            wilayaId
        ) {
            return;
        }

        const option =
            document.createElement('option');

        option.value =
            commune.value;

        option.textContent =
            commune.text;

        option.setAttribute(
            'data-wilaya',
            commune.wilayaId
        );

        option.setAttribute(
            'data-delivery-price',
            commune.deliveryPrice
        );

        communeSelect.appendChild(
            option
        );

        matchingCommunes++;
    });

    /*
     * لا نحتفظ بأي Commune قديمة.
     */
    communeSelect.value = '';

    /*
     * إذا كانت هناك بلديات تابعة للولاية
     * نفعّل القائمة.
     */
    communeSelect.disabled =
        matchingCommunes === 0;

    /*
     * لا يوجد سعر حتى يتم اختيار Commune.
     */
    updateDeliveryPrice();
}
    // =========================================================
    // DELIVERY PRICE
    // =========================================================
    // السعر من Commune وليس Wilaya
    // =========================================================

    function updateDeliveryPrice() {

        const communeSelect =
            document.getElementById(
                'id_commune'
            );

        const deliveryPriceInput =
            document.getElementById(
                'id_delivery_price'
            );

        if (
            !communeSelect ||
            !deliveryPriceInput
        ) {
            return 0;
        }

        const selectedOption =
            communeSelect.options[
                communeSelect.selectedIndex
            ];

        let deliveryPrice = 0;

        if (
            selectedOption &&
            selectedOption.value
        ) {

            deliveryPrice =
                toNumber(
                    selectedOption.getAttribute(
                        'data-delivery-price'
                    )
                );
        }

        deliveryPriceInput.value =
            communeSelect.value
                ? deliveryPrice.toFixed(2)
                : '0.00';

        return deliveryPrice;
    }

    // =========================================================
    // TOTALS
    // =========================================================

    function updateTotals() {

        let productsTotal = 0;

        const rows =
            getProductRows();

        rows.forEach(
            function (row) {

                productsTotal +=
                    updateItem(row);
            }
        );

        const deliveryPrice =
            updateDeliveryPrice();

        const total =
            productsTotal +
            deliveryPrice;

        const productsTotalInput =
            document.getElementById(
                'id_products_total'
            );

        const totalPriceInput =
            document.getElementById(
                'id_total_price'
            );

        if (productsTotalInput) {

            productsTotalInput.value =
                productsTotal.toFixed(2);
        }

        if (totalPriceInput) {

            totalPriceInput.value =
                total.toFixed(2);
        }
    }

    // =========================================================
    // INITIALIZATION
    // =========================================================

    function initialize() {

        updateCommunes();

        updateTotals();

        document.addEventListener(
            'change',
            function (event) {

                if (
                    event.target.matches(
                        'select[name$="-product"]'
                    ) ||

                    event.target.matches(
                        'input[name$="-quantity"]'
                    ) ||

                    event.target.matches(
                        'input[name$="-DELETE"]'
                    ) ||

                    event.target.id ===
                        'id_wilaya' ||

                    event.target.id ===
                        'id_commune'
                ) {

                    /*
                     * عند تغيير الولاية:
                     * أعد بناء قائمة البلديات.
                     */
                    if (
                        event.target.id ===
                        'id_wilaya'
                    ) {

                        updateCommunes();
                    }

                    updateTotals();
                }
            }
        );

        document.addEventListener(
            'input',
            function (event) {

                if (
                    event.target.matches(
                        'input[name$="-quantity"]'
                    )
                ) {

                    updateTotals();
                }
            }
        );

        document.addEventListener(
            'formset:added',
            function () {

                updateTotals();
            }
        );
    }

    if (
        document.readyState ===
        'loading'
    ) {

        document.addEventListener(
            'DOMContentLoaded',
            initialize
        );

    } else {

        initialize();
    }

})();