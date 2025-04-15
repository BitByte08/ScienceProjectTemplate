import axios from "axios";

const idrApiService = async () => {
  const url = "http://localhost:8000/api/light";
  const res = await axios.get(url);
  return res.data;
}
export default idrApiService;