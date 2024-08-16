$(document).ready(function () {
    $.ajax({
        url: 'http://127.0.0.1:8000/numbers/',
        method: 'GET',
        success: function (result) {
            const numbers = result.numbers;
            const institutes = result.institutes;
            showTables(institutes, numbers);
            $('#search-input').on('input', function () {
                const filteredData = filterData(institutes, numbers);
                showTables(filteredData.institutes, filteredData.numbers);
            })
            $('#filter-form').on('change', function () {
                const filteredData = filterData(institutes, numbers);
                showTables(filteredData.institutes, filteredData.numbers);
            })
        },
        error: function (error) {
            console.error("Ошибка при выполнении запроса на numbers: ", error);
        }
    })

})

function filterData(institutes, numbers) {
    let search = $('#search-input').val().toLowerCase();
    const filtersValues = [];
    const queryConditions = [];
    let filteredNumbers = [];
    $('#filter-form input[name="filter"]:checked').each(function () {
        filtersValues.push($(this).val());
    });
    if (filtersValues.length <= 0) {
        $('#filter-form input[name="filter"]').each(function () {
            filtersValues.push($(this).val());
        });
    }
    if (search.length > 0) {
        filtersValues.forEach(function (field) {
            if (field === 'institute') {
                institutes.filter(function (item) {
                    return (item.name && item.name.toLowerCase().includes(search));
                })
            } else {
                queryConditions.push(function (item) {
                    return item[field] && item[field].toLowerCase().includes(search);
                });
            }
        });
        filteredNumbers = numbers.filter(function (item) {
            return queryConditions.some(function (condition) {
                return condition(item);
            });
        })
    } else {
        filteredNumbers = numbers;
    }
    return {'institutes': institutes, 'numbers': filteredNumbers};
}

function showTables(institutes, filteredNumbers) {
    const result = []
    institutes.forEach(function (institute) {
        const instituteNumbers = filteredNumbers.filter(function (item) {
            return (item.institute__name && item.institute__name === institute.name);
        })
        if (instituteNumbers.length <= 0) {
            return
        }
        result.push({'institute': institute.name, 'numbers': instituteNumbers});
    })


    const $tablesContainer = $('#tables');
    $tablesContainer.empty();

    result.forEach(function (data) {
        // Создание таблицы
        var $table = $('<table>', {class: 'table text-center'});

        // Создание заголовка таблицы
        var $thead = $('<thead>', {
            role: 'button',
            'data-bs-toggle': 'collapse',
            class: 'accordion-toggle thead-aues',
            'data-bs-target': '#table-' + data.institute.id
        }).append(
            $('<tr>', {class: 'row'}).append(
                $('<th>', {scope: 'col', class: 'col'}).text(data.institute)
            )
        );

        // Добавление заголовка в таблицу
        $table.append($thead);

        // Создание тела таблицы
        var $tbody = $('<tbody>', {
            'data-toggle': 'collapse',
            id: 'table-' + data.institute.id,
            class: 'accordion-body show'
        });

        // Заполнение строк в теле таблицы
        data.numbers.forEach(function (number) {
            var $tr = $('<tr>', {class: 'row'}).append(
                $('<th>', {class: 'col-md-1 col-12 d-md-table-cell d-flex justify-content-between align-middle'}).text(number.local_number),
                $('<th>', {class: 'col-md-4 col-12 d-md-table-cell d-flex justify-content-between align-middle'}).text(number.name),
                $('<th>', {class: 'col-md-3 col-12 d-md-table-cell d-flex justify-content-between align-middle'}).text(number.position),
                $('<th>', {class: 'col-md-1 col-12 d-md-table-cell d-flex justify-content-between align-middle'}).text(number.cabinet),
                $('<th>', {class: 'col-md-3 col-12 d-md-table-cell d-flex justify-content-between align-middle'}).text(number.email)
            );
            $tbody.append($tr);
        });

        // Добавление тела таблицы в таблицу
        $table.append($tbody);

        // Добавление таблицы в контейнер
        $tablesContainer.append($table);
    });
}