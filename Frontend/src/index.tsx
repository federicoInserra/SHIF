import React from 'react';
import { render } from 'react-dom';
import App from './App';

import './styles/globals.scss'
import { CookiesProvider } from 'react-cookie';
import { BrowserRouter } from 'react-router-dom';

const container = document.getElementById('root')!;

render(
  <React.StrictMode>
  
      <CookiesProvider>
        <BrowserRouter>
          <App />
        </BrowserRouter>
      </CookiesProvider>
  </React.StrictMode>
  , container
);


