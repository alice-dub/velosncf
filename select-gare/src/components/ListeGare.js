import { useState, useEffect } from "react";

import Maps from './Maps'
import ApiRequest from './ApiRequest'
import FiltreStation from './FiltreStation'
import gares from './gares'
import Autocomplete from "@mui/material/Autocomplete";
import TextField from "@material-ui/core/TextField";

export default function Stops_nom({type}) {
  const [activeCategory, setActiveCategory] = useState([])
  const [data, setData] = useState([]);
  const [filter, setFilter] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [info, setInfo] = useState("");
  const [distance, setDistance] = useState(20);

  const filterOrigin = (filter) => {
    setFilter(filter);
  };

  function changeDistance(event) {
    setDistance(event.target.value) //update your value here
  }

  useEffect(() => {
    fetch(`data/liste_station.json`)
      .then((response) => {
        if (!response.ok) {
          throw new Error(
            `This is an HTTP error: The status is ${response.status}`
          );
        }
        return response.json();
      })
      .then((actualData) => {
        setData(actualData);
        setError(null);
      })
      .catch((err) => {
        setData(null);
        setError(err.message);
      })
      .finally(() => {
        setLoading(false);
      });
  }, []);

  function calculFiltre() {
    console.log("Filtre")
    console.log(filter)
    console.log(filter.type)
    if (filter.length == 0) {
      setInfo(" Veuillez renseigner une adresse pour pouvoir filtrer les gares à proximité");
    }
    else {
      setInfo("")
      var gares_2 = gares
                        .map((gare) => ({
                          ...gare,
                          distance_filtre: gareDistance(gare, filter),
                        }))
                        .filter((gare) => (gare.distance_filtre < distance))
                        .map(function(el) {
                          return {"stop_name" : el.stop_name};
                        });
      console.log(gares_2)
      setActiveCategory(gares_2)
      console.log("ici")
      console.log(activeCategory)
    }
  }

  function gareDistance(gare, filtre) {
    const [lat, long] = gare.coordinates;
    const [lat_0, long_0] = filtre.geometry.coordinates
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
      {loading && <div>Chargement des données</div>}
      {error && (
                <div>{` ${error}`}</div>
                )}
  <h4> Pré-filtrage des gares en fonction d'un lieu </h4>
  <p> Je veux les gares à moins de <input onChange={changeDistance} type="number" id="quantity" name="quantity" min="5" max="50" value={distance} size="5"></input> km de : </p>
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
                options={data}
                getOptionLabel={data => data.stop_name}
                renderInput={params => (
                <TextField {...params} label= {type} margin="normal" />
                )}/>
		    <Maps
			    filter = {activeCategory}/>
    </div>
  );
}
