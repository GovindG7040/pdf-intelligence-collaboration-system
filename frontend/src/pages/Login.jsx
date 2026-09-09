import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";

import { login } from "../services/api";

function Login() {

    const navigate = useNavigate();

    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");

    const [loading, setLoading] = useState(false);
    const [error, setError] = useState("");

    const handleSubmit = async (event) => {

        event.preventDefault();

        setLoading(true);
        setError("");

        try {

            const data = await login(
                email,
                password
            );

            localStorage.setItem(
                "token",
                data.access_token
            );

            navigate("/dashboard");

        } catch (error) {

            console.error(error);

            setError(
                error.response?.data?.detail ||
                "Login failed."
            );

        } finally {

            setLoading(false);

        }
    };

    return (

        <div className="auth-page">

            <div className="auth-card">

                <h1>PDF Intelligence</h1>

                <p>
                    Sign in to continue
                </p>

                {error && (
                    <div className="error-message">
                        {error}
                    </div>
                )}

                <form onSubmit={handleSubmit}>

                    <label>
                        Email
                    </label>

                    <input
                        type="email"
                        value={email}
                        onChange={(event) =>
                            setEmail(event.target.value)
                        }
                        placeholder="you@example.com"
                        required
                    />

                    <label>
                        Password
                    </label>

                    <input
                        type="password"
                        value={password}
                        onChange={(event) =>
                            setPassword(event.target.value)
                        }
                        placeholder="Password"
                        required
                    />

                    <button
                        type="submit"
                        disabled={loading}
                    >
                        {loading
                            ? "Signing in..."
                            : "Sign In"}
                    </button>

                </form>

                <p className="auth-footer">
                    Don't have an account?{" "}
                    <Link to="/signup">
                        Create one
                    </Link>
                </p>

            </div>

        </div>

    );
}

export default Login;