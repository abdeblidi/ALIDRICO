document.addEventListener('DOMContentLoaded', function () {

    const categoryField = document.getElementById('id_category');
    const subcategoryField = document.getElementById('id_subcategory');

    if (!categoryField || !subcategoryField) {
        return;
    }

    function filterSubcategories() {

        const categoryId = categoryField.value;
        const options = subcategoryField.options;

        for (let i = 0; i < options.length; i++) {

            const option = options[i];

            // Keep empty option visible
            if (!option.value) {
                option.hidden = false;
                continue;
            }

            const optionCategory = option.dataset.category;

            option.hidden = (
                !categoryId ||
                optionCategory !== categoryId
            );
        }

        // If currently selected subcategory no longer belongs
        // to the selected category, clear it.
        const selectedOption =
            subcategoryField.options[subcategoryField.selectedIndex];

        if (
            selectedOption &&
            selectedOption.value &&
            selectedOption.hidden
        ) {
            subcategoryField.value = '';
        }
    }

    categoryField.addEventListener(
        'change',
        filterSubcategories
    );

    // Run once when editing an existing product.
    filterSubcategories();
});