import type {AppProps} from 'next/app';
import { useEffect } from 'react';
import '@/styles/global.css';

export default function MyApp({Component, pageProps}: AppProps) {
    useEffect(() => {
        const link = document.createElement('link');
        link.href = 'https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600&display=swap';
        link.rel = 'stylesheet';
        document.head.appendChild(link);
    }, []);
    return (
        <Component {...pageProps} />
    );
}