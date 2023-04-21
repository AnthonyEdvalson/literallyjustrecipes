import React from 'react';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faEnvelope, faGlobe } from '@fortawesome/free-solid-svg-icons';
import { Link } from 'react-router-dom';

function Footer() {
	const currentYear = new Date().getFullYear();
	return (
		<footer className="footer">
			<div className="content has-text-centered">
				<p>
				    <s>Amelia Ivarson</s>
					<strong>
					    &nbsp;
					    <Link to="/real-bio">Anthony Edvalson</Link>
                    </strong> &nbsp;&nbsp;
					<a href="mailto:amelia.ivarson@example.com">
						<FontAwesomeIcon icon={faEnvelope} />
					</a>
					&nbsp;&nbsp;
					<a href="https://www.ameliaivarson.com">
						<FontAwesomeIcon icon={faGlobe} />
					</a>
				</p>
				<p>&copy; {currentYear} All rights reserved.</p>
			</div>
		</footer>
	);
}

export default Footer;