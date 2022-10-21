import { MapContainer, LayersControl, TileLayer, GeoJSON, Circle } from 'react-leaflet'
import L from 'leaflet'
import React from 'react';
import rails from './rails.json'

const position = [47, 3]

const Icon1 = new L.Icon({
  iconUrl: 'images/icone_1.png',
  shadowUrl: 'images/marker-shadow.png',
  iconSize: [20, 30],
  iconAnchor: [8, 30],
  popupAnchor: [1, -34],
  shadowSize: [10, 30]
});

const Icon2 = new L.Icon({
  iconUrl: 'images/icone_2.png',
  shadowUrl: 'images/marker-shadow.png',
  iconSize: [20, 30],
  iconAnchor: [8, 30],
  popupAnchor: [1, -34],
  shadowSize: [10, 30]
});

const Icon3 = new L.Icon({
  iconUrl: 'images/icone_3.png',
  shadowUrl: 'images/marker-shadow.png',
  iconSize: [20, 30],
  iconAnchor: [8, 30],
  popupAnchor: [1, -34],
  shadowSize: [10, 30]
});

const Icon4 = new L.Icon({
  iconUrl: 'images/icone_4.png',
  shadowUrl: 'images/marker-shadow.png',
  iconSize: [20, 30],
  iconAnchor: [8, 30],
  popupAnchor: [1, -34],
  shadowSize: [10, 30]
});

const Icon5 = new L.Icon({
  iconUrl: 'images/icone_5.png',
  shadowUrl: 'images/marker-shadow.png',
  iconSize: [20, 30],
  iconAnchor: [8, 30],
  popupAnchor: [1, -34],
  shadowSize: [10, 30]
});

const IconDepart = new L.Icon({
iconUrl: 'images/icone_depart.png',
shadowUrl: 'images/marker-shadow.png',
iconSize: [25, 41],
iconAnchor: [12, 41],
popupAnchor: [1, -34],
shadowSize: [41, 41]
});

function pointToLayer(feature, latlng)  {
return L.marker(latlng, {
  icon: choix_icone(feature.properties.type, feature.properties.nombre_trajet_moyen)
});
}

function choix_icone(choix, nombre) {
  if (choix === "Gare sélectionnée") {
    return IconDepart
  }
  else {
    if (nombre < 1) {
      return Icon1
    }

    if (nombre < 3) {
      return Icon2
    }

    if (nombre < 6) {
      return Icon3
    }

    if (nombre < 10 ) {
      return Icon4
    }

    else {
      return Icon5
    }
  }

}

function onEachFeature(feature, layer) {
  if (feature.properties.type === "Gare sélectionnée") {
      layer.bindPopup(
         "<br> Gare de départ : " + feature.properties.start
         + "<br> Moyen de transport : " + feature.properties.transport_legende
         + "<br> Nombre moyen de départs quotidiens: " + feature.properties.nombre_trajet_moyen
        );
  }
  else {
    layer.bindPopup(
      "Gare : " + feature.properties.stop_name
      + "<br> Gare de départ : " + feature.properties.start
      + "<br> Moyen de transport : " + feature.properties.transport_legende
      + "<br> Nombre moyen de dessertes quotidiennes : " + feature.properties.nombre_trajet_moyen
    )
  }
}

class Maps extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      data_ter:''
    };
  }

  componentDidMount() {
    this.fetchGares(this.props.filter);
  }

  // setState() can't be called in componentDidUpdate()
  componentDidUpdate(prevProps) {
    if (this.props !== prevProps) {
      this.fetchGares(this.props.filter);
    }
  }

  fetchGares(filtre) {
    this.setState({
      data_ter: []
    });
    for(let i = 0; i < filtre.length; i++){
      fetch(`data/gares_accessibles_${encodeURIComponent(this.props.transport)}/${encodeURIComponent(filtre[i].stop_name)}.json`)
      . then(res => res.json())
       .then(json => {
            this.setState({
              data_ter: [...this.state.data_ter, json]
            });
        })
        .catch(err => console.error(err));
    }
  }

  render() {
  return (
    <MapContainer style={{flexGrow: "6"}} center={position} zoom={6}>
      <TileLayer
        attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
      />
    <GeoJSON data={rails} interactive={false} style={feature => ({ color: "grey", weight:"2"})}/>
    <LayersControl collapsed={true}>
      <LayersControl.Overlay checked name="Périmètre de recherche 📍">
      <Circle
    center={this.props.recherche.slice(0,2)}
    pathOptions={{ fillColor: 'blue' }}
    radius={this.props.recherche[2]*1000}
/>
      </LayersControl.Overlay>
      <LayersControl.Overlay checked name="Gares accessibles 🚉">
      <GeoJSON key={this.state.data_ter} data={this.state.data_ter} onEachFeature={onEachFeature} pointToLayer={pointToLayer}/>
      </LayersControl.Overlay>
    </LayersControl>
    </MapContainer>
  )
}
}

export default Maps;
