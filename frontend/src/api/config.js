import axios from 'axios'

const instance = axios.create({
    baseURL: process.env.REACT_APP_API
})

axios.interceptors.request.use(config => {
    config.params = {
        ...config.params
        // More configuration can go here
    }
    return config
})

export default instance