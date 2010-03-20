
$(document).ready(function () {
    var isImageWidthChecked = false;
    var img$ = $('#strip img');
    var checkImageWidth = function (img$) {
        if (!isImageWidthChecked) {
            if (img$.width() > 800) {
                $('#strip-nav')
                    .hover(
                        function () { $('h2', this).next().slideDown(); },
                        function () { $('h2', this).next().slideUp(); }
                    )
                    .find('h2', this).next().slideUp();
            }
            isImageWidthChecked = true;
        }
    }
    if (img$.get().complete) {
        checkImageWidth(img$);
    }
    img$.load(checkImageWidth(img$));
});