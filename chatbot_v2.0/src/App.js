import React from 'react';
import { BrowserRouter as Router, Route, Routes, Link } from 'react-router-dom';
import ChatInterface from './components/Chat'; 
import InputUrl from './components/InputUrl'; 
import './App.css';

function App() {
  return (
      <Router>
        <div className="app">
          <Routes>
            <Route path="/chat" element={<ChatInterface />} />
            <Route path="/" element={<InputUrl />} />
          </Routes>
        </div>
      </Router>
  );
}

export default App;
