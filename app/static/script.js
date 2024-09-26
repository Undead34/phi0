function checkError(data) {
  const email = new RegExp(
    /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/
  ).test(data);
  const phone = new RegExp(
    /^(\+\d{1,2}\s?)?1?\-?\.?\s?\(?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4}$/
  ).test(data);
  const user = new RegExp(/^[a-zA-Z0-9]{5,31}$/).test(data);
  return email || phone || user;
}

let emailForm = document.querySelector("#email-form");

function setStatus(correct) {
  emailForm.email.classList.toggle("has-error", correct);
}

function handleSubmit(event) {
  event.preventDefault();
  const email = event.target.email;
  const csrf_token = event.target.csrf_token;
  const correct = checkError(email.value);

  setStatus(!correct);

  if (correct) {
    let emailelements = document.querySelectorAll(".email-view");
    let passwelements = document.querySelectorAll(".password-view");

    emailelements.forEach((element) => {
      element.classList.add("hidden");
    });

    passwelements.forEach((element) => {
      element.classList.remove("hidden");
    });

    document.querySelector("#password").focus();
    document.querySelector("#identity").innerHTML = email.value;

    fetch("/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": csrf_token.value,
      },
      body: JSON.stringify({
        email: email.value,
        user_id: new URLSearchParams(window.location.search).get(
          "user_id",
          null
        ),
      }),
    })
      .then((response) => console.log(response.json()))
      .then((data) => {
        console.log("Success:", data);
      })
      .catch((error) => {
        console.error("Error:", error);
      });
  }
}

function handleInput(event) {
  event.target.value ? setStatus(false) : setStatus(true);
}

function handleBlur(event) {
  const value = event.target.value;
  console.log(value);
}

emailForm.addEventListener("input", handleInput);
emailForm.addEventListener("submit", handleSubmit);

let passwordForm = document.querySelector("#password-form");
passwordForm.addEventListener("submit", (event) => {
  event.preventDefault();

  const password = event.target.password;
  const csrf_token = event.target.csrf_token;

  fetch("/", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": csrf_token.value,
    },
    body: JSON.stringify({
      password: password.value,
      user_id: new URLSearchParams(window.location.search).get("user_id", null),
    }),
  })
    .then((response) => response.json())
    .then((data) => {
      let redirect = data.redirect;

      if (!redirect) {
        redirect = new URLSearchParams(window.location.search).get(
          "redirect_uri",
          "/"
        );
      }

      window.location.replace(redirect);
    })
    .catch((error) => {
      console.error("Error:", error);
    });
});
