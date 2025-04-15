import React, { useEffect, useState } from 'react';
import axios from 'axios';

function App() {
  const [message, setMessage] = useState('');

  useEffect(() => {
    axios.get('http://mqtt-fastapi:8000/')
      .then(response => setMessage(response.data.message))
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