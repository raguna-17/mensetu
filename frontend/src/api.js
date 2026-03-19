// src/api.js
import axios from "axios";

const API_BASE = import.meta.env.VITE_API_URL;

// ===== トークン管理 =====
let token = localStorage.getItem("token") || null;

export function setToken(t) {
    token = t;
    if (t) {
        localStorage.setItem("token", t);
    } else {
        localStorage.removeItem("token");
    }
}

// ===== Axios インスタンス =====
const api = axios.create({
    baseURL: API_BASE,
    headers: {
        "Content-Type": "application/json",
    },
});

// ===== リクエスト時にトークン付与 =====
api.interceptors.request.use(config => {
    if (token) {
        config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
});

// ===== 共通エラーハンドリング =====
function handleError(err) {
    console.error(err.response?.data || err.message);
    throw err;
}

// ========== Users ==========
export async function registerUser(email, password) {
    try {
        const res = await api.post("/users/register", { email, password });
        return res.data;
    } catch (err) {
        handleError(err);
    }
}

export async function loginUser(email, password) {
    try {
        const res = await api.post("/users/login", { email, password });
        setToken(res.data.access_token);
        return res.data;
    } catch (err) {
        handleError(err);
    }
}

export async function logoutUser() {
    setToken(null);
}

export async function getCurrentUser() {
    try {
        const res = await api.get("/users/me");
        return res.data;
    } catch (err) {
        handleError(err);
    }
}

// ========== Applications ==========
export async function getApplications() {
    try {
        const res = await api.get("/applications");
        return res.data;
    } catch (err) {
        handleError(err);
    }
}

export async function createApplication(application) {
    try {
        const res = await api.post("/applications", application);
        return res.data;
    } catch (err) {
        handleError(err);
    }
}

export async function deleteApplication(id) {
    try {
        await api.delete(`/applications/${id}`);
    } catch (err) {
        handleError(err);
    }
}

// ========== Companies ==========
export async function getCompanies() {
    const res = await api.get("/companies");
    return res.data;
}

export async function createCompany(company) {
    const res = await api.post("/companies", company);
    return res.data;
}

export async function deleteCompany(id) {
    await api.delete(`/companies/${id}`);
}

// ========== Notes ==========
export async function getNotes() {
    const res = await api.get("/notes");
    return res.data;
}

export async function createNote(note) {
    const res = await api.post("/notes", note);
    return res.data;
}

export async function deleteNote(id) {
    await api.delete(`/notes/${id}`);
}