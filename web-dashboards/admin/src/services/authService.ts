import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add token to requests
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Handle token refresh
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;
    
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;
      
      try {
        const refreshToken = localStorage.getItem('refreshToken');
        if (refreshToken) {
          const response = await axios.post(`${API_BASE_URL}/auth/token/refresh/`, {
            refresh: refreshToken,
          });
          
          const newToken = response.data.access;
          localStorage.setItem('token', newToken);
          originalRequest.headers.Authorization = `Bearer ${newToken}`;
          
          return api(originalRequest);
        }
      } catch (refreshError) {
        localStorage.removeItem('token');
        localStorage.removeItem('refreshToken');
        window.location.href = '/login';
      }
    }
    
    return Promise.reject(error);
  }
);

export const authService = {
  login: async (username: string, password: string) => {
    // Mock authentication for development
    if (username === 'admin' && password === 'admin123') {
      const mockResponse = {
        access: 'mock_access_token',
        refresh: 'mock_refresh_token',
        user: {
          id: 1,
          username: 'admin',
          email: 'admin@smartlocker.com',
          role: 'admin',
          first_name: 'Admin',
          last_name: 'User',
        }
      };
      
      // Store tokens using the same keys as the interceptor expects
      localStorage.setItem('token', mockResponse.access);
      localStorage.setItem('refreshToken', mockResponse.refresh);
      localStorage.setItem('user', JSON.stringify(mockResponse.user));
      
      return mockResponse;
    }
    
    // For production, use real API
    const response = await api.post('/auth/login/', { username, password });
    return response.data;
  },

  register: async (userData: any) => {
    const response = await api.post('/auth/register/', userData);
    return response.data;
  },

  getProfile: async () => {
    const response = await api.get('/auth/profile/');
    return response.data;
  },

  updateProfile: async (userData: any) => {
    const response = await api.patch('/auth/profile/', userData);
    return response.data;
  },
};

export default api;