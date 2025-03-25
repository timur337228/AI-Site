import type { NextConfig } from "next";

const fs = require('fs');
const path = require('path');
const main_dir = 'src'

const certPath = path.join(__dirname, `${main_dir}/certs`);
const key = fs.readFileSync(path.join(certPath, 'key.pem'));
const cert = fs.readFileSync(path.join(certPath, 'cert.pem'));

module.exports = {
    server: {
        https: {
            key,
            cert,
        },
    },
};

const nextConfig: NextConfig = {
    /* config options here */
};

export default nextConfig;
