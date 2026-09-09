import axios from "axios";

const api = axios.create({
    baseURL: import.meta.env.VITE_API_URL,
});

// ==========================================
// AUTH
// ==========================================

export const signup = async (email, password) => {
    const response = await api.post("/auth/signup", {
        email,
        password,
    });

    return response.data;
};

export const login = async (email, password) => {
    const response = await api.post("/auth/login", {
        email,
        password,
    });

    return response.data;
};

// ==========================================
// AUTH HEADER
// ==========================================

const authConfig = () => {
    const token = localStorage.getItem("token");

    return {
        headers: {
            Authorization: `Bearer ${token}`,
        },
    };
};

// ==========================================
// DOCUMENTS
// ==========================================

export const getDocuments = async () => {
    const response = await api.get(
        "/documents",
        authConfig()
    );

    return response.data;
};

export const getDocument = async (documentId) => {
    const response = await api.get(
        `/documents/${documentId}`,
        authConfig()
    );

    return response.data;
};

export const uploadDocument = async (file) => {
    const formData = new FormData();

    formData.append("file", file);

    const response = await api.post(
        "/documents/upload",
        formData,
        {
            ...authConfig(),
            headers: {
                ...authConfig().headers,
                "Content-Type": "multipart/form-data",
            },
        }
    );

    return response.data;
};

// ==========================================
// SHARING
// ==========================================

export const createShareLink = async (
    documentId,
    invitedEmail = ""
) => {
    const response = await api.post(
        `/documents/${documentId}/share`,
        {
            invited_email: invitedEmail || null,
        },
        authConfig()
    );

    return response.data;
};

export const getSharedDocument = async (token) => {
    const response = await api.get(
        `/documents/shared/${token}`
    );

    return response.data;
};

// ==========================================
// COMMENTS - AUTHENTICATED USER
// ==========================================

export const getComments = async (documentId) => {
    const response = await api.get(
        `/documents/${documentId}/comments`,
        authConfig()
    );

    return response.data;
};

export const addComment = async (
    documentId,
    content
) => {
    const response = await api.post(
        `/documents/${documentId}/comments`,
        {
            content,
        },
        authConfig()
    );

    return response.data;
};

// ==========================================
// COMMENTS - GUEST
// ==========================================

export const getGuestComments = async (token) => {
    const response = await api.get(
        `/documents/shared/${token}/comments`
    );

    return response.data;
};

export const addGuestComment = async (
    token,
    guestName,
    content
) => {
    const response = await api.post(
        `/documents/shared/${token}/comments`,
        {
            guest_name: guestName,
            content: content,
        }
    );

    return response.data;
};

// ==========================================
// AI CHAT - AUTHENTICATED USER
// ==========================================

export const askDocumentQuestion = async (
    documentId,
    question,
    history = []
) => {
    const response = await api.post(
        `/documents/${documentId}/chat`,
        {
            question,
            history,
        },
        authConfig()
    );

    return response.data;
};

// ==========================================
// AI CHAT - GUEST
// ==========================================

export const askSharedQuestion = async (
    token,
    question,
    history = []
) => {
    const response = await api.post(
        `/documents/shared/${token}/chat`,
        {
            question,
            history,
        }
    );

    return response.data;
};

export default api;