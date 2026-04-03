import { useState, useRef, useEffect } from 'react';
import axios from 'axios';
 
const API_URL = 'http://localhost:8000';
 
function Message({ msg }) {
  const isUser = msg.role === 'user';
return (
    <div className={`flex ${isUser ? 'justify-end' : 'justify-start'} mb-4`}>
      <div className={`max-w-2xl px-4 py-3 rounded-2xl shadow
        ${isUser
          ? 'bg-blue-600 text-white rounded-br-none'
          : 'bg-white text-gray-800 rounded-bl-none border border-gray-200'
        }`}>
        <p className='whitespace-pre-wrap'>{msg.content}</p>
        {msg.sources && msg.sources.length > 0 && (
          <div className='mt-2 pt-2 border-t border-gray-200'>
            <p className='text-xs text-gray-500 font-semibold'>Sources:</p>
            {msg.sources.map((s, i) => (
              <p key={i} className='text-xs text-blue-600'>{s}</p>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
 
export default function App() {
  const [messages, setMessages] = useState([{
    role: 'assistant',
    content: 'Welcome. Ask any question about Sri Sri Anukul thakur\'s teachings.',
    sources: []
  }]);
  const [input, setInput]   = useState('');
  const [loading, setLoading] = useState(false);
  const bottomRef = useRef(null);
 
  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);
 
  const sendMessage = async () => {
    if (!input.trim() || loading) return;
    const question = input.trim();
    setInput('');
    setMessages(prev => [...prev, { role: 'user', content: question }]);
    setLoading(true);
    try {
      const res = await axios.post(`${API_URL}/ask`, { question });
      setMessages(prev => [...prev, {
        role: 'assistant',
        content: res.data.answer,
        sources: res.data.sources
      }]);
    } catch (err) {
      setMessages(prev => [...prev, {
        role: 'assistant',
        content: 'Error connecting to the server. Please ensure the backend is running.',
        sources: []
      }]);
    }
    setLoading(false);
  };
 
  const handleKey = e => {
if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); sendMessage(); }
  };
 
  return (
    <div className='min-h-screen bg-gray-100 flex flex-col'>
      <header className='bg-blue-800 text-white py-4 px-6 shadow'>
        <h1 className='text-xl font-bold'>Ask Sri Sri Anukul Thakur</h1>
        <p className='text-sm text-blue-200'>Answers drawn from the Sri Sri Anukul Thakur's writings</p>
      </header>
      <main className='flex-1 overflow-y-auto p-4 max-w-3xl mx-auto w-full'>
        {messages.map((m, i) => <Message key={i} msg={m} />)}
        {loading && (
          <div className='flex justify-start mb-4'>
            <div className='bg-white px-4 py-3 rounded-2xl shadow border border-gray-200'>
              <p className='text-gray-500 text-sm'>Searching scriptures...</p>
            </div>
          </div>
        )}
        <div ref={bottomRef} />
      </main>
      <footer className='bg-white border-t p-4'>
        <div className='max-w-3xl mx-auto flex gap-2'>
          <textarea
            className='flex-1 border border-gray-300 rounded-xl p-3 text-sm
              resize-none focus:outline-none focus:ring-2 focus:ring-blue-500'
            rows={2}
            value={input}
            onChange={e => setInput(e.target.value)}
            onKeyDown={handleKey}
            placeholder='Type your question in Bengali or English...'
          />
          <button
            onClick={sendMessage}
            disabled={loading || !input.trim()}
            className='bg-blue-600 hover:bg-blue-700 disabled:opacity-50
              text-white px-5 py-2 rounded-xl font-semibold transition'
          >
            Ask
          </button>
        </div>
      </footer>
    </div>
  );
}
