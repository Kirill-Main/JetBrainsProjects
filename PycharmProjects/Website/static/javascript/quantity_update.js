function quantity_update(product_id)
{
    let num = $("#input" + product_id.toString()).val();

    if (!(/^-{0,1}\d+$/.test(num))) {
        $("#input" + product_id).val("1");
        num = 1;
    }

    $.ajax({
        url: "add/" + product_id.toString() + "/",
        type: "POST",
        data: $("#send_form" + product_id.toString()).serializeArray(),
        dataType: "json",
        success: function (data) {
            $("#cart_length").text("Корзина (" + data.cart_length + ")")
            $("#item" + product_id + "_total_price").text(data.item_total_price + ",0 руб")
            $("#cart_total_price").text(data.cart_total_price + ",0 руб")
        },
        error: function (error) {
            alert('Ошибка при изменении количества товара!')
        }
    });
}