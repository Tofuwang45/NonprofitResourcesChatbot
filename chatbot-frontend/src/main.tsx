import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App' // Import the App component you just renamed
import './styles.css'      // Make sure you have a CSS file for styles

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
)