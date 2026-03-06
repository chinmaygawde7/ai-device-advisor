document.addEventListener("DOMContentLoaded", function () {

    let steps = document.querySelectorAll(".step")
    let currentStep = 0
    let progress = document.getElementById("progress-bar")

    function updateProgress() {
        let percent = (currentStep / (steps.length - 1)) * 100
        progress.style.width = percent + "%"
    }

    window.nextStep = function () {

        let input = steps[currentStep].querySelector("input[type='hidden']")
        if (input && input.value === "") {
            alert("Please select an option")
            return
        }

        steps[currentStep].classList.remove("active")
        currentStep++

        if (currentStep < steps.length) {
            steps[currentStep].classList.add("active")
        }

        updateProgress()
    }


    // CARD SELECTION

    document.querySelectorAll(".card-group").forEach(group => {

        let hiddenInput = group.nextElementSibling

        group.querySelectorAll(".card").forEach(card => {

            card.addEventListener("click", function () {

                // OS SELECTION
                if (group.classList.contains("os-group")) {

                    group.querySelectorAll(".card").forEach(c => c.classList.remove("selected"))

                    card.classList.add("selected")

                    hiddenInput.value = card.dataset.value

                    handleOSChange(card.dataset.value)

                }

                // BRAND MULTI SELECT
                else if (group.classList.contains("brand-group")) {

                    card.classList.toggle("selected")

                    let selected = []

                    group.querySelectorAll(".card.selected").forEach(c => {
                        selected.push(c.dataset.value)
                    })

                    hiddenInput.value = selected.join(",")

                }

                // NORMAL SINGLE SELECT
                else {

                    group.querySelectorAll(".card").forEach(c => c.classList.remove("selected"))

                    card.classList.add("selected")

                    hiddenInput.value = card.dataset.value

                }

            })

        })

    })


    // OS BASED BRAND FILTER

    function handleOSChange(os) {

        let apple = document.querySelectorAll(".apple-brand")
        let android = document.querySelectorAll(".android-brand")

        let brandInput = document.querySelector("input[name='brand']")

        // reset selections
        document.querySelectorAll(".brand").forEach(card => {
            card.classList.remove("selected")
        })

        if (os === "iOS") {

            android.forEach(card => card.style.display = "none")

            apple.forEach(card => {
                card.style.display = "block"
                card.classList.add("selected")
            })

            brandInput.value = "Apple"

        }

        if (os === "Android") {

            apple.forEach(card => card.style.display = "none")

            android.forEach(card => card.style.display = "block")

            brandInput.value = ""

        }

    }

})