import axios from 'axios';
import {getAccessToken, getRefreshToken, setAccessToken, setTokens} from './crud_jwt_tokens';
import {TokenInfo, UserSchema, DecodedToken} from './schemes';
import BASE_URL from '@/constants';

const BASE_URL_JWT = `${BASE_URL}/jwt`;

const axiosInstance = axios.create({
    baseURL: BASE_URL_JWT,
    httpsAgent: new (require('https').Agent)({
        rejectUnauthorized: false
    })
});

function convert(data) {
    return new URLSearchParams(data).toString();
}

// const isTokenValid = (token: string): boolean => {
//     try {
//         const decoded: DecodedToken = jwtDecode(token);
//         const currentTime = Date.now() / 1000;
//         return decoded.exp > currentTime;
//     } catch (error) {
//         console.error('Error decoding token:', error);
//         return false;
//     }
// };


axiosInstance.interceptors.request.use(
    (config) => {
        const token = getAccessToken();
        if (token) {
            config.headers['Authorization'] = `Bearer ${token}`;
        }
        return config;
    },
    (error) => Promise.reject(error)
);


axiosInstance.interceptors.response.use(
    (response) => response,
    async (error) => {
        const originalRequest = error.config;

        if (error.response?.status === 401 && !originalRequest._retry) {
            originalRequest._retry = true;

            try {
                const { access_token } = await refreshToken();
                setAccessToken(access_token);
                originalRequest.headers['Authorization'] = `Bearer ${access_token}`;
                return axiosInstance(originalRequest);
            } catch (refreshError) {
                return Promise.reject(refreshError);
            }
        }

        return Promise.reject(error);
    }
);

export const register = async (userData: UserSchema): Promise<TokenInfo> => {
    const response = await axiosInstance.post('/register/', convert(userData));
    const data = response.data;
    setTokens(data.access_token, data.refresh_token);
    return data;
};

export const login = async (userData: UserSchema) => {

    await axiosInstance.post('/login/',
        convert(userData),
    ).then((response) => {
        const data = response.data;
        setTokens(data.access_token, data.refresh_token);
        return data;
    });
};

export const refreshToken = async (): Promise<TokenInfo> => {
    const refreshToken = getRefreshToken()
    const response = await axios.post(`${BASE_URL_JWT}/refresh/`, {}, {
        headers: {
            'Authorization': `Bearer ${refreshToken}`,
        }
    });
    return response.data;
};

export const getCurrentUser = async () => {
    const response = await axiosInstance.get('/users/me/');
    return response.data;
};

export const confirm_email = async (token: string) => {
    await axiosInstance.post(`/confirm-email/?token=${token}`,
    ).then((response) => {
        const data = response.data;
        setTokens(data.access_token, data.refresh_token);
        return data;
    });
};
