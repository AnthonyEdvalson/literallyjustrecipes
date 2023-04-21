import React from 'react';
import { Link } from 'react-router-dom';

function Header() {
	return (
		<nav className="navbar is-primary" role="navigation" aria-label="main navigation">
			<div className="navbar-brand">
				<Link className="navbar-item" to="/">
					<img src="https://source.unsplash.com/random/640x480/?food" alt="Logo" width="112" height="28" />
				</Link>

				<a role="button" className="navbar-burger" aria-label="menu" aria-expanded="false" data-target="navbarBasicExample">
					<span aria-hidden="true"></span>
					<span aria-hidden="true"></span>
					<span aria-hidden="true"></span>
				</a>
			</div>

			<div id="navbarBasicExample" className="navbar-menu">
				<div className="navbar-start">
					<Link className="navbar-item" to="/">
						Home
					</Link>
				</div>

				<div className="navbar-end">
					<div className="navbar-item">
						<div className="field is-grouped">
							<p className="control">
								<input className="input" type="text" placeholder="Search" />
							</p>
							<p className="control">
								<button className="button is-primary">Search</button>
							</p>
						</div>
					</div>
				</div>
			</div>
		</nav>
	);
}

export default Header;