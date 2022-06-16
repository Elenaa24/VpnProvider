import * as React from 'react';
import Button from '@mui/material/Button';
import TextField from '@mui/material/TextField';
import Link from '@mui/material/Link';
import Grid from '@mui/material/Grid';
import Box from '@mui/material/Box';
import Typography from '@mui/material/Typography';
import Container from '@mui/material/Container';
import { createTheme, ThemeProvider } from '@mui/material/styles';
import { useMutation } from 'react-query';
import axios from 'axios';
import { useState } from 'react';
import { Alert } from '@mui/material';
import { useNavigate } from 'react-router-dom';
import pic from '../images/govpnlogo.png'


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


export default function LoginPage() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("")
  const alertDiv = error ? <Alert severity="error">{error}</Alert> : '' ;
  const navigate = useNavigate()

  const { reset, mutateAsync } = useMutation(
      (user) => {return axios.post('/user/login', user)}
    );

  // @ts-ignore
  const handleSubmit = async (e) => {
  e.preventDefault();
  setError(null);
  try {
    // @ts-ignore
    await mutateAsync({"mail": email, "password": password}, 
    {
      onSuccess: (response) =>{
        const token = response.data['token'];
        localStorage.setItem('token', token);
        axios.defaults.headers.common['Authorization'] = localStorage.getItem('token')
        navigate("/main");
      }
    })
  } catch (err) {
    setError(err.response.data)
  }
};

  return (
    <ThemeProvider theme={theme}>
      <Container component="main" maxWidth="xs">
        <Box
          sx={{
            marginTop: 8,
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
          }}
        >
           
          {/* <AccountCircleIcon fontSize="large" color='secondary'>
          </AccountCircleIcon> */}
          <Typography component="h1" variant="h5" fontStyle='Libre Bodoni' align='center' color='primary'>
           Welcome
          </Typography>
          <Box component="form" sx={{ mt: 1 }}>
            <TextField
              className='email'
              margin="normal"
              required
              fullWidth
              id="email"
              label="Email Address"
              name="email"
              autoComplete="email"
              autoFocus
              onChange={(v) => {setEmail(v.target.value)}}
            />
            <TextField 
              className='password'
              margin="normal"
              required
              fullWidth
              name="password"
              label="Password"
              type="password"
              id="password"
              autoComplete="current-password"
              onChange={(v) => {setPassword(v.target.value)}}
            />
            {/* <FormControlLabel
              control={<Checkbox value="remember" color="primary" />}
              label="Remember me"
            /> */}
            <Grid container>
              <Grid item xs>
                <Link href="#" variant="body2">
                  Forgot password?
                </Link>
              </Grid>
            </Grid>
            <Button
              className='mybutton'
              onClick={handleSubmit}
              fullWidth
              color='primary'
              variant="contained"
              sx={{ mt: 3, mb: 2}}
            >
              Sign In
            </Button>
            <Grid container >
              <Grid item xs>
                <Typography variant="body2" display='inline' color='#C0C0C0' fontStyle='Libre Bodoni'>
                Don't have an account? 
                </Typography>
                <Link href="/register" variant="body2" display='inline' fontStyle='Libre Bodoni'>
                   Click here
                </Link>
              </Grid>
            </Grid>
            {alertDiv}
          </Box>
          <img src={pic} alt='logo'></img>
        </Box>
      </Container>
    //</ThemeProvider>
  );
}