$(document).ready(function () {
    // Because the logo overlaps the links in the header,
    // they don’t always work properly. So add invisible duplicates...
    var overlay$ = $('<div>').addClass('tabs-overlay').appendTo($('#top'));
    $('#tabs li *').each(function (i) {
        var isLink = $(this).is('a');
        if (isLink) {
            var link$ = $('<a>').attr('href', this.href).text('\xA0').appendTo(overlay$);
            link$.css('left', link$.width() * i);
        }
    });
});