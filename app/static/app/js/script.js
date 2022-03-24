let delay = 1000;
let autoPlay = true;

$('#slider1, #slider2, #slider3').owlCarousel({
    loop: true,
    margin: 20,
    responsiveClass: true,
    responsive: {
        0: {
            items: 1,
            nav: false,
            autoplay: autoPlay,
            autoplayTimeout: delay,
        },
        600: {
            items: 3,
            nav: true,
            autoplay: autoPlay,
            autoplayTimeout: delay,
        },
        1000: {
            items: 5,
            nav: true,
            loop: true,
            autoplay: autoPlay,
            autoplayTimeout: delay,
        }
    }
})
