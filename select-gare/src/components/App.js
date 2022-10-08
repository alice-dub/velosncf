//import React from 'react'
import { useState } from 'react'
import Banner from './Banner'
import DualListeGare from './DualListeGare'

function App() {
	const styles = {
		item: {
		  margin: '5%' // is 50% of container width
		}
	  }
    const [activeDepart, setActiveDepart] = useState('')
    return (
    <div>
        <Banner />
        <div style={styles.container}>
		<div style={styles.item}>
		<DualListeGare
			setActiveCategory = {setActiveDepart}
			activeCategory = {activeDepart}
			type="Choux de la gare 🚉"/>
		</div>
	</div>
    </div>)
}

export default App