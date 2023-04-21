import React, { createElement } from 'react';
import { useParams } from "react-router-dom";
import BeefStirFry from "./recipes/BeefStirFry";
import ChickenFajitas from "./recipes/ChickenFajitas";
import PestoPasta from "./recipes/PestoPasta";

const recipes = {
    "beef-stir-fry": BeefStirFry,
    "chicken-fajitas": ChickenFajitas,
    "pesto-pasta": PestoPasta
}

function RecipePage(props) {
	let { name } = useParams();
	return createElement(recipes[name]);
}

export default RecipePage;