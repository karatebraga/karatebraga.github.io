/* Shared navigation menu behavior (dropdown + responsive). */

let closeDropdown = function () {};

window.myFunction1 = function (num) {
  closeDropdown();

  const el = document.getElementById("myDropdown" + num);
  if (el) {
    el.classList.toggle("show");
    closeDropdown = function () {
      el.classList.remove("show");
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
  if (!event.target || !event.target.matches || !event.target.matches(".dropbtn")) {
    const dropdowns = document.getElementsByClassName("dropdown-content");
    for (let i = 0; i < dropdowns.length; i++) {
      const openDropdown = dropdowns[i];
      if (openDropdown.classList.contains("show")) {
        openDropdown.classList.remove("show");
      }
    }
  }
});

