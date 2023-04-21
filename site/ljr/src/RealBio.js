import React from 'react';

function Biography() {
	return (
		<section className="section">
			<div className="container">
				<div className="columns">
					<div className="column">
						<p className="title">About Me</p>
						<p className="subtitle">Software Developer and Serial Tinkerer | Anthony Edvalson</p>
						<div className="content">
							<p>Hi there! </p>
							<p>As you may have figured out by now, this site is a joke. It's a little art project I threw together over a weekend, I hope no one actually is using it to get recipes.</p>
							<p>This was an experiment to see if LLMs (GPT, LaMDA, etc.) are capable of creating stories worth reading, so I picked the most absurd format I could think of. I threw it together in a weekend and the results were pretty good so I made it open source, if you want to dig into the details, you can check out the <a href="https://github.com/AnthonyEdvalson/literallyjustrecipes">GitHub</a> repo.</p>
							<p>The website was also made by another LLM project that I'm currently working on, so if you notice any bugs in it or just want to say hi, I'm at <a href="mailto:tonyedvalson@gmail.com">tonyedvalson@gmail</a>.</p>
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