document.addEventListener("DOMContentLoaded", function () {
    console.log("Script loaded!");

    // Validate emergency contact number (must be 10 digits)
    const emergencyContactInput = document.getElementById("emergency_contact");
    if (emergencyContactInput) {
        emergencyContactInput.addEventListener("input", function () {
            const regex = /^[0-9]{0,10}$/;
            if (!regex.test(this.value)) {
                this.value = this.value.slice(0, -1);
            }
        });
    }

    // Toggle allergies input field based on dropdown selection
    const allergiesDropdown = document.getElementById("allergies_select");
    const allergiesInput = document.getElementById("allergies_input");
    if (allergiesDropdown && allergiesInput) {
        allergiesDropdown.addEventListener("change", function () {
            if (this.value === "Yes") {
                allergiesInput.style.display = "block";
            } else {
                allergiesInput.style.display = "none";
                allergiesInput.value = "";
            }
        });
    }

    // Toggle differently-abled input field based on dropdown selection
    const disabledDropdown = document.getElementById("disabled_select");
    const disabledInput = document.getElementById("disabled_input");
    if (disabledDropdown && disabledInput) {
        disabledDropdown.addEventListener("change", function () {
            if (this.value === "Yes") {
                disabledInput.style.display = "block";
            } else {
                disabledInput.style.display = "none";
                disabledInput.value = "";
            }
        });
    }

    // Copy UID to clipboard when clicked
    const uidElements = document.querySelectorAll(".uid");
    uidElements.forEach((uid) => {
        uid.addEventListener("click", function () {
            navigator.clipboard.writeText(this.textContent).then(() => {
                alert("UID copied to clipboard!");
            });
        });
    });

    // Aztec Code Generator
    const generateAztecBtn = document.getElementById("generate_aztec");
    if (generateAztecBtn) {
        generateAztecBtn.addEventListener("click", function () {
            const uid = document.getElementById("uid").textContent;
            if (uid) {
                fetch(`/generate_aztec?uid=${uid}`)
                    .then((response) => response.json())
                    .then((data) => {
                        if (data.success) {
                            document.getElementById("aztec_code").src = data.image_url;
                        } else {
                            alert("Failed to generate Aztec Code!");
                        }
                    });
            }
        });
    }
});