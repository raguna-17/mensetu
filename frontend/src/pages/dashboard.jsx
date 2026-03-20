import React, { useEffect, useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import {
    getCurrentUser,
    getCompanies,
    getApplications,
    getNotes,
    setToken
} from '../api';

function Dashboard() {
    const navigate = useNavigate();

    const [username, setUsername] = useState('');
    const [companiesCount, setCompaniesCount] = useState(0);
    const [applicationsCount, setApplicationsCount] = useState(0);
    const [notesCount, setNotesCount] = useState(0);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetchData = async () => {
            try {
                // 並列実行（ここが大事）
                const [user, companies, applications, notes] = await Promise.all([
                    getCurrentUser(),
                    getCompanies(),
                    getApplications(),
                    getNotes()
                ]);

                setUsername(user.email);
                setCompaniesCount(companies.length);
                setApplicationsCount(applications.length);
                setNotesCount(notes.length);

            } catch (err) {
                console.error(err);
                handleLogout(); // トークン不正時の統一処理
            } finally {
                setLoading(false);
            }
        };

        fetchData();
    }, []);

    const handleLogout = () => {
        setToken(null); // api側と同期
        navigate('/auth');
    };

    if (loading) {
        return <p>読み込み中...</p>;
    }

    return (
        <div className="dashboard-container">
            <div className="dashboard-header">
                <h2>ようこそ</h2>
                <button onClick={handleLogout}>ログアウト</button>
            </div>

            <div className="dashboard-summary">
                <div className="summary-card">
                    <h3>会社</h3>
                    <p>合計: {companiesCount} 件</p>
                    <Link to="/companies">詳細を見る</Link>
                </div>

                <div className="summary-card">
                    <h3>アプリケーション</h3>
                    <p>合計: {applicationsCount} 件</p>
                    <Link to="/applications">詳細を見る</Link>
                </div>

                <div className="summary-card">
                    <h3>メモ</h3>
                    <p>合計: {notesCount} 件</p>
                    <Link to="/notes">詳細を見る</Link>
                </div>
            </div>
        </div>
    );
}

export default Dashboard;