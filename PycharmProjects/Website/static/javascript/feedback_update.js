function feedback_update(product_id)
{
    if (!$("textarea").val()) {
        $("h5.text-danger").text("Заполните поле для отзыва");
        return;
    }

    $.ajax({
        url: "/about/" + product_id.toString() + "/",
        type: "POST",
        data: $("#send_form").serializeArray(),
        dataType: "json",
        success: function (data) {
            $("#count").html("<h3 style=\"margin-top: 20px;\" id=\"count\">Отзывы (" + data.feedbacks_count + ")</h3>")
            if (data.feedback.is_recommended)
                $("#add").prepend("<span class=\"font-weight-bold lead\">" + data.feedback.username + "</span>\n" +
                    "                    <span class=\"text-muted text-sm\">" + data.feedback.published + "</span>\n" +
                    "                    <p class=\"text-success\">Рекомендует</p>\n" +
                    "                    <p>" + data.feedback.content + "</p>\n" +
                    "                    <hr>\n" +
                    "                    </div>")
            else
                $("#add").prepend("<span class=\"font-weight-bold lead\">" + data.feedback.username + "</span>\n" +
                    "                    <span class=\"text-muted text-sm\">" + data.feedback.published + "</span>\n" +
                    "                    <p class=\"text-danger\">Не рекомендует</p>\n" +
                    "                    <p>" + data.feedback.content + "</p>\n" +
                    "                    <hr>\n" +
                    "                    </div>")
            $("#clear_form").click();
        },
        error: function () {
            alert('Ошибка при добавлении отзыва!')
        }
    });
}