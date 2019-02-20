// Chapte-list jumping code
function movetolistchapter() {
    var divPosition = $('#chapter').offset();
    $('html, body').animate({
        scrollTop: divPosition.top
    }, 300);
};
// Chapter-list jumping code end


// Show-more & Show-less content button code
function expandcontent() {
    document.getElementById('noidungm').style.maxHeight = 'none';
    document.getElementById("content_more").style.display = "none";
    document.getElementById("content_less").style.display = "initial";
}

function lesscontent() {
    document.getElementById('noidungm').style.maxHeight = '300px';
    document.getElementById("content_less").style.display = "none";
    document.getElementById("content_more").style.display = "initial";
}
$(document).ready(function(e) {
    $('.content_more').click(function(e) {
        expandcontent();
        var date = new Date();
        date.setTime(date.getTime() + (30 * 24 * 60 * 60 * 1000));
        $.cookie("content_more", "more", {
            expires: date,
            path: "/"
        });
    });
    $('.content_less').click(function(e) {
        lesscontent();
        var date = new Date();
        date.setTime(date.getTime() + (30 * 24 * 60 * 60 * 1000));
        $.cookie("content_more", "less", {
            expires: date,
            path: "/"
        });
    });
    $(window).bind("load", function() {
        if ($.cookie("content_more") == "less" || tooltypejs == 'mobile') {
            lesscontent();
        }
    });
});
// Show-more & Show-less content button code end



$(document).ready(function() {
    if (!$.cookie("vote_" + $postid)) {
        $('.rate_row').starwarsjs({
            stars: 5,
            count: 1,
            default_stars: $votepointstar,
            on_select: function(datares) {
                $('.rate_row_result').starwarsjs({
                    stars: 5,
                    count: 1,
                    default_stars: datares,
                    disable: 0
                });
                document.getElementById("rate_row").style.display = "none";
                document.getElementById("rate_row_cmd").innerHTML = "Thanks for your vote!";
                var date = new Date();
                date.setTime(date.getTime() + (3 * 60 * 60 * 1000));
                $.cookie("vote_" + $postid, "voted", {
                    expires: date,
                    path: "/"
                });
                jQuery.ajax({
                    type: 'POST',
                    data: {
                        'rate': datares,
                        'idmanga': $postid
                    },
                    url: $ddrate
                });
            }
        });
    } else {
        $('.rate_row').starwarsjs({
            stars: 5,
            count: 1,
            default_stars: $votepointstar,
            disable: 0
        });
    }
});

function addnote() {
    if ($lg == false) {
        alert('Please login to use this function !');
        return;
    }
    jQuery.ajax({
        url: $ddbookmark,
        type: "POST",
        data: {
            'storyid': $postid
        },
        success: function(data) {
            $("#Bookmark").html("Followed");
        },
        error: function(xhr) {}
    });
};
