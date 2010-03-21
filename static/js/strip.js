
$(document).ready(function () {
    var isHoverAdded = false;
    var img$ = $('#strip img');
    var checkImageWidth = function (img$) {
        if (!isHoverAdded && img$.width() > 800) {
             $('#strip-nav')
                .hover(
                    function () { 
                        $('h2', this).next().slideDown(); 
                    },
                    function () {
                        $('h2', this).next().slideUp(); 
                    }
                )
                .find('h2', this).next().slideUp();
            isHoverAdded = true;
        }
    }
    if (img$.get(0).complete) { // This is intended to get it when the image comes from the cache.
        checkImageWidth(img$);
    }
    img$.load(checkImageWidth(img$));
});