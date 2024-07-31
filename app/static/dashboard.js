document.addEventListener('DOMContentLoaded', function () {
  const checkboxes = document.querySelectorAll('.show-password-checkbox');
  checkboxes.forEach(checkbox => {
    checkbox.addEventListener('change', function () {
      const row = this.closest('tr');
      const sensitiveInputs = row.querySelectorAll('.sensitive-input');
      sensitiveInputs.forEach(input => {
        input.type = this.checked ? 'text' : 'password';
      });
    });
  });
});

// Toggle Dark Mode
const toggleDarkModeButton = document.getElementById('toggle-dark-mode');

// Check local storage for dark mode preference
if (localStorage.getItem('theme') === 'dark') {
  document.documentElement.classList.add('dark');
} else {
  document.documentElement.classList.remove('dark');
}

toggleDarkModeButton.addEventListener('click', () => {
  document.documentElement.classList.toggle('dark');
  
  // Save the user's preference in local storage
  if (document.documentElement.classList.contains('dark')) {
    localStorage.setItem('theme', 'dark');
  } else {
    localStorage.setItem('theme', 'light');
  }
});


document.querySelectorAll('.copy-button').forEach(button => {
  button.addEventListener('click', function() {
      const textToCopy = this.getAttribute('data-id');
      navigator.clipboard.writeText(textToCopy).then(function() {
          console.log('Text copied to clipboard');
      }).catch(function(error) {
          console.error('Error copying text: ', error);
      });
  });
});