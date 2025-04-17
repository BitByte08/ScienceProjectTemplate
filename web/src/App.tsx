import React, { useEffect, useState } from 'react';
import { BrowserRouter as Router, Route, Routes, useNavigate, useParams } from 'react-router-dom';
import axios from 'axios';

const API_BASE = 'http://localhost:8000/api';

type Client = {
  id: number;
  client_name: string;
};

type LdrData = {
  brightness: number;
  time: string;
};

function MainPage() {
  const [clients, setClients] = useState<Client[]>([]);
  const [newClient, setNewClient] = useState('');
  const navigate = useNavigate();

  const fetchClients = async () => {
    const res = await axios.get(`${API_BASE}/client/list`);
    setClients(res.data);
  };

  const createClient = async () => {
    if (!newClient) return;
    await axios.post(`${API_BASE}/client/add`, { client_name: newClient });
    setNewClient('');
    fetchClients();
  };

  const deleteClient = async (client_name: string) => {
    await axios.delete(`${API_BASE}/client/delete/${client_name}`);
    fetchClients();
  };

  useEffect(() => {
    fetchClients();
  }, []);

  return (
    <div className="p-4">
      <h1 className="text-xl font-bold mb-4">센서 클라이언트 목록</h1>
      <input
        className="border p-2 mr-2"
        placeholder="클라이언트 이름"
        value={newClient}
        onChange={(e) => setNewClient(e.target.value)}
      />
      <button className="bg-blue-500 text-white px-4 py-2 rounded" onClick={createClient}>생성</button>
      <ul className="mt-4">
        {clients.map((client) => (
          <li key={client.id} className="flex items-center justify-between p-2 border-b">
            <span onClick={() => navigate(`/client/${client.client_name}`)} className="cursor-pointer text-blue-600">
              {client.client_name}
            </span>
            <button className="text-red-500" onClick={() => deleteClient(client.client_name)}>삭제</button>
          </li>
        ))}
      </ul>
    </div>
  );
}

function ClientPage() {
  const { client_name } = useParams();
  const [data, setData] = useState<LdrData | null>(null);
  const [history, setHistory] = useState<LdrData[]>([]);

  const fetchData = async () => {
    const res = await axios.get(`${API_BASE}/light?client=${client_name}`);
    const resHis = await axios.get(`${API_BASE}/light/history?client=${client_name}`);
    const newData = res.data;
    setData(newData);
    setHistory(resHis.data);
  };

  useEffect(() => {
    fetchData();
    const interval = setInterval(fetchData, 5000);
    return () => clearInterval(interval);
  }, [client_name]);
  useEffect(() => {
    console.log(data);
  }, [data]);
  return (
    <div className="p-4">
      <h1 className="text-xl font-bold mb-4">클라이언트 {client_name} 데이터</h1>
      {data && (
        <div className="mb-4">
          <p>밝기: {data.brightness}</p>
          {data.brightness < 1000 && (
            <p className="text-green-600 font-semibold">광합성이 이루어지고 있습니다.</p>
          )}
        </div>
      )}
      <ul className="list-disc pl-5">
        {history.map((entry, index) => (
          <li key={index}>
            {entry.time}: 밝기 {entry.brightness}
          </li>
        ))}
      </ul>
    </div>
  );
}

export default function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<MainPage />} />
        <Route path="/client/:client_name" element={<ClientPage />} />
      </Routes>
    </Router>
  );
}
