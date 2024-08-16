$(document).ready(function () {
    $.ajax({
        url: 'http://127.0.0.1:8000/numbers/',
        method: 'GET',
        success: function (result) {
            const numbers = result.numbers;
            showTables(numbers);
            $('#search-input').on('input', function () {
                let search = $(this).val().toLowerCase();
                const filteredNumbers = numbers.filter(function (number) {
                    return (number && number.name.toLocaleLowerCase().includes(search));
                })
                showTables(filteredNumbers);
            })
        },
        error: function (error) {
            console.error("Ошибка при выполнении запроса на numbers: ", error);
        }
    })
});

function showTables(data) {
    var tableBody = $('#result_list');
    tableBody.empty(); // Clear any existing rows

    if (data.length > 0) {
        $.each(data, function (index, obj) {
            var row = `
                    <tr>
                        <td>${obj.name}</td>
                        <td>${obj.position}</td>
                        <td>${obj.email}</td>
                        <td>
                            <a href="/admin/app/numbers/${obj.id}/change/" class="btn btn-secondary mb-2 btn-sm">Редактировать</a>
                            <a href="/admin/app/numbers/${obj.id}/delete/" class="btn btn-danger btn-sm">Удалить</a>
                        </td>
                    </tr>
                `
            tableBody.append(row);
        });
    } else {
        tableBody.append('<tr><td colspan="4">No data available</td></tr>');
    }
}