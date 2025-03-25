import { JSX, useEffect, useState } from 'react';
import { useRouter } from 'next/router';
import { login, register } from '@/jwt_api/api';
import { UserSchema } from './schemes';
import styles from '@/styles/auth/AuthForm.module.css';
import CheckEmailAnimation from '@/jwt_api/animations';

const AuthForm: ({ isLogin }: { isLogin: boolean }) => JSX.Element = ({ isLogin }) => {
    const [username, setUsername] = useState<string>('');
    const [email, setEmail] = useState<string>('');
    const [password, setPassword] = useState<string>('');
    const [showEmailCheck, setShowEmailCheck] = useState<boolean>(false);
    const [errorMessage, setErrorMessage] = useState<string>('');
    const [lastRegistrationTime, setLastRegistrationTime] = useState<number | null>(null);
    const [isButtonDisabled, setIsButtonDisabled] = useState<boolean>(false);
    const router = useRouter();
    const userData: UserSchema = { username, email, password };

    const handleRegSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setErrorMessage('');

        try {
            const data = await register(userData);
            setIsButtonDisabled(true);
            setTimeout(() => {
                setIsButtonDisabled(false);
            }, 60000);
            setShowEmailCheck(true);
        } catch (error: any) {
            setShowEmailCheck(false);
            if (error.response && error.response.status === 400 && error.response.data.detail === 'User authorized') {
                setErrorMessage('Пользователь уже зарегистрирован в системе.');
            } else {
                setErrorMessage('Произошла ошибка при регистрации. Пожалуйста, попробуйте снова.');
            }
        }
    };

    const handleLogSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        try {
            const data = await login(userData);
            router.push('/');
        } catch (error: any) {
            setErrorMessage('Неверный email или пароль.');
        }
    };

    useEffect(() => {
        setErrorMessage('');
        setShowEmailCheck(false);
    }, [isLogin]);

    const reg = 'Регистрация';
    const log = 'Вход';

    return (
        <div className={styles.container}>
            <form onSubmit={isLogin ? handleLogSubmit : handleRegSubmit} className={styles.form}>
                <h2 className={styles.title}>{isLogin ? log : reg}</h2>
                {!isLogin && (
                    <input
                        className={styles.input}
                        type="text"
                        placeholder="Username"
                        value={username}
                        onChange={(e) => setUsername(e.target.value)}
                    />
                )}
                <input
                    className={styles.input}
                    type="email"
                    placeholder="Почта"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                />
                <input
                    className={styles.input}
                    type="password"
                    placeholder="Пароль"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                />
                <button type="submit" className={styles.button}>
                    {isLogin ? log : reg}
                </button>
                {errorMessage && <div className="errorMessage">{errorMessage}</div>}
                <div style={{ display: 'flex', justifyContent: 'space-between', width: '100%' }}>
                    <a href='/forgot-password'>Забыл пароль</a>
                    <a href={isLogin ? '/registration' : '/login'}>
                        {isLogin ? "Нет аккаунта" : "Уже зарегистрирован"}
                    </a>
                </div>
            </form>
            {!errorMessage && showEmailCheck && <CheckEmailAnimation onClose={() => setShowEmailCheck(false)} />}
        </div>
    );
};

export default AuthForm;