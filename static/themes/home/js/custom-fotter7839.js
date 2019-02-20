$(document).ready(function() {
    $("#owl-demo").owlCarousel({
        autoPlay: true,
        items: 8,
        autoheight: true,
        lazyLoad: true,
        navigation: true,
        pagination: false,
        navigationText: ["", ""],
        itemsDesktop: [1170, 5],
        itemsDesktopSmall: [992, 4],
        itemsTablet: [768, 3],
        itemsMobile: [479, 2],
        slideSpeed: 200,
    });
});
$(document).ready(function() {
    $('#search_story').fsearch();
});
$(document).ready(function(e) {
    $('.mobile-menu').click(function(e) {
        $('.menu-primary').toggle();
    });
});
$(document).ready(function(e) {
    $('.name , .options').hover(function(e) {
        $('.options').toggle();
    });
});
jQuery(function($) {
    jQuery('#search_story').keypress(function(event) {
        if (event.which == 13) {
            if (document.frmsearch.search_style.value == "tentacgia")
                searchauthorpublic();
            else
                searchpublic();
        }
    })
});

function searchpublic() {
    window.location = _base_url_search + change_alias(document.frmsearch.search_story.value);
};

function searchauthorpublic() {
    window.location = _base_url_search_author + change_alias(document.frmsearch.search_story.value);
};
