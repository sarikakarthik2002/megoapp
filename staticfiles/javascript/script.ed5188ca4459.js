let tl1=gsap.timeline()
tl1.from("#full",{
    y:-1000,
    duration:0.4,
    opacity:-1
})
tl1.from("#full #profilelink",{
    y:-400,
    opacity:0,
    duration:0.5,
    stagger:0.3,
})
tl1.from("#full #logout",{
    y:-400,
    opacity:0,
    duration:0.5,
    stagger:0.3,
})
tl1.from("#full #hi",{
    y:-100,
    duration:0.3,
})
// tl1.from("#full a",{
//     y:-100,
//     opacity:0,
//     duration:0.5,
//     stagger:0.3,
// })
// tl1.from("#full .i",{
//     y:-100,
//     opacity:0,
//     duration:0.5,
//     stagger:0.3,
// })
// tl1.from("#full #hi",{
//     y:-100,
//     duration:0.3,
// })
tl1.pause()
let menu = document.querySelector("#menu");
let isOpen = false;
menu.addEventListener("click", () => {
    if (isOpen) {
        tl1.reverse();
    } else {
        tl1.play();
    }
    isOpen = !isOpen;
});
