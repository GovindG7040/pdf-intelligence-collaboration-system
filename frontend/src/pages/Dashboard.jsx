import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

import {
    getDocuments,
    uploadDocument,
} from "../services/api";

function Dashboard() {

    const navigate = useNavigate();

    const [documents, setDocuments] = useState([]);
    const [search, setSearch] = useState("");

    const [file, setFile] = useState(null);
    const [uploading, setUploading] = useState(false);

    const [loading, setLoading] = useState(true);
    const [error, setError] = useState("");

    const loadDocuments = async () => {

        try {

            setLoading(true);

            const data = await getDocuments();

            setDocuments(data);

        } catch (error) {

            console.error(error);

            if (error.response?.status === 401) {

                localStorage.removeItem("token");

                navigate("/login");

                return;
            }

            setError(
                error.response?.data?.detail ||
                "Failed to load documents."
            );

        } finally {

            setLoading(false);

        }
    };

    useEffect(() => {

        loadDocuments();

    }, []);

    const handleUpload = async (event) => {

        event.preventDefault();

        if (!file) {
            return;
        }

        setUploading(true);
        setError("");

        try {

            const document = await uploadDocument(file);

            setDocuments((previous) => [
                document,
                ...previous,
            ]);

            setFile(null);

            event.target.reset();

        } catch (error) {

            console.error(error);

            setError(
                error.response?.data?.detail ||
                "Failed to upload PDF."
            );

        } finally {

            setUploading(false);

        }
    };

    const handleLogout = () => {

        localStorage.removeItem("token");

        navigate("/login");

    };

    const filteredDocuments = documents.filter(
        (document) =>
            document.filename
                ?.toLowerCase()
                .includes(search.toLowerCase())
    );

    return (

        <div className="dashboard-page">

            <header className="dashboard-header">

                <div>

                    <h1>PDF Intelligence</h1>

                    <p>
                        Manage, analyze and collaborate on your PDFs.
                    </p>

                </div>

                <button
                    type="button"
                    onClick={handleLogout}
                >
                    Logout
                </button>

            </header>

            {error && (
                <div className="error-message">
                    {error}
                </div>
            )}

            <section className="upload-card">

                <h2>Upload a PDF</h2>

                <form onSubmit={handleUpload}>

                    <input
                        type="file"
                        accept="application/pdf,.pdf"
                        onChange={(event) =>
                            setFile(event.target.files[0])
                        }
                    />

                    <button
                        type="submit"
                        disabled={!file || uploading}
                    >
                        {uploading
                            ? "Uploading..."
                            : "Upload PDF"}
                    </button>

                </form>

                <p>
                    Maximum file size: 20 MB
                </p>

            </section>

            <section className="documents-section">

                <div className="documents-heading">

                    <div>

                        <h2>Your Documents</h2>

                        <p>
                            {documents.length} document
                            {documents.length !== 1 ? "s" : ""}
                        </p>

                    </div>

                    <input
                        type="search"
                        placeholder="Search by filename..."
                        value={search}
                        onChange={(event) =>
                            setSearch(event.target.value)
                        }
                    />

                </div>

                {loading ? (

                    <div className="loading">
                        Loading documents...
                    </div>

                ) : filteredDocuments.length === 0 ? (

                    <div className="empty-state">

                        <h3>
                            {search
                                ? "No matching documents"
                                : "No documents yet"}
                        </h3>

                        <p>
                            {search
                                ? "Try another filename."
                                : "Upload your first PDF to get started."}
                        </p>

                    </div>

                ) : (

                    <div className="document-grid">

                        {filteredDocuments.map((document) => (

                            <article
                                key={document.id}
                                className="document-card"
                                onClick={() =>
                                    navigate(
                                        `/documents/${document.id}`
                                    )
                                }
                            >

                                <div className="document-icon">
                                    PDF
                                </div>

                                <div className="document-info">

                                    <h3>
                                        {document.filename}
                                    </h3>

                                    <p>
                                        {document.created_at
                                            ? new Date(
                                                document.created_at
                                            ).toLocaleDateString()
                                            : ""}
                                    </p>

                                    <p className="document-summary">

                                        {document.summary ||
                                            "No summary available."}

                                    </p>

                                </div>

                            </article>

                        ))}

                    </div>

                )}

            </section>

        </div>

    );
}

export default Dashboard;