// components/Layout.js
import Head from 'next/head';

export default function Layout({ children }) {
    return (
        <>
            <Head>
                <meta charSet="UTF-8" />
                <meta name="viewport" content="width=device-width, initial-scale=1.0" />
                <title>Базовое меню</title>
                <link rel="stylesheet" href="src/styles/menu.css" />
            </Head>
            <body>
            <header>
                <nav className="navbar">
                    <div className="logo">Логотип</div>
                    <div className="menu">
                        <a href="/login" className="menu-button">Войти</a>
                        <a href="/register" className="menu-button">Зарегистрироваться</a>
                        <div className="profile-menu">
                            <button className="profile-button" onClick={toggleProfileMenu}>
                                <img src="/profile-icon.png" alt="Профиль" />
                            </button>
                            <div className="dropdown" id="profileDropdown">
                                <a href="/profile" className="dropdown-item">Профиль</a>
                                <a href="/logout" className="dropdown-item">Выйти</a>
                            </div>
                        </div>
                    </div>
                </nav>
            </header>
            <main>{children}</main>
            </body>
        </>
    );
};

function toggleProfileMenu() {
    const dropdown = document.getElementById('profileDropdown');
    if (dropdown) {
        dropdown.classList.toggle('show');
    }
}