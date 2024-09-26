function checkError(data) {
  const email = new RegExp(
    /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/
  ).test(data);
  const phone = new RegExp(/^(\+\d{1,2}\s?)?1?\-?\.?\s?\(?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4}$/).test(data);
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
  const correct = checkError(email.value);

  setStatus(!correct);

  if (correct) {
    console.log(email);
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
