import React from 'react';

function Biography() {
	return (
		<section className="section">
			<div className="container">
				<div className="columns">
					<div className="column">
						<p className="title">About Me</p>
						<p className="subtitle">A Failed Chef and Fanfiction Author | A. Ivarson</p>
						<div className="content">
							<p>Once upon a time, I dreamed of becoming a world-renowned chef. I spent countless hours in the kitchen, perfecting my craft and experimenting with new recipes. Unfortunately, my dreams were shattered when I accidentally set fire to my kitchen and burned down my apartment building.</p>
							<p>But I didn't let that setback stop me. I turned to writing, and soon discovered a passion for fanfiction. My stories were a hit with the online community, and I quickly gained a following. However, my success was short-lived when I was sued by J.K. Rowling for my unauthorized Harry Potter fanfic.</p>
							<p>After taking a break from cooking, I rediscovered my love for it when I started hosting dinner parties for my friends. I found joy in creating new dishes and experimenting with different flavors. Now, I'm excited to combine my love of cooking with my programming skills to create the ultimate recipe app.</p>
						</div>
					</div>
					<div className="column">
						<figure className="image is-4by3">
							<img src="https://source.unsplash.com/random/640x480/?portrait" alt="A. Ivarson" />
						</figure>
					</div>
				</div>
			</div>
		</section>
	);
}

export default Biography;