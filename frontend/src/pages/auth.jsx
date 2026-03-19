import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { loginUser, registerUser } from '../api';

function Auth() {
    const navigate = useNavigate();

    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [isRegister, setIsRegister] = useState(false);
    const [error, setError] = useState('');
    const [loading, setLoading] = useState(false);

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError('');
        setLoading(true);

        try {
            if (isRegister) {
                await registerUser(email, password);
                alert('登録成功。ログインしてください。');
                setIsRegister(false);
            } else {
                await loginUser(email, password); // ← tokenはapi側で保存
                navigate('/');
            }
        } catch (err) {
            setError(err.response?.data?.detail || 'エラーが発生しました');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="auth-container">
            <h2>{isRegister ? '新規登録' : 'ログイン'}</h2>

            <form onSubmit={handleSubmit}>
                <input
                    type="email"
                    placeholder="Email"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    required
                />

                <input
                    type="password"
                    placeholder="Password"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    required
                />

                {error && <p className="error">{error}</p>}

                <button type="submit" disabled={loading}>
                    {loading ? '処理中...' : (isRegister ? '登録' : 'ログイン')}
                </button>
            </form>

            <button onClick={() => setIsRegister(!isRegister)}>
                {isRegister
                    ? '既にアカウントがありますか？ログイン'
                    : 'アカウントを作成'}
            </button>
        </div>
    );
}

export default Auth;