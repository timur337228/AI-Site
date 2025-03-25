import HomeAuth from '@/jwt_api/schemes';
import Home,  from '@/jwt_api/render';
import { getServerSideProps } from '@/jwt_api/render';
import React from "react";

export const loginUser: React.FC<HomeAuth> = ({user}) => {
    return <Home user={user} isLogin={true}></Home>;
}
export { getServerSideProps };
export default loginUser;