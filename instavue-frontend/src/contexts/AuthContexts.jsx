import { createContext, useEffect, useRef, useState } from "react";

export const AuthContext = createContext(null);

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [token, setToken] = useState(localStorage.getItem('access_token'));
  const refreshInterval = useRef(null); // ⏱️ reference to the interval

  useEffect(() => {
    const storedEmail = localStorage.getItem("user_email");
    const storedAccess = localStorage.getItem("access_token");
    const storedRefresh = localStorage.getItem("refresh_token");

    if (storedEmail && storedAccess && storedRefresh) {
      setUser({ email: storedEmail });
      setToken(storedAccess);
      startRefreshLoop(); // 🚀 start refresh loop on login
    }
  }, []);

  // ✅ Login
  const login = async (email, password) => {
    try {
      const res = await fetch("http://localhost:8000/api/auth/jwt/create/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username: email, password }),
      });

      if (!res.ok) throw new Error("Login failed");

      const data = await res.json();
      localStorage.setItem("access_token", data.access);
      localStorage.setItem("refresh_token", data.refresh);
      localStorage.setItem("user_email", email);

      setUser({ email });
      setToken(data.access);
      startRefreshLoop(); // ✅ Start refreshing after login
      return true;
    } catch (err) {
      console.error("Login failed:", err);
      return false;
    }
  };

  // ✅ Refresh token
  const refreshToken = async () => {
    const refresh = localStorage.getItem("refresh_token");
    if (!refresh) return logout();

    try {
      const res = await fetch("http://localhost:8000/auth/jwt/refresh/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ refresh }),
      });

      if (!res.ok) throw new Error("Failed to refresh token");

      const data = await res.json();
      localStorage.setItem("access_token", data.access);
      setToken(data.access);
      console.log("🔄 Access token refreshed");
    } catch (err) {
      console.error("❌ Refresh failed, logging out:", err);
      logout(); // 🚨 Logout if refresh fails
    }
  };

  // ✅ Start token refresh interval
  const startRefreshLoop = () => {
    clearInterval(refreshInterval.current); // Clear existing loop
    refreshInterval.current = setInterval(refreshToken, 55 * 60 * 1000); // Every 55 min
  };

  // ✅ Logout
  const logout = () => {
    localStorage.removeItem("access_token");
    localStorage.removeItem("refresh_token");
    localStorage.removeItem("user_email");
    clearInterval(refreshInterval.current); // ⛔ Stop token refresh
    setUser(null);
    setToken(null);
  };

  return (
    <AuthContext.Provider value={{ user, token, login, logout, refreshToken }}>
      {children}
    </AuthContext.Provider>
  );
};
