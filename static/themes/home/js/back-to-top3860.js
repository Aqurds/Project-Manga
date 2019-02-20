$(document).ready(function() {
    $('body').append('<div id="top">Back to Top</div>');
    $(window).scroll(function() {
        if ($(window).scrollTop() != 0) {
            $('#top').fadeIn();
        } else {
            $('#top').fadeOut();
        }
    });
    $('#top').click(function() {
        $('body,html').animate({
            scrollTop: 0
        }, 300);
    });
});
