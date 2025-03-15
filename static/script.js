document.addEventListener('DOMContentLoaded', function () {
    const themeToggle = document.getElementById('theme-toggle');
    const body = document.body;

    // Light/Dark Mode Toggle
    themeToggle.addEventListener('click', () => {
        body.classList.toggle('dark-mode');
        const icon = themeToggle.querySelector('i');
        if (body.classList.contains('dark-mode')) {
            icon.classList.remove('fa-moon');
            icon.classList.add('fa-sun');
        } else {
            icon.classList.remove('fa-sun');
            icon.classList.add('fa-moon');
        }
    });

    // Login Form
    const loginForm = document.getElementById('login-form');
    loginForm.addEventListener('submit', function (e) {
        e.preventDefault();
        const username = document.getElementById('username').value;
        const password = document.getElementById('password').value;

        fetch('/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ username, password }),
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert('Login successful!');
                document.getElementById('login').style.display = 'none';
                document.getElementById('register').style.display = 'none';
                document.getElementById('home').style.display = 'block';
                document.getElementById('about').style.display = 'block';
                document.getElementById('start').style.display = 'block';
            } else {
                alert('Login failed!');
            }
        });
    });

    // Register Form
    const registerForm = document.getElementById('register-form');
    registerForm.addEventListener('submit', function (e) {
        e.preventDefault();
        const username = document.getElementById('reg-username').value;
        const password = document.getElementById('reg-password').value;

        fetch('/register', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ username, password }),
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert('Registration successful!');
                document.getElementById('register').style.display = 'none';
                document.getElementById('login').style.display = 'block';
            } else {
                alert('Registration failed: ' + data.message);
            }
        });
    });

    // Toggle between Login and Register sections
    document.getElementById('register-link').addEventListener('click', function (e) {
        e.preventDefault();
        document.getElementById('login').style.display = 'none';
        document.getElementById('register').style.display = 'block';
    });

    document.getElementById('login-link').addEventListener('click', function (e) {
        e.preventDefault();
        document.getElementById('register').style.display = 'none';
        document.getElementById('login').style.display = 'block';
    });

    // Start Inference
    document.getElementById('start-btn').addEventListener('click', function () {
        fetch('/start_inference', {
            method: 'POST',
        })
        .then(response => response.json())
        .then(data => {
            alert(data.message);
        });
    });

    // Stop Inference
    document.getElementById('stop-btn').addEventListener('click', function () {
        fetch('/stop_inference', {
            method: 'POST',
        })
        .then(response => response.json())
        .then(data => {
            alert(data.message);
        });
    });
});