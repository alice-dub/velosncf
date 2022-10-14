//import React from 'react'
import Banner from './Banner'
import ListeGare from './ListeGare'

function App() {
	const styles = {
		item: {
		  margin: '5%' // is 50% of container width
		}
	  }
    return (
    <div>
        <Banner />
		<div style={styles.item}>
		<ListeGare
			type="Choix des gares 🚉"/>
		<footer> Site fait avec ❤️. Le code et toutes les infos concernant les données utilisées sont disponibles <a href="https://github.com/alice-dub/velosncf"> ici</a>. 
		J'aimerais récupérer des données plus précises sur les trajets acceptant des 🚲 : n'hésitez pas à donner un coup de ✋ ! </footer>
		</div>
	</div>)
}

export default App