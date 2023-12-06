import { RouterProvider, createBrowserRouter } from "react-router-dom";
import './App.css';
import Upload from "./Upload.jsx";
import Search from "./Search.jsx";

const router = createBrowserRouter([
  {
    path: "/upload",
    element: <Upload />
  },
  {
    path: "/",
    element: <Search />
  },
  {
    path: "/search",
    element: <Search />
  },
]);

function App() {
  return <RouterProvider router={router} />;
}

export default App;
