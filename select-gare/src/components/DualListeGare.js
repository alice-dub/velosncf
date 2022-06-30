import { useState } from 'react'
import ListeGare from './ListeGare'


function DualListeGare() {
	const [activeDepart, setActiveDepart] = useState({'stop_name':'Paris Austerlitz'})
	return (
		<div> 
		<ListeGare
			setActiveCategory = {setActiveDepart}
			activeCategory = {activeDepart}
			type="Choix de la gare 🚉"/>
	</div>
	)
}

export default DualListeGare