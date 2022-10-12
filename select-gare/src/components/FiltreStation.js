import Autocomplete from "@mui/material/Autocomplete";
import TextField from "@material-ui/core/TextField";

function FiltreStation({setActiveCategory, activeCategory, type, data}) {
    console.log("lalala")
    console.log(activeCategory)
    return   <Autocomplete
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
}

export default FiltreStation
