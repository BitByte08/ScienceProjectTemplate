import React, { useEffect, useState } from 'react';
import axios from 'axios';
import {QueryClientProvider, QueryClient} from "@tanstack/react-query";
import MainLayout from "./layouts/MainLayout";

const queryClient = new QueryClient();

function App() {
  return(
    <QueryClientProvider client={queryClient}>
      <MainLayout>

      </MainLayout>
    </QueryClientProvider>
  )
}

export default App;