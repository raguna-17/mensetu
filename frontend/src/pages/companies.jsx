import React, { useEffect, useState } from 'react';
import { getCompanies, createCompany, deleteCompany } from '../api';
import { Link } from 'react-router-dom';

function Companies() {
    const [companies, setCompanies] = useState([]);
    const [name, setName] = useState('');
    const [industry, setIndustry] = useState('');
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState('');

    const fetchCompanies = async () => {
        try {
            const data = await getCompanies();
            setCompanies(data);
        } catch (err) {
            console.error(err);
            setError('取得に失敗しました');
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchCompanies();
    }, []);

    const handleCreate = async (e) => {
        e.preventDefault();
        setError('');

        if (!name) {
            setError('会社名は必須');
            return;
        }

        try {
            await createCompany({ name, industry });
            setName('');
            setIndustry('');
            fetchCompanies();
        } catch (err) {
            console.error(err);
            setError('作成に失敗しました');
        }
    };

    const handleDelete = async (id) => {
        if (!confirm('削除する？')) return;

        try {
            await deleteCompany(id);
            setCompanies(companies.filter(c => c.id !== id));
        } catch (err) {
            console.error(err);
            setError('削除に失敗しました');
        }
    };

    if (loading) return <p>読み込み中...</p>;

    return (
        <div className="companies-container">
            
            <h2>会社一覧</h2>
            <Link to="/">← ダッシュボードに戻る</Link>
            {/* 作成フォーム */}
            <form onSubmit={handleCreate}>
                <input
                    type="text"
                    placeholder="会社名"
                    value={name}
                    onChange={(e) => setName(e.target.value)}
                />
                <input
                    type="text"
                    placeholder="業界"
                    value={industry}
                    onChange={(e) => setIndustry(e.target.value)}
                />
                <button type="submit">追加</button>
            </form>

            {error && <p className="error">{error}</p>}

            {/* 一覧 */}
            <ul>
                {companies.map(company => (
                    <li key={company.id}>
                        <strong>{company.name}</strong>
                        {company.industry && ` (${company.industry})`}
                        <button onClick={() => handleDelete(company.id)}>
                            削除
                        </button>
                    </li>
                ))}
            </ul>
        </div>
    );
}

export default Companies;