import { useState } from 'react'
import ListeGare from './ListeGare'
import Maps from './Maps'

function DualListeGare() {
	const [activeDepart, setActiveDepart] = useState('Paris Austerlitz')
	return (
		<div> 
		<ListeGare
			setActiveCategory = {setActiveDepart}
			activeCategory = {activeDepart}
			type="Choix de la gare 🚉"/>s
	</div>
	)
}

export default DualListeGare