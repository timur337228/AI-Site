import {JSX, useEffect, useState} from 'react';
import {useRouter} from 'next/router';
import {getCurrentUser} from '@/jwt_api/api';
import {isAuthenticated} from '@/jwt_api/crud_jwt_tokens';
import {UserSchema} from '../jwt_api/schemes';
import Layout from '@/layout/Layout'

const Index: () => (JSX.Element) = () => {
    const [user, setUser] = useState<UserSchema | null>(null);
    const router = useRouter();

    useEffect(() => {
        if (!isAuthenticated()) {
            router.push('/auth');
        } else {
            getCurrentUser()
                .then(setUser)
                .catch(() => router.push('/auth'));
        }
    }, [router]);

    if (!user) return <div>Загрузка</div>;

    return (
        <Layout>
            <h1>Добро пожаловать на главную страницу!</h1>
            <div>
                <h1>Dashboard</h1>
                <p>Welcome, {user.username}!</p>
                <p>Email: {user.email}</p>
            </div>
        </Layout>
    );
};

export default Index;