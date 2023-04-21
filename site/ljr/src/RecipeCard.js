import React from 'react';
import { Link } from 'react-router-dom';

function RecipeCard(props) {
	return (
		<Link to={`/recipe/${props.id}`}>
			<div className="card">
				<div className="card-image">
					<figure className="image is-4by3">
						<img src={`https://source.unsplash.com/random/640x480/?${props.search}`} alt={props.title} />
					</figure>
				</div>
				<div className="card-content">
					<div className="media">
						<div className="media-content">
							<p className="title is-4">{props.title}</p>
						</div>
					</div>

					<div className="content">
						{props.description}
					</div>
				</div>
				{props.children}
			</div>
		</Link>
	);
}

export default RecipeCard;