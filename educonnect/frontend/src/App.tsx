import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { Toaster } from 'react-hot-toast';
import { AuthProvider } from './context/AuthContext';
import { ThemeProvider } from './context/ThemeContext';
import Layout from './components/Layout/Layout';
import HomePage from './pages/HomePage';
import LoginPage from './pages/LoginPage';
import RegisterPage from './pages/RegisterPage';
import CoursesPage from './pages/CoursesPage';
import './index.css';

// Create a client
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 5 * 60 * 1000, // 5 minutes
      refetchOnWindowFocus: false,
    },
  },
});

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <ThemeProvider>
        <AuthProvider>
          <Router>
            <div className="App">
              <Routes>
                {/* Auth Routes (without layout) */}
                <Route path="/login" element={<LoginPage />} />
                <Route path="/register" element={<RegisterPage />} />
                
                {/* Main Routes (with layout) */}
                <Route path="/" element={<Layout><HomePage /></Layout>} />
                
                {/* Main application routes */}
                <Route path="/courses" element={<Layout><CoursesPage /></Layout>} />
                <Route path="/universities" element={<Layout><div className="p-8 text-center">Universities page coming soon...</div></Layout>} />
                <Route path="/search" element={<Layout><div className="p-8 text-center">Search page coming soon...</div></Layout>} />
                <Route path="/profile" element={<Layout><div className="p-8 text-center">Profile page coming soon...</div></Layout>} />
                <Route path="/saved" element={<Layout><div className="p-8 text-center">Saved courses page coming soon...</div></Layout>} />
                <Route path="/chat" element={<Layout><div className="p-8 text-center">AI Chat page coming soon...</div></Layout>} />
                
                {/* 404 Route */}
                <Route path="*" element={<Layout><div className="p-8 text-center">Page not found</div></Layout>} />
              </Routes>
              
              {/* Toast notifications */}
              <Toaster
                position="top-right"
                toastOptions={{
                  duration: 4000,
                  style: {
                    background: 'var(--toast-bg)',
                    color: 'var(--toast-color)',
                  },
                }}
              />
            </div>
          </Router>
        </AuthProvider>
      </ThemeProvider>
    </QueryClientProvider>
  );
}

export default App;