import React, { useState } from 'react';
import axios from 'axios';

// Inside the Chat component (or a similar component where the upload button will be placed)
const Chat = () => {
    const [selectedFile, setSelectedFile] = useState(null);

    const handleFileChange = (event) => {
        setSelectedFile(event.target.files[0]);
    };

    const handleUpload = async () => {
        if (!selectedFile) {
            alert('Please select a file first.');
            return;
        }

        const formData = new FormData();
        formData.append('file', selectedFile);

        try {
            const response = await axios.post('/upload', formData, {
                headers: {
                    'Content-Type': 'multipart/form-data'
                }
            });
            alert('File uploaded successfully: ' + response.data.filename);
        } catch (error) {
            alert('Failed to upload file. Please try again.');
        }
    };

    return (
        <div>
            <input type="file" onChange={handleFileChange} accept="image/*" />
            <button onClick={handleUpload}>Upload Image</button>
        </div>
    );
};

export default Chat;
