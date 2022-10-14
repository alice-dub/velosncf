import { MapContainer, LayersControl, TileLayer, GeoJSON } from 'react-leaflet'
import L from 'leaflet'
import React from 'react';
import rails from './rails.json'

const position = [47, 3]

const Icon1 = new L.Icon({
  iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-green.png',
  shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png',
  iconSize: [20, 30],
  iconAnchor: [8, 30],
  popupAnchor: [1, -34],
  shadowSize: [10, 30]
});

const Icon2 = new L.Icon({
iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-red.png',
shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png',
iconSize: [25, 41],
iconAnchor: [12, 41],
popupAnchor: [1, -34],
shadowSize: [41, 41]
});

function pointToLayer(feature, latlng)  {
return L.marker(latlng, {
  icon: choix_icone(feature.properties.type)
});
}

function choix_icone(choix) {
  if (choix === "Gare accessible") {
    return Icon1
  }
  else {
    return Icon2
  }

}

function onEachFeature(feature, layer) {
  if (feature.properties) {
      layer.bindPopup(
        "Gare : " + feature.properties.stop_name
         + "<br> Gare de départ : " + feature.properties.start
         + "<br> Moyen de transport : " + feature.properties.transport_legende
        );
  }
}

class Maps extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      data_ter:'',
      data_car:'',
      data_intercite:'',
      data_tgv:'',
      data_transilien:''
    };
  }

  componentDidMount() {
    this.fetchGares(this.props.filter);
  }

  // setState() can't be called in componentDidUpdate()
  componentDidUpdate(prevProps) {
    if (this.props.filter !== prevProps.filter) {
      this.fetchGares(this.props.filter);
    }

  }

  fetchGares(filtre) {
    this.setState({
      data_ter: [],
      data_car: [],
      data_intercite:[],
      data_tgv:[],
      data_transilien:[]
    });
    for(let i = 0; i < filtre.length; i++){
      fetch(`data/gares_accessibles_TER/${encodeURIComponent(filtre[i].stop_name)}.json`)
      . then(res => res.json())
       .then(json => {
            this.setState({
              data_ter: [...this.state.data_ter, json]
            });
        })
        .catch(err => console.error(err));
    }
    for(let i = 0; i < filtre.length; i++){
      fetch(`data/gares_accessibles_carTER/${encodeURIComponent(filtre[i].stop_name)}.json`)
      . then(res => res.json())
       .then(json => {
            this.setState({
              data_car: [...this.state.data_car, json]
            });
        })
        .catch(err => console.error(err));
    }
    for(let i = 0; i < filtre.length; i++){
      fetch(`data/gares_accessibles_intercite/${encodeURIComponent(filtre[i].stop_name)}.json`)
      . then(res => res.json())
       .then(json => {
            this.setState({
              data_intercite: [...this.state.data_intercite, json]
            });
        })
        .catch(err => console.error(err));
    }
    for(let i = 0; i < filtre.length; i++){
      fetch(`data/gares_accessibles_TGV/${encodeURIComponent(filtre[i].stop_name)}.json`)
      . then(res => res.json())
       .then(json => {
            this.setState({
              data_tgv: [...this.state.data_tgv, json]
            });
        })
        .catch(err => console.error(err));
    }
    for(let i = 0; i < filtre.length; i++){
      fetch(`data/gares_accessibles_transilien/${encodeURIComponent(filtre[i].stop_name)}.json`)
      . then(res => res.json())
       .then(json => {
            this.setState({
              data_transilien: [...this.state.data_transilien, json]
            });
        })
        .catch(err => console.error(err));
    }
  }

  render() {
  return (
    <MapContainer center={position} zoom={6}>
      <TileLayer
        attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
      />
    <GeoJSON data={rails} interactive={false} style={feature => ({ color: "grey", weight:"2"})}/>
    <LayersControl collapsed={false}>
      <LayersControl.Overlay checked name="🚲 ❤️ Train TER 🚆">
      <GeoJSON key={this.state.data_ter} data={this.state.data_ter} onEachFeature={onEachFeature} pointToLayer={pointToLayer}/>
      </LayersControl.Overlay>
      <LayersControl.Overlay checked name="🚲 ❤️ Intercité 🚆">
      <GeoJSON key={this.state.data_intercite} data={this.state.data_intercite} onEachFeature={onEachFeature} pointToLayer={pointToLayer}/>
      </LayersControl.Overlay>
      <LayersControl.Overlay checked name="🚲 💔 TGV 🚄">
      <GeoJSON key={this.state.data_tgv} data={this.state.data_tgv} onEachFeature={onEachFeature} pointToLayer={pointToLayer}/>
      </LayersControl.Overlay>
      <LayersControl.Overlay checked name="🚲 ❤️ Transilien 🚆">
      <GeoJSON key={this.state.data_transilien} data={this.state.data_transilien} onEachFeature={onEachFeature} pointToLayer={pointToLayer}/>
      </LayersControl.Overlay>
      <LayersControl.Overlay checked name= "🚲 💔 Car TER 🚍">
      <GeoJSON key={this.state.data_car} data={this.state.data_car} onEachFeature={onEachFeature} pointToLayer={pointToLayer}/>
      </LayersControl.Overlay>
    </LayersControl>
    </MapContainer>
  )
}
}

export default Maps;