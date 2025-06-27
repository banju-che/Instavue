import React, { useState, useContext } from "react";
import { AuthContext } from "../contexts/AuthContexts";
import { useNavigate } from "react-router-dom";

const Login = () => {
  const { login } = useContext(AuthContext);
  const [form, setForm] = useState({ username: "", password: "" });
  const [error, setError] = useState("");

  const navigate = useNavigate()

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    const success = await login(form.username, form.password);
    navigate('/')
    if (!success) setError("Invalid credentials. Try again.");
  };

  return (
    <div className="flex min-h-screen items-center justify-center bg-light px-4">
      <div className="w-full max-w-md rounded-xl bg-white p-8 shadow-lg border border-gray-200">
        <h2 className="mb-6 text-3xl font-bold text-dark text-center">Welcome Back</h2>
        {error && <p className="mb-4 text-sm text-error text-center">{error}</p>}

        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-dark mb-1">Username</label>
            <input
              type="text"
              name="username"
              value={form.username}
              onChange={handleChange}
              className="w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary"
              required
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-dark mb-1">Password</label>
            <input
              type="password"
              name="password"
              value={form.password}
              onChange={handleChange}
              className="w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary"
              required
            />
          </div>

          <button
            type="submit"
            className="w-full bg-primary text-black py-2 rounded-md hover:bg-indigo-700 transition duration-200"
          >
            Log In
          </button>
        </form>

        <p className="mt-4 text-sm text-center text-gray-600">
          Don’t have an account?{" "}
          <a href="/register" className="text-accent hover:underline font-medium">
            Sign up
          </a>
        </p>
      </div>
    </div>
  );
};

export default Login;
