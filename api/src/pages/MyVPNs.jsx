import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { Box } from '@mui/system';
import { Card, CardActionArea, CardContent, Container, TextField, Typography } from '@mui/material';
import List from '@mui/material/List';
import ListItemText from '@mui/material/ListItemText';
import Fab from '@mui/material/Fab';
import AddIcon from '@mui/icons-material/Add';
import Collapse from '@mui/material/Collapse';
import { ColorizeSharp, ExpandLess, ExpandMore } from '@mui/icons-material';
import { Alert } from '@mui/material';
import { useNavigate } from 'react-router-dom';
import { green, red } from '@mui/material/colors';
import { QRCode } from "react-qr-svg";

const Newsfeed = () => {
  const [vpns, setVPNs] = useState([]);
  const [detailsOpen, setDetailsOpen] = useState({});
  const navigate = useNavigate()

  useEffect(() => {
    // @ts-ignore
    const fetchVPNs = async () => {
      await axios.get('/vpns').then((res) => {
        console.log(res.data);
        // @ts-ignore
        setVPNs(res.data.reverse());
      });
    };
    fetchVPNs();
    console.log(vpns);
  }, []);


  const handleNewVPN = () => {
    navigate('/buy_vpn');
  };

  const handleOpenDetails = (id) => {
    setDetailsOpen((prevState) => ({ ...prevState, [id]: !prevState[id] }));
  };

  return (
    <Box m={2} pt={3} pb={7}>
      <Box pb={3}>
        <Typography variant="h4">Your's VPNs</Typography>
      </Box>
      <List>
        {vpns.map((vpns) => (
          <ListItemText key={vpns.id}>
            <Card variant="outlined">
              <CardActionArea onClick={() => handleOpenDetails(vpns.id)}>
                <CardContent>
                  <Typography variant="h6" color="text.primary">
                    {vpns.country}
                  </Typography>

                  {vpns.running == 'True' &&
                    <Typography color = 'green'>
                      Running
                    </Typography>
                  }
                  {vpns.running == 'False' &&
                    <Typography color = 'red'>
                      Expired
                    </Typography>
                  }
                  <Typography variant="body2" color="text.secondary" align="right">
                    expires on {vpns.expiration}
                  </Typography>
                  {detailsOpen[vpns.id] ? (
                    <Box display="flex">
                      
                      <Typography variant="body2" color="text.secondary">
                        Hide details
                      </Typography>
                      <ExpandLess />
                    </Box>
                  ) : (
                    <Box display="flex">
                      <Typography variant="body2" color="text.secondary">
                        See details
                      </Typography>
                      <ExpandMore />
                    </Box>
                  )}
                </CardContent>
              </CardActionArea>
              <Collapse in={detailsOpen[vpns.id]} timeout="auto" unmountOnExit>
              {/* <QRCode
                bgColor="#FFFFFF"
                fgColor="#000000"
                level="Q"
                style={{ width: 256 }}
                value={vpns.qr}
            /> */}
            <Container sx={{ display: 'flex'}}>
              <img src = {vpns.qr}></img>
              <Card>
              {vpns.conf.split('\n').map(line=>{ return <Typography>{line}</Typography>})}
              </Card>
            </Container>
              </Collapse>
            </Card>
          </ListItemText>
        ))}
      </List>
      <Fab
        onClick={handleNewVPN}
        variant="extended"
        color="primary"
        style={{ bottom: 0, position: 'fixed', transform: 'translate(-50%, -50%)', left: '50%' }}>
        <AddIcon sx={{ mr: 1 }} />
        New vpn
      </Fab>
    </Box>
  );
};

export default Newsfeed;
