'use client';

import { useState, useEffect, useRef } from 'react';

const apiUrl = process.env.NEXT_PUBLIC_API_URL;

export default function Chatbot() {
  const [threads, setThreads] = useState([]);
  const [selectedThreadId, setSelectedThreadId] = useState(null);
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const chatContainerRef = useRef(null);

  const fetchThreads = async () => {
    try {
      const response = await fetch(`${apiUrl}/threads`);
      const data = await response.json();
      setThreads(data);
      if (data.length > 0) {
        setSelectedThreadId(data[0].id);
      }
    } catch (error) {
      console.error('Error fetching threads:', error);
    }
  };

  const fetchMessages = async (threadId) => {
    try {
      const response = await fetch(`${apiUrl}/threads/${threadId}/messages`);
      const data = await response.json();
      setMessages(data);
    } catch (error) {
      console.error('Error fetching messages:', error);
    }
  };

  useEffect(() => {
    fetchThreads();
  }, []);

  useEffect(() => {
    if (selectedThreadId) {
      fetchMessages(selectedThreadId);
    }
  }, [selectedThreadId]);

  const sendMessage = async () => {
    if (!input.trim()) return;

    try {
      const response = await fetch(`${apiUrl}/thread/${selectedThreadId}/message`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          content: input,
        }),
      });

      const data = await response.json();
      setMessages((prev) => [
        ...prev, data.user, data.bot
      ]);

      setInput('');
    } catch (error) {
      console.error('Error sending message:', error);
    }
  };

  const handleKeyDown = (event) => {
    if (event.key === 'Enter') {
      sendMessage();
    }
  };

  const scrollToBottom = () => {
    if (chatContainerRef.current) {
      chatContainerRef.current.scrollTo({
        top: chatContainerRef.current.scrollHeight,
        behavior: 'smooth',
      });
    }
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  return (
    <div className="flex h-screen">
      <div className="w-1/3 bg-gray-200 p-4 overflow-y-auto">
        <h2 className="text-lg font-bold mb-4">Chat History</h2>
        {threads.map((thread) => (
          <div
            key={thread.id}
            className={`p-2 mb-2 rounded cursor-pointer ${
              selectedThreadId === thread.id ? 'bg-blue-500 text-white' : 'bg-white hover:bg-gray-100'
            }`}
            onClick={() => setSelectedThreadId(thread.id)}
          >
            Thread {thread.id}
          </div>
        ))}
      </div>

      <div className="w-2/3 flex flex-col p-4">
        <div ref={chatContainerRef} className="flex-grow overflow-y-auto p-4 border rounded">
          {messages.map((msg, index) => (
            <div
              key={index}
              className={`p-2 mb-2 rounded ${msg.added_by_user ? 'bg-blue-200' : 'bg-green-200'}`}
            >
              <strong>{msg.added_by_user ? 'You: ' : 'Bot: '}</strong>
              {msg.content}
            </div>
          ))}
        </div>
        <div className="mt-4 flex">
          <input
            className="flex-grow p-2 border rounded"
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="Type your message..."
          />
          <button className="ml-2 bg-blue-500 text-white p-2 rounded" onClick={sendMessage}>
            Send
          </button>
        </div>
      </div>
    </div>
  );
}
