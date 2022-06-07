//import React from 'react'
import { useState } from 'react'
import Banner from './Banner'
import DualListeGare from './DualListeGare'

function App() {
	const styles = {
		container: {
		  display: 'flex',
		  flex: 1,
		  flexDirection: 'row',
		  flexWrap: 'wrap',
		  alignItems: 'flex-start' // if you want to fill rows left to right
		},
		item: {
		  width: '80%' // is 50% of container width
		}
	  }
    const [activeDepart, setActiveDepart] = useState('')
    return (
    <div style={{marginLeft:"5%"}} >
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