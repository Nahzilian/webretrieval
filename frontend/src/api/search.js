import instance from './config'

const baseURL = '/'

// Leave it as async
export const queryData = (params = {}) => instance.get(baseURL, params)

