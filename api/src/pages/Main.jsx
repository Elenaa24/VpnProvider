import * as React from 'react';
import AppBar from '@mui/material/AppBar';
import Box from '@mui/material/Box';
import Toolbar from '@mui/material/Toolbar';
import IconButton from '@mui/material/IconButton';
import Typography from '@mui/material/Typography';
import Menu from '@mui/material/Menu';
import MenuIcon from '@mui/icons-material/Menu';
import Container from '@mui/material/Container';
import Avatar from '@mui/material/Avatar';
import Button from '@mui/material/Button';
import Tooltip from '@mui/material/Tooltip';
import MenuItem from '@mui/material/MenuItem';
import { ExpandMoreOutlined } from '@mui/icons-material';
import { useState } from 'react';
import { Accordion, AccordionDetails, AccordionSummary, createTheme, Grid, ThemeProvider } from '@mui/material';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import pic from '../images/worldwide-access.svg'
import { width } from '@mui/system';

const pages = ['Products', 'About VPN', 'Servers'];
const settings = ['Account'];
const products = ['Windows', 'Linux', 'Android', 'IOS']



const theme = createTheme({
    palette: {
      primary: {
        main: '#3b5b75',
      },
      secondary: {
        main: '#7a6091',
      },
    },
  });

const ResponsiveAppBar = () => {
  const [anchorElNav, setAnchorElNav] = useState(null);
  const [anchorElUser, setAnchorElUser] = useState(null);
  const navigate = useNavigate()

  const handleOpenNavMenu = (event) => {
    setAnchorElNav(event.currentTarget);
  };
  const handleOpenUserMenu = (event) => {
    setAnchorElUser(event.currentTarget);
  };

  const handleCloseNavMenu = () => {
    setAnchorElNav(null);
  };

  const handleCloseUserMenu = () => {
    setAnchorElUser(null);
  };

  const handleBuyVpn = () => {
    navigate("/buy_vpn");
  };

  const handleMyVpns = () => {
    navigate('/my_vpns');
  };

  const handleLogout = () => {
    localStorage.setItem('token', "");
    axios.defaults.headers.common['Authorization'] = localStorage.getItem('token')
    navigate('/login');
  };

  return (
    <ThemeProvider theme={theme}>
    <AppBar position="static" color='primary'>
      <Container maxWidth="xl">
        <Toolbar disableGutters>
          <Typography
            variant="h6"
            noWrap
            component="div"
            sx={{ mr: 2, display: { xs: 'none', md: 'flex' } }}
          >
            GoVPN
          </Typography>
          {/* <img src={pic} alt='logo'></img> */}

          <Box sx={{ flexGrow: 1, display: { xs: 'flex', md: 'none' } }}>
            <IconButton
              size="large"
              aria-label="account of current user"
              aria-controls="menu-appbar"
              aria-haspopup="true"
              onClick={handleOpenNavMenu}
              color="inherit"
            >
              <MenuIcon />
            </IconButton>
            <Menu
              id="menu-appbar"
              anchorEl={anchorElNav}
              anchorOrigin={{
                vertical: 'bottom',
                horizontal: 'left',
              }}
              keepMounted
              transformOrigin={{
                vertical: 'top',
                horizontal: 'left',
              }}
              open={Boolean(anchorElNav)}
              onClose={handleCloseNavMenu}
              sx={{
                display: { xs: 'block', md: 'none' },
              }}
            >
              {pages.map((page) => (
                <MenuItem key={page} onClick={handleCloseNavMenu}>
                  <Typography textAlign="center">{page}</Typography>
                </MenuItem>
              ))}
            </Menu>
          </Box>
          <Typography
            variant="h6"
            noWrap
            component="div"
            sx={{ flexGrow: 1, display: { xs: 'flex', md: 'none' } }}
          >
            LOGO
          </Typography>
          <Box sx={{ flexGrow: 1, display: { xs: 'none', md: 'flex' } }}>
            {pages.map((page) => (
              <Button
                key={page}
                onClick={handleCloseNavMenu}
                sx={{ my: 2, color: 'white', display: 'block' }}
              >
                {page}
              </Button>
            ))}
          </Box>

          <Box sx={{ flexGrow: 0 }}>
            <Tooltip title="Open settings">
              <IconButton onClick={handleOpenUserMenu} sx={{ p: 0 }}>
                <Avatar/>
              </IconButton>
            </Tooltip>
            <Menu
              sx={{ mt: '45px' }}
              id="menu-appbar"
              anchorEl={anchorElUser}
              anchorOrigin={{
                vertical: 'top',
                horizontal: 'right',
              }}
              keepMounted
              transformOrigin={{
                vertical: 'top',
                horizontal: 'right',
              }}
              open={Boolean(anchorElUser)}
              onClose={handleCloseUserMenu}
            >
              <MenuItem key = 'My VPNs' onClick={handleMyVpns}>
                <Typography textAlign="center">{'My VPNs'}</Typography>
              </MenuItem>
              {settings.map((setting) => (
                <MenuItem key={setting} onClick={handleCloseUserMenu}>
                  <Typography textAlign="center">{setting}</Typography>
                </MenuItem>
              ))}
              <MenuItem key = 'Logout' onClick={handleLogout}>
                <Typography textAlign="center">{'Logout'}</Typography>
              </MenuItem>
            </Menu>
          </Box>
        </Toolbar>
      </Container>
    </AppBar>
    <Container sx={{marginLeft: "15px"}}>
      <Grid container spacing={2} marginTop='10px'>
        <Grid item xs={6}>
          <Typography component="h2" variant="h3" fontStyle='Libre Bodoni' color='primary' mb={'40px'}>
            Why do you need a VPN?
          </Typography>
          <Accordion disableGutters elevation={0} square sx={{marginBottom: "15px", boxShadow:'none', borderLeft:'1px solid #3b5b75', '&:before': {
          display: 'none' }}}>
            <AccordionSummary expandIcon={<ExpandMoreOutlined />}>
              <Typography component="h4" variant="h4" fontStyle='Libre Bodoni' color='primary' marginTop={'10px'}>
              You use public Wi-Fi regularly
            </Typography>

            </AccordionSummary>
            <AccordionDetails>
              VPN is used to secure your connection on public Wi-Fi, so you can browse in full privacy. 
              Hackers have many methods to steal your data on public hotspots, but with a VPN your online 
              traffic is invisible to them.
            </AccordionDetails>
          </Accordion>
          <Accordion disableGutters elevation={0} square sx={{marginBottom: "15px", boxShadow:'none', borderLeft:'1px solid #3b5b75', '&:before': {
          display: 'none',
      }}}>
            <AccordionSummary expandIcon={<ExpandMoreOutlined />} >
              <Typography component="h4" variant="h4" fontStyle='Libre Bodoni' color='primary' marginTop={'10px'}>
              You want to stay safe online
            </Typography>

            </AccordionSummary>
            <AccordionDetails>
            Government agencies, marketers, internet service providers would all love to track and collect
            your browsing history, messages, and other private data. Best way to hide it? Using a VPN to 
            encrypt your traffic, hide your IP, and cover your tracks online. Use it at home, at work, and 
            on the go to enjoy non-stop protection.
            </AccordionDetails>
          </Accordion>
        </Grid>
        <Grid item xs={6} sx={{display:'flex', justifyContent:'center'}}> 
          <img src={`${pic}?marginLeft="100px"`} width="600px"></img>
          {/* <Image>
              img src={pic}
              style={{margin:'auto', display:'block'}}
            </Image> */}
          {/* <img src={`${pic}?margin=auto&display=block`} width="400px"></img> */}
          {/* import pic from '../images/govpnlogo.png' */}
        </Grid>
      </Grid>
        <Button variant='contained' sx={{marginLeft:'670px'}} onClick={handleBuyVpn} color='secondary'>
            <Typography variant='h6'>
            BUY A VPN 
            </Typography>
           
        </Button>
    </Container>
    </ThemeProvider>
  );
};
export default ResponsiveAppBar;
