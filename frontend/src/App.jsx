import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import './App.css';

import Dashboard from './pages/dashboard';
import Applications from './pages/applications';
import Companies from './pages/companies';
import Notes from './pages/notes';
import Auth from './pages/auth';

// ===== 認証ガード =====
function PrivateRoute({ children }) {
  const isLoggedIn = !!localStorage.getItem('token');
  return isLoggedIn ? children : <Navigate to="/auth" />;
}

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/auth" element={<Auth />} />

        <Route path="/" element={
          <PrivateRoute><Dashboard /></PrivateRoute>
        } />

        <Route path="/applications" element={
          <PrivateRoute><Applications /></PrivateRoute>
        } />

        <Route path="/companies" element={
          <PrivateRoute><Companies /></PrivateRoute>
        } />

        <Route path="/notes" element={
          <PrivateRoute><Notes /></PrivateRoute>
        } />

        <Route path="*" element={<Navigate to="/" />} />
      </Routes>
    </Router>
  );
}

export default App;