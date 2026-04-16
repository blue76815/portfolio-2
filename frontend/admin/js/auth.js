const API_BASE = 'http://localhost:8000';

function checkAuth() {
    const token = localStorage.getItem('token');
    if (!token) {
        window.location.href = '../login.html';
        return false;
    }
    return true;
}

function logout() {
    localStorage.removeItem('token');
    window.location.href = '../login.html';
}

async function authFetch(url, options = {}) {
    const token = localStorage.getItem('token');
    if (!token) {
        window.location.href = '../login.html';
        return;
    }

    const defaultHeaders = {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
    };

    options.headers = { ...defaultHeaders, ...options.headers };

    try {
        const res = await fetch(`${API_BASE}${url}`, options);
        if (res.status === 401) {
            localStorage.removeItem('token');
            window.location.href = '../login.html';
            return;
        }
        return await res.json();
    } catch (err) {
        showToast('網路錯誤，請確認後端服務已啟動', 'error');
        throw err;
    }
}

function showToast(message, type = 'success') {
    const existing = document.querySelector('.toast-notification');
    if (existing) existing.remove();

    const toast = document.createElement('div');
    toast.className = 'toast-notification';
    const bgColor = type === 'success' ? 'bg-green-500' : 'bg-red-500';
    toast.innerHTML = `
        <div class="fixed top-4 right-4 z-50 ${bgColor} text-white px-6 py-3 rounded-lg shadow-lg transition-all duration-300 transform translate-x-0">
            ${message}
        </div>
    `;
    document.body.appendChild(toast);

    setTimeout(() => {
        toast.remove();
    }, 3000);
}
