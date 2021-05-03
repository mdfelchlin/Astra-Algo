$(window).scroll(function () {
    var scroll = $(window).scrollTop();
    $(".zoom img").css({
        width: (100 + scroll / 20) + "%",
        height: (100 + scroll / 40) + "%"
    })
})