import React, { useState } from "react";
import APIService from "./APIService";

export default function Upload() {
    const [image, setImage] = useState(null);
    const [labels, setLabels] = useState("");
    
    const handleImageChange = (e) => {
        setImage(e.target.files[0]);
    };
    const handleLabelsChange = (e) => {
        setLabels(e.target.value);
    };
    const handleSubmit = () => {
        if (image) {
            const formData = new FormData(); // not sure if i want to use this or do something custom
            formData.append("image", image);
            formData.append("labels", labels);
            // APIService.uploadPhoto(formData)
            APIService.uploadPhoto(image, labels.split(","))
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
            <input type="file" onChange={handleImageChange} />
            <input type="text" placeholder="Labels (comma separated)" value={labels} onChange={handleLabelsChange} />
            <button onClick={handleSubmit}>Submit</button>
        </div>
    );
}