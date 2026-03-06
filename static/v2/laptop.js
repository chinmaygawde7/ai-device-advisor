let steps = document.querySelectorAll(".step")
let currentStep = 0

function nextStep() {

    let input = steps[currentStep].querySelector("input[type='hidden']")

    if (input.value === "") {
        alert("Please select option")
        return
    }

    steps[currentStep].classList.remove("active")
    currentStep++
    steps[currentStep].classList.add("active")

}

document.querySelectorAll(".card").forEach(card => {

    card.addEventListener("click", function () {

        let group = this.parentElement
        let input = group.nextElementSibling

        group.querySelectorAll(".card").forEach(c => c.style.border = "none")

        this.style.border = "2px solid white"

        input.value = this.dataset.value

    })

})