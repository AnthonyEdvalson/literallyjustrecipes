import React from 'react';
import RecipeCard from './RecipeCard';
import Biography from './Biography'; 
import { Link } from 'react-router-dom';

function HomePage(props) {
	return (
		<>
			<section className="hero">
				<div className="hero-body">
					<div className="container">
						<p className="title">Welcome to our Recipe Website</p>
						<p className="subtitle">Browse through our collection of delicious recipes</p>
					</div>
				</div>
			</section>
			<Biography />
			<section className="section">
				<div className="container">
					<div className="columns is-multiline">
						{props.recipes && props.recipes.map(recipe => (
							<div className="column is-one-third" key={recipe.id}>
								<Link to={`/recipe/${recipe.id}`}>
									<RecipeCard
										title={recipe.title}
										description={recipe.description}
										search={recipe.search}
									/>
								</Link>
							</div>
						))}
            
            <div className="column is-one-third">
                <RecipeCard
                  title="Pesto Pasta"
                  id="pesto-pasta"
                  description="A classic pasta dish with a delicious pesto sauce"
                  search="pasta,pesto"
                />
            </div>
            <div className="column is-one-third">
                <RecipeCard
                  title="Chicken Fajitas"
                  id="chicken-fajitas"
                  description="A spicy and flavorful Mexican dish"
                  search="chicken,fajitas"
                />
            </div>
            <div className="column is-one-third">
                <RecipeCard
                  title="Beef Stir Fry"
                  id="beef-stir-fry"
                  description="A quick and easy Asian-inspired dish"
                  search="beef,stir fry"
                />
            </div>
					</div>
				</div>
			</section>
		</>
	);
}

export default HomePage;