import {TokenInfo} from "@/jwt_api/schemes";

export const setTokens = (accessToken: string, refreshToken: string): void => {
    localStorage.setItem('accessToken', accessToken);
    localStorage.setItem('refreshToken', refreshToken);
};

export const setAccessToken = (accessToken: string): void => {
    localStorage.setItem('accessToken', accessToken);
};

export const getAccessToken = (): string | null => {
    return localStorage.getItem('accessToken');
};

export const getRefreshToken = (): string | null => {
    return localStorage.getItem('refreshToken');
};

export const clearTokens = (): void => {
    localStorage.removeItem('accessToken');
    localStorage.removeItem('refreshToken');
};

export const isAuthenticated = (): boolean => {
    return !!getAccessToken();
};