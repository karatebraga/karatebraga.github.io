/* Shared navigation menu behavior (dropdown + responsive). */

let closeDropdown = function () {};

window.myFunction1 = function (num) {
  closeDropdown();

  const el = document.getElementById("myDropdown" + num);
  const parent = el ? el.closest(".dropdown") : null;
  if (el) {
    el.classList.toggle("show");
    if (parent) parent.classList.toggle("show", el.classList.contains("show"));
    closeDropdown = function () {
      el.classList.remove("show");
      if (parent) parent.classList.remove("show");
    };
  } else {
    closeDropdown = function () {};
  }
};

window.myFunction = function () {
  const x = document.getElementById("myTopnav");
  if (!x) return;

  if (x.className === "topnav") {
    x.className += " responsive";
  } else {
    x.className = "topnav";
  }
};

window.addEventListener("click", function (event) {
  if (event.target && event.target.closest && event.target.closest(".dropbtn")) {
    return;
  }
  const dropdowns = document.getElementsByClassName("dropdown-content");
  for (let i = 0; i < dropdowns.length; i++) {
    const openDropdown = dropdowns[i];
    if (openDropdown.classList.contains("show")) {
      openDropdown.classList.remove("show");
      const parent = openDropdown.closest(".dropdown");
      if (parent) parent.classList.remove("show");
    }
  }
});

