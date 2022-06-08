import { useState, useEffect } from "react";
import Maps from './Maps'

export default function Stops_nom({setActiveCategory, activeCategory, type}) {
  const [data, setData] = useState([]);
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
        setError(err.message);
        setData(null);
      })
      .finally(() => {
        setLoading(false);
      });
  }, []);

  return (
    <div>
      <h3> {type} </h3>
      {loading && <div>Chargement des données</div>}
      {error && (
        <div>{` ${error}`}</div>
      )}
			<select
				value={activeCategory}
				onChange={(e) => setActiveCategory(e.target.value)}>
        {data &&
          data.map(({ stop_name}) => (
            <option key={stop_name}>
              {stop_name}
            </option>
          ))}
			</select>
		    <Maps
			    filter = {activeCategory}/>
    </div>
  );
}
