import periode_analyse from './periode_analyse.json'

function Legende({transport}) {
    var param = periode_analyse[transport]
    return (
    <div style={{maxWidth: "400px", marginLeft:"0.5%"}}>
        <h5> Légende</h5>
        <p style={{fontSize: "13px"}}> Calcul sur la période {param.debut} - {param.fin} </p>
        <table>
        <tr>
        <td><img alt="legende" src="images/icone_depart.png" height="30"/></td>
        <td style={{textAlign: "left"}}>Gare de départ</td>
        </tr>
        <tr>
        <td><img alt="legende" src="images/icone_1.png" height="30"/></td>
        <td style={{textAlign: "left"}}>Moins de 1 trajet / jour en moyenne</td>
        </tr>
        <tr>
        <td><img alt="legende" src="images/icone_2.png" height="30"/></td>
        <td style={{textAlign: "left"}}>Entre 1 et 3 trajets / jour en moyenne</td>
        </tr>
        <tr>
        <td><img alt="legende" src="images/icone_3.png" height="30"/></td>
        <td style={{textAlign: "left"}}>Entre 3 et 5 trajets / jour en moyenne</td>
        </tr>
        <tr>
        <td><img alt="legende" src="images/icone_4.png" height="30"/></td>
        <td style={{textAlign: "left"}}>Entre 5 et 10 trajets / jour en moyenne</td>
        </tr>
        <tr>
        <td><img alt="legende" src="images/icone_5.png" height="30"/></td>
        <td style={{textAlign: "left"}}>Plus de 10 trajets / jour en moyenne</td>
        </tr>
        </table>


            
            
    </div>
    )
}

export default Legende