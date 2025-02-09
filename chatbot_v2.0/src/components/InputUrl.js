import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import '../styles/InputUrl.css';

function InputUrl() {
    const [url, setUrl] = useState('');
    const [loading, setLoading] = useState(false);
    const navigate = useNavigate();

    const handleSubmit = async (event) => {
        event.preventDefault();
        setLoading(true);

        const apiUrl = 'http://127.0.0.1:5000/extract';
        const token = 'YOUR_OPENAI_TOKEN_HERE'; // Replace with your actual token

        try {
            await axios.post(
                apiUrl,
                { url: url },
                { headers: { Authorization: 'Bearer ' + token } }
            );
            navigate('/chat', { state: { url: url } });
        } catch (error) {
            console.error('Error:', error);
        } finally {
            setLoading(false);
        }
    };

    if (loading) {
        return (
            <div className="loading-overlay">
                <div className="loading-text">Loading...</div>
            </div>
        );
    }

    return (
        <div className="input-container">
            <h1>Chat with your repository</h1>
            <p>Provide the url to your repository to start interacting with it :)</p>
            <form onSubmit={handleSubmit}>
                <input
                    type="url"
                    value={url}
                    onChange={(e) => setUrl(e.target.value)}
                    placeholder="https://github.com/owner/repository"
                    required
                />
                <button type="submit">Submit</button>
            </form>
        </div>
    );
}

export default InputUrl;
