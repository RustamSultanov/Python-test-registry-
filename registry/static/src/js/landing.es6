$(function() {
    $('body').on('click', '.anchor-link', function(e) {
        e.preventDefault();
        $("html, body").stop().animate({
            scrollTop: Math.round($(this.getAttribute('href')).offset().top) + 'px'
        }, 500);
    });

    $('form').submit(function (e) {
        let form = $(this);
        let url = form.attr('action');
        $.ajax({
            type: 'POST',
            url: url,
            data: form.serialize(), // serializes the form's elements.
            success: function(data)
            {
                $('.modal').modal('hide');
                $(data).modal('toggle');
            }
        });
        e.preventDefault();
    });
});