// components/Layout.js

// export default function Layout({children}) {
//     return (
//         <>
//             <header>
//                 <meta charSet="UTF-8"/>
//                 <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
//                 <title>Базовое меню</title>
//                 <link rel="stylesheet" href="src/styles/menu.css"/>
//             </header>
//             <body>
//             <header>
//                 <nav className="navbar">
//                     <div className="logo">Логотип</div>
//                     <div className="menu">
//                         <a href="/login" className="menu-button">Войти</a>
//                         <a href="/register" className="menu-button">Зарегистрироваться</a>
//                         <div className="profile-menu">
//                             <button className="profile-button" onClick={toggleProfileMenu}>
//                                 <img src="/profile-icon.png" alt="Профиль"/>
//                             </button>
//                             <div className="dropdown" id="profileDropdown">
//                                 <a href="/profile" className="dropdown-item">Профиль</a>
//                                 <a href="/logout" className="dropdown-item">Выйти</a>
//                             </div>
//                         </div>
//                     </div>
//                 </nav>
//             </header>
//             <main>{children}</main>
//             </body>
//         </>
//     );
// };