document.addEventListener('DOMContentLoaded', function () {
    const enrollButtons = document.querySelectorAll('.enroll-btn');
    enrollButtons.forEach(button => {
        button.addEventListener('click', function () {
            const courseId = this.getAttribute('data-course-id');
            fetch('/ajax/enroll',
                {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ course_id: courseId })
                })
                .then(response => response.json())
                .then(data => {
                    if (data.status === 'success') {
                        alert('Enrolled successfully!');
                    }
                    else {
                        alert('You need to log in first.');
                    }
                });
        });
    });
});


// تهيئة السمة عند التحميل
function initializeTheme() {
    const theme = getCookie('theme') || 'light';
    document.documentElement.setAttribute('data-theme', theme);
    updateThemeButton(theme);
}

// تبديل السمة
function toggleTheme() {
    const currentTheme = document.documentElement.getAttribute('data-theme');
    const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
    document.documentElement.setAttribute('data-theme', newTheme);
    setCookie('theme', newTheme, 365);
    updateThemeButton(newTheme);
}

// تحديث حالة الزر
function updateThemeButton(theme) {
    const icon = theme === 'dark' ? 'bi-moon' : 'bi-sun';
    const text = theme === 'dark' ? 'Dark Mode' : 'Light Mode';
    document.getElementById('themeToggle').innerHTML = `
                <i class="bi ${icon}"></i>
                <span class="d-none d-md-inline">${text}</span>
            `;
}

// دوال الكوكيز
function setCookie(name, value, days) {
    const date = new Date();
    date.setTime(date.getTime() + (days * 24 * 60 * 60 * 1000));
    document.cookie = `${name}=${value};expires=${date.toUTCString()};path=/`;
}

function getCookie(name) {
    const cookies = document.cookie.split(';');
    for (let cookie of cookies) {
        const [cookieName, cookieValue] = cookie.trim().split('=');
        if (cookieName === name) return cookieValue;
    }
    return null;
}

// الأحداث
document.getElementById('themeToggle').addEventListener('click', toggleTheme);
window.addEventListener('DOMContentLoaded', initializeTheme);
