import React, { useEffect, useState } from 'react';
import { getNotes, createNote, deleteNote, getApplications } from '../api';
import { Link } from 'react-router-dom';

function Notes() {
    const [notes, setNotes] = useState([]);
    const [applications, setApplications] = useState([]);

    const [content, setContent] = useState('');
    const [applicationId, setApplicationId] = useState('');

    const [loading, setLoading] = useState(true);
    const [error, setError] = useState('');

    const fetchData = async () => {
        try {
            const [notesData, appsData] = await Promise.all([
                getNotes(),
                getApplications()
            ]);

            setNotes(notesData);
            setApplications(appsData);
        } catch (err) {
            console.error(err);
            setError('取得に失敗しました');
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchData();
    }, []);

    const handleCreate = async (e) => {
        e.preventDefault();
        setError('');

        if (!content || !applicationId) {
            setError('内容と応募を選択してください');
            return;
        }

        try {
            await createNote({
                content,
                application_id: Number(applicationId)
            });

            setContent('');
            setApplicationId('');
            fetchData();
        } catch (err) {
            console.error(err);
            setError('作成に失敗しました');
        }
    };

    const handleDelete = async (id) => {
        if (!confirm('削除する？')) return;

        try {
            await deleteNote(id);
            setNotes(notes.filter(n => n.id !== id));
        } catch (err) {
            console.error(err);
            setError('削除に失敗しました');
        }
    };

    if (loading) return <p>読み込み中...</p>;

    return (
        <div className="notes-container">
            <h2>メモ一覧</h2>
            <Link to="/">← ダッシュボードに戻る</Link>
            {/* 作成フォーム */}
            <form onSubmit={handleCreate}>
                <textarea
                    placeholder="メモ内容"
                    value={content}
                    onChange={(e) => setContent(e.target.value)}
                />

                <select
                    value={applicationId}
                    onChange={(e) => setApplicationId(e.target.value)}
                >
                    <option value="">応募を選択</option>
                    {applications.map(app => (
                        <option key={app.id} value={app.id}>
                            {app.position}
                        </option>
                    ))}
                </select>

                <button type="submit">追加</button>
            </form>

            {error && <p className="error">{error}</p>}

            {/* 一覧 */}
            <ul>
                {notes.map(note => (
                    <li key={note.id}>
                        {note.content}
                        <button onClick={() => handleDelete(note.id)}>
                            削除
                        </button>
                    </li>
                ))}
            </ul>
        </div>
    );
}

export default Notes;