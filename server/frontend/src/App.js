import { Route, Routes } from "react-router-dom";
import Dealers from "./components/Dealers/Dealers";
import LoginPanel from "./components/Login/Login";
import RegisterPanel from "./components/Register/Register";

function App() {
	return (
		<Routes>
			<Route path="/login" element={<LoginPanel />} />
			<Route path="/register" element={<RegisterPanel />} />
			<Route path="/dealers" element={<Dealers />} />
		</Routes>
	);
}
export default App;
