import { useState, useEffect } from "react";

import Maps from './Maps'
import ApiRequest from './ApiRequest'
import liste_station from './liste_station.json'
import Autocomplete from "@mui/material/Autocomplete";
import TextField from "@material-ui/core/TextField";

export default function Stops_nom({type}) {
  const [activeCategory, setActiveCategory] = useState([])
  const [filter, setFilter] = useState([]);
  const [info, setInfo] = useState("");
  const [distance, setDistance] = useState(5);
  const [transport, setTransport] = useState("TER");

  const filterOrigin = (filter) => {
    setFilter(filter);
  };

  function changeDistance(event) {
    setDistance(event.target.value) //update your value here
  }

  function changeTransport(event) {
    setTransport(event.target.value) //update your value here
  }

  function calculFiltre() {
    console.log("coucou")
    console.log("Filtre")
    console.log(filter)
    console.log(filter.type)
    if (filter.length == 0) {
      setInfo(" Veuillez renseigner une adresse pour pouvoir filtrer les gares à proximité");
    }
    else {
      setInfo("")
      console.log(liste_station)
      var gares_2 = liste_station
                        .map((liste_station) => ({
                          ...liste_station,
                          distance_filtre: gareDistance(liste_station, filter),
                        }))
                        .filter((liste_station) => liste_station.transport.includes(transport))
                        .filter((liste_station) => (liste_station.distance_filtre < distance))
                        .sort((liste_station) => liste_station.distance)
                        .map(function(el) {
                          return {"stop_name" : el.stop_name};
                        });
      console.log(gares_2)
      console.log(gares_2.length)
      if (gares_2.length > 10) {
        setInfo("Plus de 10 gares correspondant à vos critères de recherche ont été trouvés ! Les 10 gares les plus proches ont été sélectionnées.");
        gares_2 = gares_2.slice(0, 10); 
      };
      if (gares_2.length === 0) {
        setInfo("Aucune gare correpondant aux critère n'a été trouvée. Vous pouvez ");
      };
      setActiveCategory(gares_2)
    }
  }

  function gareDistance(gare, filtre) {
    const [lat, long] = [gare.stop_lat, gare.stop_lon];
    const [long_0, lat_0] = filtre.geometry.coordinates
    return getDistanceFromLatLonInKm(lat, long, lat_0, long_0);
  };
  
  function getDistanceFromLatLonInKm(lat1, lon1, lat2, lon2) {
    var R = 6371; // Radius of the earth in km
    var dLat = deg2rad(lat2-lat1);  // deg2rad below
    var dLon = deg2rad(lon2-lon1); 
    var a = 
      Math.sin(dLat/2) * Math.sin(dLat/2) +
      Math.cos(deg2rad(lat1)) * Math.cos(deg2rad(lat2)) * 
      Math.sin(dLon/2) * Math.sin(dLon/2)
      ; 
    var c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a)); 
    var d = R * c; // Distance in km
    return d;
  }

  function deg2rad(deg) {
    return deg * (Math.PI/180)
  }

  return (
    <div>
  <h4> Pré-filtrage des gares en fonction d'un lieu </h4>
  <p> Je veux les gares 
  <select value={transport} onChange={changeTransport}>
        <option value="TER" selected>TER</option>
        <option value="intercite">Intercité</option>
        <option value="TGV">TGV</option>
        <option value="carTER">Car TER</option>
        <option value="transilien">Transilien</option>
      </select>
    
      à moins de <input onChange={changeDistance} type="number" id="quantity" name="quantity" min="5" max="50" value={distance} size="5"></input> km de : </p>
  <div style={{"display":"flex", "flexDirection":"row"}}>
  <ApiRequest filterOrigin={filterOrigin}/>
  <button className="button" onClick={calculFiltre} >Filtre</button>
  <p  style={{color:"red", marginLeft:"5px"}}>  {info}</p>
  </div>
  <h4> Sélection de gares </h4>
        <Autocomplete
                multiple
                limitTags={2}
                value={activeCategory}
                onChange={(event: any, newValue: string | null) => {
                setActiveCategory(newValue);
                }}
                options={liste_station}
                getOptionLabel={liste_station => liste_station.stop_name}
                renderInput={params => (
                <TextField {...params} label= {type} margin="normal" />
                )}/>
		    <Maps
			    filter = {activeCategory}/>
    </div>
  );
}
