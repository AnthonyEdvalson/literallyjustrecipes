import React from 'react';

function RecipePage() {
	return (
		<section className="section">
			<div className="container">
				<div className="columns">
					<div className="column">
						<p className="title">Recipe Title</p>
						<div className="card">
							<div className="card-image">
								<figure className="image is-4by3">
									<img src="https://source.unsplash.com/random/640x480/?food" alt="Recipe" />
								</figure>
							</div>
							<div className="card-content">
								<div className="media">
									<div className="media-content">
										<p className="title is-4">Recipe Title</p>
									</div>
								</div>

								<div className="content">
									<p><strong>Author:</strong> John Doe</p>
									<p><strong>Description:</strong> This is a delicious recipe that is perfect for any occasion.</p>
									<p><strong>Ingredients:</strong></p>
									<ul>
										<li>1 cup flour</li>
										<li>1/2 cup sugar</li>
										<li>1/4 cup butter</li>
										<li>1 egg</li>
										<li>1 tsp baking powder</li>
										<li>1/2 tsp salt</li>
										<li>1/2 cup milk</li>
									</ul>
									<p><strong>Instructions:</strong></p>
									<ol>
										<li>Preheat oven to 350 degrees F (175 degrees C).</li>
										<li>In a large bowl, cream together the butter and sugar until smooth.</li>
										<li>Beat in the egg and mix well.</li>
										<li>In a separate bowl, combine the flour, baking powder, and salt.</li>
										<li>Add the dry ingredients to the wet ingredients and mix until just combined.</li>
										<li>Stir in the milk until the batter is smooth.</li>
										<li>Pour the batter into a greased 9x9 inch baking dish.</li>
										<li>Bake for 25-30 minutes, or until a toothpick inserted into the center comes out clean.</li>
										<li>Cool the cake in the pan for 10 minutes before removing and serving.</li>
									</ol>
								</div>
							</div>
						</div>
					</div>
				</div>
			</div>
		</section>
	);
}

export default RecipePage;