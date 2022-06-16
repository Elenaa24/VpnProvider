import React from 'react';
import { MyRoutes } from './Routes';
import './App.css';
import { QueryClient, QueryClientProvider } from 'react-query';

function App() {
  const queryClient = new QueryClient();

  // const instance = axios.create({
  //   baseURL: 'http://127.0.0.1:5000',
  //   headers: {'X-Custom-Header': 'foobar'}
  // });
 
  return (
   
  <QueryClientProvider client={queryClient}>
    <MyRoutes/>
  </QueryClientProvider>
 
  );
}

export default App;
