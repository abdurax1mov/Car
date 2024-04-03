const brand = document.querySelector(".brend")
const add_brand = document.querySelector(".addd")
const icon = document.querySelector(".she")
const add_car = document.querySelector(".add_car")
const add_ = document.querySelector(".add_cra")
const ico = document.querySelector(".ico")
brand.addEventListener("click", () => {
    add_brand.classList.toggle("add_flask")
})
icon.addEventListener("click", ()=>{
    add_brand.classList.remove("add_flask")
})
add_car.addEventListener("click", () => {
    add_.classList.toggle("add_fla")
})
ico.addEventListener("click", ()=>{
    add_.classList.remove("add_fla")
})
