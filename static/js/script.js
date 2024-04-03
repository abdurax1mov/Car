new WOW().init();

const img = document.querySelectorAll(".img")
const body = document.querySelector(".img1")
const next = document.querySelector(".next")
const prev = document.querySelector(".prev")
console.log(img.length)
let input = 0;

function chang() {
    if (input > img.length - 1) {
        input = 0;
    } else if (input < 0) {
        input = img.length - 1
    }
    body.style.transform = `translateX(${-input * 380}px)`
}

next.addEventListener("click", () => {
    console.log(img.length)
    input++
    chang()
})
prev.addEventListener("click", () => {
    input--
    chang()
})