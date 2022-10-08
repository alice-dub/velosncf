import { useState, useEffect } from "react";
import Autocomplete from "@mui/material/Autocomplete";
import TextField from "@material-ui/core/TextField";
import Maps from './Maps'
import ApiRequest from './ApiRequest'

export default function Stops_nom({setActiveCategory, activeCategory, type}) {
  const [data, setData] = useState(['Paris Austerlitz']);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

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
  console.log("data")
  console.log(activeCategory)
  return (
    <div>
      {loading && <div>Chargement des données</div>}
      {error && (
                <div>{` ${error}`}</div>
                )}
  <ApiRequest/>
  <Autocomplete
    multiple
    limitTags={2}
    defaultValue={activeCategory}
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
