document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementById('registrationForm');
    const messageEl = document.getElementById('formMessage');

    function showMessage(text, type = 'info') {
        messageEl.textContent = text;
        messageEl.style.color = type === 'error' ? '#b00020' : '#155724';
        messageEl.style.background = type === 'error' ? '#ffecec' : '#e6ffed';
        messageEl.style.border = type === 'error' ? '1px solid #f5c6cb' : '1px solid #c3e6cb';
        messageEl.style.padding = '0.6rem';
        messageEl.style.borderRadius = '4px';
    }

    function clearMessage() {
        messageEl.textContent = '';
        messageEl.style.background = 'transparent';
        messageEl.style.border = 'none';
        messageEl.style.padding = '';
    }

    form.addEventListener('submit', async function (e) {
        e.preventDefault();
        clearMessage();

        const submitBtn = form.querySelector('button[type="submit"]');
        const fullName = document.getElementById('fullName').value.trim();
        const email = document.getElementById('email').value.trim();
        const password = document.getElementById('password').value;
        const confirmPassword = document.getElementById('confirmPassword').value;
        const phone = document.getElementById('phone').value.trim();

        // Client-side validation
        if (!fullName || !email || !password) {
            showMessage('Full name, email and password are required.', 'error');
            return;
        }

        if (password !== confirmPassword) {
            showMessage('Passwords do not match!', 'error');
            return;
        }

        if (password.length < 6) {
            showMessage('Password must be at least 6 characters long!', 'error');
            return;
        }

        // Disable submit while processing
        submitBtn.disabled = true;
        submitBtn.textContent = 'Registering...';

        const payload = { fullName, email, password, phone };

        try {
            const res = await fetch('http://127.0.0.1:5000/api/register', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload),
            });

            const body = await res.json();

            if (res.status === 201) {
                showMessage('Registration successful! You can now log in.', 'info');
                form.reset();
            } else {
                // show server-provided error if available
                showMessage(body.error || 'Registration failed. Please try again.', 'error');
            }
        } catch (err) {
            console.error(err);
            showMessage('Network error. Make sure the backend server is running.', 'error');
        } finally {
            submitBtn.disabled = false;
            submitBtn.textContent = 'Register';
        }
    });
});