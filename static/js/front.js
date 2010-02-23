/* Jazz up the index page smidgen */

    // We are loading the Twitter feed, so mark the heading accordingly.
    $('#cleanskies').prev('h2').addClass('loading');

/**
* Process a bunch of Twitter tweets.
*
* This is called via a SCRIPT tag at the bottom of the host page.
*/
function twitter(data) {
   $(document).ready(function () {
    var list = $('#cleanskies');
    $(list).prev('h2').removeClass('loading');
    for (var i = 0; i < data.results.length; ++i) {
        var tweet = data.results[i];
        var link = $('<a>').attr('href', 'http://twitter.com/cleanskies/statuses/' + tweet.id);
        
        // Can we use the image without making a mess?
        var src = 'http://urlimg.com/square/16/' + tweet.profile_image_url.slice(7);
        $('<img>').attr({src: src, alt: ''}).appendTo(link);
        
        // The text uses HTML escapes for ampersands etc.,
        // so I could just use jQueryâ€™s html method here,
        // but do I want to trust Twitter to be immune to XSS attacks?
        // Instead I reverse the HTML escaping jQueryâ€™s text method will apply.
        text = tweet.text.replace('&lt', '<').replace(/&amp;/, '&');
        $('<span>').text(text).appendTo(link);
        link.append(' ');
        
        // Convert the date of the tweet to a relative timestamp.
        var created = Date.parse(tweet.created_at);
        var nowish = new Date().getTime();
        var ago = nowish - created;
        ago = ago / 1000.0;
        if (ago > 48 * 3600) {
          ago = Math.round(ago / 24 / 3600) + '\xA0days ago';
        } else if (ago > 7200) {
          ago = Math.round(ago / 3600) + '\xA0hours ago';
        } else if (ago > 120) {
          ago = Math.round(ago / 60) + '\xA0minutes ago';
        } else  if (ago > 1.5) {
          ago = Math.round(ago) + '\xA0seconds ago';
        } else if (ago > 0.5) {
          ago = 'one second ago';
        } else {
          ago = 'just now';
        }
        $('<small>').attr('class', 'permalink').append($('<b>').text(ago)).appendTo(link);
        
        // Add the link as a list item.
        var item = $('<li>').attr('class', 'big');
        item.append(link);
        list.append(item);
    }   
 });
}

$(document).ready(function () {
    $.ajax({
        url: 'livejournal',
        dataType: 'json',
        success: function (data, textStatus, request) {
            if (data.success) {
                $('#livejournal').html(data.body);
            }
        }
    });
});