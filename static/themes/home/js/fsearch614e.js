(function($) {
    $.fn.fsearch = function() {
        var $searchInput = $(this);
        $searchInput.after('<div id="divResult"></div>');
        $resultDiv = $('#divResult');

        $searchInput.addClass('searchi');
        $resultDiv.html("<ul></ul><div id='search-footer' class='searchf'></div>");
        $old = '';
        var timesearchstory = null;
        $searchInput.keyup(function(e) {
            var q = $(this).val().trim();
            if (q != '') {
                if (q == $old || q.length < 3)
                    return;
                if (q == $old && e.keyCode != 13) {
                    if (e.keyCode == 27) {
                        $searchInput.val('');
                        $resultDiv.hide();
                    }
                    return;
                }
                $old = q;
                var current_index = $('.selected').index(),
                    $options = $resultDiv.find('.option'),
                    items_total = $options.length;
                $resultDiv.fadeIn();
                $resultDiv.find('#search-footer').html("<img src='static/themes/home/images/loadingimg.gif' alt='Collecting Data...'/>");
                if (timesearchstory != null) {
                    clearTimeout(timesearchstory);
                }
                timesearchstory = setTimeout(function() {
                    timesearchstory = null;
                    $.ajax({
                        contentType: "application/x-www-form-urlencoded; charset=UTF-8",
                        url: baseurljs + 'home_json_search',
                        type: 'POST',
                        data: "searchword=" + change_alias(q) + "&search_style=" + document.getElementById('search_style').value,
                        dataType: "json",
                        success: function(jsonResult) {
                            var str = '';
                            for (var i = 0; i < jsonResult.length; i++) {
                                str += '<li onclick="fmouseclick(\'' + jsonResult[i].nameunsigned + '\');" onmouseover="fmouseover(' + jsonResult[i].id + ');" id=' + jsonResult[i].id + ' class="option"><img class="profile_image" src="' + jsonResult[i].image + '" /><span style="width: 80%;white-space: nowrap;overflow: hidden;text-overflow: ellipsis;display: inline-block;" class="resultname" id="' + jsonResult[i].nameunsigned + '" >' + jsonResult[i].name + '<span style="font-size: 13px;opacity: 0.7;"> - by ' + jsonResult[i].author + '</span></span><br><span style="font-size: 12px;">' + jsonResult[i].lastchapter + '<span></span></span></li>';
                            }
                            $resultDiv.find('ul').empty().prepend(str);
                            if (jsonResult.length > 0)
                                $resultDiv.find('div#search-footer').text("Display first " + jsonResult.length + " results");
                            else
                                $resultDiv.find('div#search-footer').text("No matches found. Try a different search...");
                        }
                    });
                }, 1000);
            } else {
                $resultDiv.hide();
            }
        });
        jQuery(document).on("click", function(e) {
            var $clicked = $(e.target);
            if ($clicked.hasClass("searchi") || $clicked.hasClass("searchf")) {} else {
                $resultDiv.fadeOut();
            }
        });
        $searchInput.click(function() {
            var q = $(this).val();
            if (q != '') {
                $resultDiv.fadeIn();
            }
        });
    };
})(jQuery);

function fmouseover(id) {
    $(".option").removeClass("selected");
    document.getElementById(id).className += " selected";
}

function fmouseclick(nameunsigned) {
    if (nameunsigned != null) {
        url = baseurljs + 'manga/' + nameunsigned;
        window.location = url;
    }
}
