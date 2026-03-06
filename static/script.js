let currentStep = 0
const steps = document.querySelectorAll(".step")

function nextStep() {

    steps[currentStep].classList.remove("active")

    currentStep++

    steps[currentStep].classList.add("active")

}