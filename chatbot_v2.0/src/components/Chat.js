import React, { useState } from 'react';
import { useLocation } from 'react-router-dom';
import axios from 'axios';
import '../styles/Chat.css';
import botAvatar from '../resources/bot-avatar.png';
import humanAvatar from '../resources/human-avatar.png';

function Chat() {
    const [messages, setMessages] = useState([
        { text: 'Hello! 👋, how may I assist you today?', author: 'bot' },
    ]);
    const [newMessage, setNewMessage] = useState('');
    const [isLoading, setIsLoading] = useState(false);

    const location = useLocation();
    const url = location.state.url;

    const sendMessage = async (event) => {
        event.preventDefault();
        setIsLoading(true);

        const apiUrl = 'http://127.0.0.1:5000/lang-chat-sources';
        const token = 'YOUR_OPENAI_TOKEN_HERE'; // Replace with your actual token

        console.log("Sending message to url:", apiUrl);

        try {
            const response = await axios.post(
                apiUrl,
                { user_input: newMessage, url: url },
                { headers: { Authorization: 'Bearer ' + token } }
            );

            const botResponse = {
                text: response.data.response,
                author: 'bot',
                source: response.data.sources.map((source) => ({
                    ...source,
                    page_content: source.page_content
                        .replace(/\\n/g, '<br/>')
                        .replace(/\\r/g, '')
                        .replace(/\\t/g, '&nbsp;&nbsp;&nbsp;&nbsp;'),
                })),
                showSource: false,
            };

            setMessages([...messages, { text: newMessage, author: 'user' }, botResponse]);
            setNewMessage('');
        } catch (error) {
            console.error('Error:', error);
        } finally {
            setIsLoading(false);
        }
    };

    const toggleSource = (index) => {
        console.log("toggleSource function called for message index:", index); 

        const updatedMessages = messages.map((message, i) => {
            if (i === index && message.author === 'bot') {
                return { ...message, showSource: !message.showSource };
            }
            return message;
        });

        console.log("Updated messages:", updatedMessages); 
        setMessages(updatedMessages);
    };

    return (
        <div className="chat-container">
            <div className="chat-messages">
                {messages.map((message, index) => (
                    <div className={`message ${message.author}`} key={index}>
                        {message.author === 'bot' ? (
                            <img
                                className="avatar left"
                                src={botAvatar}
                                alt="Bot avatar"
                            />
                        ) : null}

                        <div className="text">
                            {message.text}
                            {message.author === 'bot' && (
                                <>
                                    <button onClick={() => toggleSource(index)}>
                                        View Source
                                    </button>
                                    {message.showSource && (
                                        <div
                                            className="source"
                                            style={{ display: 'block' }} 
                                            dangerouslySetInnerHTML={{ __html: message.source.map(s => s.page_content).join('<br /><br />') }}
                                        />
                                    )}
                                </>
                            )}
                        </div>

                        {message.author !== 'bot' ? (
                            <img
                                className="avatar"
                                src={humanAvatar}
                                alt="User avatar"
                            />
                        ) : null}
                    </div>
                ))}
            </div>
            <div className="message-input">
                <input
                    type="text"
                    placeholder="Ask a question..."
                    value={newMessage}
                    onChange={(e) => setNewMessage(e.target.value)}
                    onKeyPress={(e) => e.key === 'Enter' && sendMessage(e)}
                />
                <button onClick={(e) => sendMessage(e)} disabled={isLoading}>Send</button>
            </div>
        </div>
    );
}

export default Chat;
