import { useState } from 'react';
import { getGreeting } from './api';

export default function App() {
  const [name, setName] = useState('');
  const [greeting, setGreeting] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    try {
      const msg = await getGreeting(name.trim() || undefined);
      setGreeting(msg);
    } catch (err) {
      setError('Failed to contact the API');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ fontFamily: 'sans-serif', padding: '2rem' }}>
      <h1>🧮 Option‑Tool Demo</h1>

      <form onSubmit={handleSubmit}>
        <label>
          Your name:{' '}
          <input
            type="text"
            value={name}
            onChange={(e) => setName(e.target.value)}
            placeholder="World"
          />
        </label>{' '}
        <button type="submit" disabled={loading}>
          {loading ? '…talking' : 'Say hello'}
        </button>
      </form>

      {greeting && <p style={{ marginTop: '1rem' }}>{greeting}</p>}
      {error && <p style={{ color: 'red' }}>{error}</p>}
    </div>
  );
}