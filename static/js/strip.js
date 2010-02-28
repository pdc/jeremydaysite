
$(document).ready(function () {
    if ($('#strip img').width() > 800) {
        $('#strip-nav')
            .hover(
                function () { $('h2', this).next().slideDown(); },
                function () { $('h2', this).next().slideUp(); }
            )
            .find('h2', this).next().slideUp();
    }
});