import React, { useState } from "react";
import APIService from "./APIService";
import "./App.css";
export default function Search() {
    const [search, setSearch] = useState("");
    const handleSearchChange = (e) => {
        setSearch(e.target.value);
    };

    const handleSearch = () => {
        if (search) {
            // const formData = new FormData(); // not sure if i want to use this or do something custom
            // formData.append("image", image);
            // formData.append("labels", labels);
            // APIService.uploadPhoto(formData)
            APIService.searchPhotos(search)
                .then((response) => {
                    console.log(response);
                })
                .catch((error) => {
                    console.error(error);
                });
        }
    };
    return (
    <div>
        <nav>
            <ul className="nav-list">
                <li>
                    <a href="/upload" className="nav-item">Upload</a>
                </li>
                <li>
                    <a href="/search" className="nav-item"><strong>Search</strong></a>
                </li>
            </ul>
        </nav>
        <div className="outer">
            <div className="main">
                <h1>Search:</h1>
                <input type="text" placeholder="Search for images..." value={search} onChange={handleSearchChange} />
                <button onClick={handleSearch}>Search</button>
            </div>
        </div>
    </div>
    );
}