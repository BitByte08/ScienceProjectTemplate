import Header from "../Components/Header";
import Footer from "../Components/Footer";
import {PropsWithChildren} from "react";

const MainLayout = (props:PropsWithChildren) => {
  return(
    <div>
      <Header />
      {props.children}
      <Footer />
    </div>
  )
}
export default MainLayout