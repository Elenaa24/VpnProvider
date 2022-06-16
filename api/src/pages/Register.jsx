import * as React from 'react';
import Button from '@mui/material/Button';
import TextField from '@mui/material/TextField';
import Box from '@mui/material/Box';
import Typography from '@mui/material/Typography';
import Container from '@mui/material/Container';
import { createTheme, ThemeProvider } from '@mui/material/styles';
import { useMutation } from 'react-query';
import axios from 'axios';
import { useState } from 'react';
import { Alert } from '@mui/material';
import AccountCircleIcon from '@mui/icons-material/AccountCircle';
import { useNavigate } from 'react-router-dom';

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


export default function RegisterPage() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [password2, setPassword2] = useState("");
  const [error, setError] = useState("")
  const alertDiv = error ? <Alert severity="error">{error}</Alert> : '' ;
  const navigate = useNavigate();

  const { reset, mutateAsync } = useMutation(
      (user) => {return axios.post('/user/register', user)}
    );

  // @ts-ignore
  const handleSubmit = async (e) => {
  e.preventDefault();
  setError(null);
  if (password !== password2){
    setError('Passwords do not match');
  }
  else{
    try {
        // @ts-ignore
        await mutateAsync({"mail": email, "password": password}, 
        {
          onSuccess: (response) => {
            const token = response.data['token'];
            localStorage.setItem('token', token);
            axios.defaults.headers.common['Authorization'] = localStorage.getItem('token')
            navigate("/main");
          }
        })
      } catch (err) {
        setError(err.response.data)
      }
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
          <AccountCircleIcon fontSize="large" color='primary'>
          </AccountCircleIcon>
          <Typography component="h1" variant="h5" fontStyle='Libre Bodoni' color='primary'>
            Registration
          </Typography>
          <Box component="form" sx={{ mt: 1 }}>
            <TextField
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
              margin="normal"
              required
              fullWidth
              name="password"
              label="Password"
              type="password"
              id="password"
              onChange={(v) => {setPassword(v.target.value)}}
            />
            <TextField
              margin="normal"
              required
              fullWidth
              name="password2"
              label="Confirm Password"
              type="password"
              id="password2"
              onChange={(v) => {setPassword2(v.target.value)}}
            />
            <Button
              onClick={handleSubmit}
              fullWidth
              variant="contained"
              color='primary'
              sx={{ mt: 3, mb: 2, fontStyle:'Libre Bodoni' }}
            >
              Register
            </Button>
            {alertDiv}
          </Box>
        </Box>
      
      </Container>
    //</ThemeProvider>
  );
}