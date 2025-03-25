import { useEffect } from 'react';
import { useRouter } from 'next/router';
import Link from 'next/link';
import { confirm_email } from "@/jwt_api/api";

const ConfirmationPage = () => {
    const router = useRouter();
    const { token } = router.query;

    useEffect(() => {
        if (token) {
            confirm_email(token as string)
                .then(() => {
                });
        }
    }, [token]);

    return (
        <div>
            {token ? (
                <Link href={{ pathname: '/confirm_email', query: { token } }}>
                    <div>Ваш Email успешно подтверждён</div>
                </Link>
            ) : (
                <div>Токен отсутствует</div>
            )}
        </div>
    );
};

export default ConfirmationPage;