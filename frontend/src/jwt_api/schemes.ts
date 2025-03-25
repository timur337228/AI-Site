export interface TokenInfo {
    access_token: string;
    refresh_token: string;
    token_type: string;
}

export interface UserSchemaLogin {
    email: string;
    password: string;
}

export interface UserSchema extends UserSchemaLogin {
    username: string;
}

export interface DecodedToken {
    exp: number;
    sub?: string;
}

export default interface HomeProps {
    user: UserSchema | null;
}

export default interface HomeAuth extends HomeProps{
    isLogin?: boolean;
}

