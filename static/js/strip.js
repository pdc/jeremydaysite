

function checkImageWidth(img$) {
    if (img$.width() > 800) {
         $('#strip-nav:not(.hover-added)')
            .hover(
                function () { 
                    $('h2', this).next().slideDown(); 
                },
                function () {
                    $('h2', this).next().slideUp(); 
                }
            )
            .find('h2', this).next().slideUp()
            .addClass('hover-added');
    }
}

$(document).ready(function () {    
    var img$ = $('#strip img');
    if (img$.get(0).complete) { // This is intended to get it when the image comes from the cache.
        checkImageWidth(img$);
        img$.addClass('checked-complete');
    }
});

$('#strip img').load(function () {
    checkImageWidth($(this));
    $(this).addClass('checked-loaded');
});