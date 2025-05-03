document.addEventListener('DOMContentLoaded', () => {
    const themeSwitch = document.getElementById('checkbox');
    const body = document.body;

    // Check for saved theme preference or system preference
    const savedTheme = localStorage.getItem('theme');
    const prefersDarkMode = window.matchMedia('(prefers-color-scheme: dark)');

    // Set initial theme
    if (savedTheme === 'dark' || (!savedTheme && prefersDarkMode.matches)) {
        body.classList.add('dark-theme');
        themeSwitch.checked = true;
    }

    // Theme toggle functionality
    themeSwitch.addEventListener('change', () => {
        if (themeSwitch.checked) {
            body.classList.add('dark-theme');
            localStorage.setItem('theme', 'dark');
        } else {
            body.classList.remove('dark-theme');
            localStorage.setItem('theme', 'light');
        }
    });

    // Listen for system theme changes
    prefersDarkMode.addListener((e) => {
        if (e.matches) {
            body.classList.add('dark-theme');
            themeSwitch.checked = true;
            localStorage.setItem('theme', 'dark');
        } else {
            body.classList.remove('dark-theme');
            themeSwitch.checked = false;
            localStorage.setItem('theme', 'light');
        }
    });

    // Contact form handling (if contact form exists)
    const form = document.getElementById('contact-form');
    if (form) {
        form.addEventListener('submit', function(event) {
            event.preventDefault();

            const name = document.getElementById('name').value;
            const email = document.getElementById('email').value;
            const message = document.getElementById('message').value;

            if (name && email && message) {
                alert('Thank you for your message!');
                form.reset();
            } else {
                alert('Please fill out all fields.');
            }
        });
    }
});