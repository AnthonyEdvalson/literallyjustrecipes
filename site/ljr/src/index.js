import React from 'react';
import ReactDOM from 'react-dom';
import Header from './Header';
import PageRouter from './PageRouter';
import Footer from './Footer';
import { BrowserRouter as Router } from 'react-router-dom';
import './index.css';

function Site() {
    return (
        <Router>
            <Header />
            <PageRouter />
            <Footer />
        </Router>
    )
}

ReactDOM.render(
	<React.StrictMode>
        <Site />
	</React.StrictMode>,
	document.getElementById('root')
);


export default Site;