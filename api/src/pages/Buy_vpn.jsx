import * as React from 'react';
import Box from '@mui/material/Box';
import Typography from '@mui/material/Typography';
import Container from '@mui/material/Container';
import { Alert, Backdrop, Button, Checkbox, createTheme, Fade, Modal, Paper, ThemeProvider } from '@mui/material';
import TextField from '@mui/material/TextField';
import Stack from '@mui/material/Stack';
import Autocomplete from '@mui/material/Autocomplete';
import { useEffect, useState } from 'react';
import { useMutation } from 'react-query';
import axios from 'axios';
import { useRecoilState } from 'recoil';
import EmailOutlinedIcon from '@mui/icons-material/EmailOutlined';
import EmailIcon from '@mui/icons-material/Email';

const theme = createTheme({
  palette: {
    primary: {
      main: '#677fa6',
    },
    secondary: {
      main: '#7a6091',
    },
  },
});


export default function BuyVpn() {
  
    
    const [countryList, setCountryList] = useState([]);
    const [selectedCountry, setSelectedCountry] = useState("");
    const [selectedPackage, setSelectedPackage] = useState("");
    const [error, setError] = useState("")
    const [info, setInfo] = useState(false)
    const alertDiv = error ? <Alert severity="error">{error}</Alert> : '' ;
    const infoDiv = info ? <Alert severity="success">Succes! Now you can connect to your vpn accesing the My VPNs page.</Alert> : '';
    const [checked, setChecked] = useState(false);

    const checkChanged = (state) => {
      setChecked(!checked);
    };

    const { reset, mutateAsync } = useMutation(
      (vpn) => {return axios.post('/vpn', vpn)}
    );
  
    useEffect(() => {
     
      // @ts-ignore
      const fetchCountries = async () => {
        await axios.get('/countries').then((res) => {
          setCountryList(res.data);
        });
      };
      fetchCountries();
    }, []);

  
    const handleChange = (event, value) => setSelectedCountry(value);
    const basicPick = (event) => setSelectedPackage('Basic');
    const premiumPick = (event) => setSelectedPackage('Premium');
    const enterprisePick = (event) => setSelectedPackage('Enterprise');
    const provideHandler = (event) => {
      setError("");
      setInfo(false);
      if(selectedCountry == ""){
        setError('Please chose a country');
        return;
      }
      if(selectedPackage == ""){
        setError('Please choose a plan');
        return;
      }
      //send request
      setSelectedPackage("");
      handleSubmit()
    }

    // @ts-ignore
  const handleSubmit = async () => {
    setError(null);
    setInfo(false);
    try {
      // @ts-ignore
      await mutateAsync({"country": selectedCountry, "plan": selectedPackage, "subscribe": checked}, 
      {
        onSuccess: (response) =>{
          setInfo(true);
        }
      })
    } catch (err) {
      setError(err.response.data)
    }};

  return (
    <ThemeProvider theme={theme}>
    <Container component="main">
        <Box
          sx={{
            marginTop: 8,
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
            marginBottom:2
          }}
          >
          <Typography color='primary'>
          Select the country for your VPN
          </Typography>
          <Stack spacing={2} sx={{ width: 300 }}>
        <Autocomplete
            onChange={handleChange}
            id="countries"
            freeSolo
            options={countryList.map((option) => option.name)}
            renderInput={(params) => <TextField {...params}  />}
        />
        </Stack>
        </Box>

        <Box sx={{ display: 'flex', flexWrap: 'wrap', width: '100%' }}>
        <Paper sx={{position:'relative', width:300, height:300, justifyContent: "center", alignItems: "center", textAlign: "center", verticalAlign: "middle", margin:5, background: (selectedPackage == "Basic" ? '#8cdea0' : '') }} elevation={3} color='primary'>
              <Typography component="h1" variant="h5" fontStyle='Libre Bodoni' align='center' color='primary'>
                Basic
              </Typography>
              <Typography marginTop={6} marginLeft={1} marginRight={1} component="h1" variant="body1" fontStyle='Libre Bodoni' align='center' color='#00000'>
                The VPN service will be available just for one month
              </Typography>
              <Typography marginTop={7} component="h1" variant="h5" fontStyle='Libre Bodoni' align='center' color='primary'>
                9,99$
              </Typography>
              <Button onClick={basicPick} variant="contained" sx={{marginTop: "20px"}}>
                PICK
              </Button>
        </Paper>
          
        <Paper sx={{position:'relative', width:300, height:300, justifyContent: "center", alignItems: "center", textAlign: "center", verticalAlign: "middle", margin:5, background: (selectedPackage == "Premium" ? '#8cdea0' : '')}} elevation={3} color='primary'>
      
              <Typography component="h1" variant="h5" fontStyle='Libre Bodoni' align='center' color='primary'>
                Premium
              </Typography>
              <Typography marginTop={6} marginLeft={1} marginRight={1} component="h1" variant="body1" fontStyle='Libre Bodoni' align='center' color='#00000'>
                The VPN service will be available for three months
              </Typography>
              <Typography marginTop={7} component="h1" variant="h5" fontStyle='Libre Bodoni' align='center' color='primary'>
                19,99$
              </Typography>
              <Button onClick={premiumPick} variant="contained" sx={{marginTop: "20px"}}>
                PICK
              </Button>
        </Paper>

        <Paper sx={{position:'relative', width:300, height:300, justifyContent: "center", alignItems: "center", textAlign: "center", verticalAlign: "middle", margin:5, background: (selectedPackage == "Enterprise" ? '#8cdea0' : '')}} elevation={3} color='primary'>
           
              <Typography component="h1" variant="h5" fontStyle='Libre Bodoni' align='center' color='primary'>
                Enterprise
              </Typography>
              <Typography marginTop={6} marginLeft={1} marginRight={1} component="h1" variant="body1" fontStyle='Libre Bodoni' align='center' color='#00000'>
                The VPN service will be available for one year
              </Typography>
              <Typography marginTop={7} component="h1" variant="h5" fontStyle='Libre Bodoni' align='center' color='primary'>
                39,99$
              </Typography>
              <Button onClick={enterprisePick} variant="contained" sx={{marginTop: "20px"}}>
                PICK
              </Button>
        </Paper>
        </Box>
        <Box
          sx={{
            marginTop: 2,
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
            marginBottom:2
          }}
          >
          <Typography color='primary'>Subscribe to our mail annoucements</Typography>
          <Checkbox
            checked={checked} onChange={checkChanged}
            icon={<EmailOutlinedIcon />}
            checkedIcon={<EmailIcon />}
          />
            {alertDiv}
            {infoDiv}
            
          <Button onClick={provideHandler} variant="outlined">
            PROVIDE VPN
          </Button>
        
        </Box>
    </Container>
    </ThemeProvider>
  );
}


