import React, { useEffect, useState } from 'react';
import axios from 'axios';

function App() {
  const [message, setMessage] = useState('');

  useEffect(() => {
    axios.get('/api')
      .then(response => console.log(response.data))
      .catch(error => console.error(error));
  }, []);

  return (
    <div>
      <h1>React + FastAPI + MQTT</h1>
      <p>FastAPI 응답: {message}</p>
    </div>
  );
}

export default App;