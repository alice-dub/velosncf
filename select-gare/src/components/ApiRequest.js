import * as React from 'react';
import Box from '@mui/material/Box';
import TextField from '@mui/material/TextField';
import Autocomplete from '@mui/material/Autocomplete';
import LocationOnIcon from '@mui/icons-material/LocationOn';
import Grid from '@mui/material/Grid';
import api from './utils/api';


export default function ApiRequest({filterOrigin}) {
  const [value, setValue] = React.useState(null);
  const [inputValue, setInputValue] = React.useState('');
  const [options, setOptions] = React.useState([]);
  const loaded = React.useRef(false);

  React.useEffect(() => {
    let active = true;

    if (inputValue === '') {
      setOptions(value ? [value] : []);
      return undefined;
    }

    if (inputValue && inputValue.length > 2) {
        api
        .get(`https://api-adresse.data.gouv.fr/search/?q=${inputValue}`)
        .then((res) => setOptions(res.features));

    }

    fetch({ input: inputValue }, (results) => {
      if (active) {
        let newOptions = [];

        if (value) {
          newOptions = [value];
        }

        if (results) {
          newOptions = [...newOptions, ...results];
        }

        setOptions(newOptions);
      }
    });
    
    return () => {
      active = false;
    };
    
  }, [value, inputValue, fetch]);

  function updateValue(value) {
    filterOrigin(value)
  };

  return (
    <Autocomplete
      id="ban-api"
      noOptionsText={'Pas de résultats trouvés'}
      sx={{ width: 300 }}
      getOptionLabel={(option) =>
        option.properties.label
      }
      filterOptions={(x) => x}
      options={options}
      autoComplete
      includeInputInList
      filterSelectedOptions
      value={value}
      onChange={(event, newValue) => {
        setOptions(newValue ? [newValue, ...options] : options);
        setValue(newValue);
        updateValue(newValue);
      }}
      onInputChange={(event, newInputValue) => {
        setInputValue(newInputValue);
      }}
      renderInput={(params) => (
        <TextField {...params} label="Choix de l'adresse 📍" />
      )}
      renderOption={(props, option) => {
        const matches = option.properties.label;

        return (
          <li {...props}>
            <Grid container alignItems="center">
              <Grid item>
                <Box
                  component={LocationOnIcon}
                  sx={{ color: 'text.secondary', mr: 2 }}
                />
              </Grid>
              <Grid item xs>
                {matches}
              </Grid>
            </Grid>
          </li>
        );
      }}
    />
  );
}