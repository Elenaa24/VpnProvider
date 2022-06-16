import LoginPage from "./pages/Login";
import MainPage from "./pages/Main";
import { Paths } from "./Paths";
import React from "react";
import { BrowserRouter as Router, Route, Routes} from "react-router-dom";
import RegisterPage from "./pages/Register";
import BuyVpn from "./pages/Buy_vpn";
import MyVPNs from "./pages/MyVPNs";

export const MyRoutes = () => {
    return (
        <Router> 
        <Routes>
        <Route  path={Paths.Main} element={<MainPage />}>
        </Route>
        <Route  path={Paths.Login} element={<LoginPage />}>
        </Route>
        <Route  path={Paths.Register}  element={<RegisterPage />}>
       </Route>
        <Route path={Paths.Buy_vpn} element={<BuyVpn />}>
        </Route>
        <Route path={Paths.MyVPNs} element={<MyVPNs />}>
        </Route>
       </Routes>
       </Router>
    )
}