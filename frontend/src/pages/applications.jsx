import React, { useEffect, useState } from 'react';
import {
    getApplications,
    createApplication,
    deleteApplication,
    getCompanies
} from '../api';
import { Link } from 'react-router-dom';

function Applications() {
    const [applications, setApplications] = useState([]);
    const [companies, setCompanies] = useState([]);

    const [position, setPosition] = useState('');
    const [status, setStatus] = useState('applied');
    const [companyId, setCompanyId] = useState('');

    const [loading, setLoading] = useState(true);
    const [error, setError] = useState('');

    const fetchApplications = async () => {
        try {
            const data = await getApplications();
            setApplications(data);
        } catch (err) {
            console.error(err);
            setError('取得に失敗しました');
        } finally {
            setLoading(false);
        }
    };

    const fetchCompanies = async () => {
        try {
            const data = await getCompanies();
            setCompanies(data);

            { companies.length === 0 && <p>会社を先に登録してください</p> }
        } catch (err) {
            console.error(err);
        }
    };

    useEffect(() => {
        fetchApplications();
        fetchCompanies();
    }, []);

    const handleCreate = async (e) => {
        e.preventDefault();
        setError('');

        if (!position) {
            setError('ポジションは必須');
            return;
        }

        if (!companyId) {
            setError('会社を選択してください');
            return;
        }

        try {
            await createApplication({
                position,
                status,
                company_id: Number(companyId)
            });

            setPosition('');
            setStatus('applied');
            fetchApplications();
        } catch (err) {
            console.error(err);
            setError('作成に失敗しました');
        }
    };

    const handleDelete = async (id) => {
        if (!confirm('削除する？')) return;

        try {
            await deleteApplication(id);
            setApplications(applications.filter(app => app.id !== id));
        } catch (err) {
            console.error(err);
            setError('削除に失敗しました');
        }
    };

    if (loading) return <p>読み込み中...</p>;

    return (
        <div className="applications-container">
            <h2>応募一覧</h2>
            <Link to="/">← ダッシュボードに戻る</Link>

            {/* 作成フォーム */}
            <form onSubmit={handleCreate}>
                <input
                    type="text"
                    placeholder="ポジション"
                    value={position}
                    onChange={(e) => setPosition(e.target.value)}
                />

                <select value={companyId} onChange={(e) => setCompanyId(e.target.value)}>
                    {companies.map(c => (
                        <option key={c.id} value={c.id}>
                            {c.name}
                        </option>
                    ))}
                </select>

                <select value={status} onChange={(e) => setStatus(e.target.value)}>
                    <option value="applied">応募済み</option>
                    <option value="interview">面接中</option>
                    <option value="offer">内定</option>
                    <option value="rejected">不採用</option>
                </select>

                <button type="submit">追加</button>
            </form>

            {error && <p className="error">{error}</p>}

            {/* 一覧 */}
            <ul>
                {applications.map(app => (
                    <li key={app.id}>
                        <strong>{app.position}</strong>
                        {' - '}
                        {app.status}

                        <button onClick={() => handleDelete(app.id)}>
                            削除
                        </button>
                    </li>
                ))}
            </ul>
        </div>
    );
}

export default Applications;