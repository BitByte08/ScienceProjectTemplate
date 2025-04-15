import {useQuery} from "@tanstack/react-query";
import idrApiService from "./IdrApiService";

const IdrQueryService = () => {
  const { data, isLoading, error } = useQuery({
    queryKey: ['myData'],
    queryFn: idrApiService,
    refetchInterval: 5000,
  })
  if(isLoading) return { "light" : "loading" };
  if(error) return { "light" : error.message };
  return { "light" : data };
}
export default IdrQueryService;