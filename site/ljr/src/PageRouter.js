import React from 'react';
import HomePage from './HomePage';
import RecipePage from './RecipePage';
import RealBio from './RealBio';
import { Switch, Route } from 'react-router-dom';

function PageRouter() {
	return (
		<Switch>
			<Route exact path="/">
				<HomePage />
			</Route>
			<Route exact path="/real-bio">
				<RealBio />
			</Route>
			<Route path="/recipe/:name">
				<RecipePage />
			</Route>
		</Switch>
	);
}

export default PageRouter;