// Password toggle visibility
document.addEventListener("DOMContentLoaded", function () {
  const passwordToggle = document.getElementById("passwordToggle");
  const passwordInput = document.getElementById("password");

  if (passwordToggle && passwordInput) {
    passwordToggle.addEventListener("click", function (e) {
      e.preventDefault();
      const eyeOpen = this.querySelector(".eye-open");
      const eyeClosed = this.querySelector(".eye-closed");

      if (passwordInput.type === "password") {
        passwordInput.type = "text";
        eyeOpen.style.display = "none";
        eyeClosed.style.display = "block";
      } else {
        passwordInput.type = "password";
        eyeOpen.style.display = "block";
        eyeClosed.style.display = "none";
      }
    });
  }

  // Validación básica del formulario
  const loginForm = document.getElementById("loginForm");
  if (loginForm) {
    loginForm.addEventListener("submit", function (e) {
      const email = document.getElementById("email").value.trim();
      const password = document.getElementById("password").value;
      let isValid = true;

      // Limpiar errores
      document.getElementById("emailError").textContent = "";
      document.getElementById("passwordError").textContent = "";

      // Validar email
      if (!email) {
        document.getElementById("emailError").textContent =
          "El email es requerido";
        isValid = false;
      } else if (!email.match(/^[^\s@]+@[^\s@]+\.[^\s@]+$/)) {
        document.getElementById("emailError").textContent =
          "Ingresa un email válido";
        isValid = false;
      }

      // Validar contraseña
      if (!password) {
        document.getElementById("passwordError").textContent =
          "La contraseña es requerida";
        isValid = false;
      }

      if (!isValid) {
        e.preventDefault();
      }
    });
  }
});
