// src/pages/Home.jsx
import React, { useEffect, useState } from "react";

const Home = () => {
  const [posts, setPosts] = useState([]);
  const [error, setError] = useState("");

  useEffect(() => {
    const fetchFeed = async () => {
      try {
        const res = await fetch("http://localhost:8000/api/posts/", {
          headers: {
            Authorization: `Bearer ${localStorage.getItem("access_token")}`,
          },
        });

        if (!res.ok) throw new Error("Failed to load feed");

        const data = await res.json();
        setPosts(data);
      } catch (err) {
        setError("Couldn't load feed. Try logging in again.");
      }
    };

    fetchFeed();
  }, []);

  return (
    <main className="min-h-screen bg-[#F9FAFB] px-4 py-6">
      <h1 className="text-2xl font-bold text-[#2E2E2E] mb-6">Home Feed</h1>

      {error && <p className="text-red-500 mb-4">{error}</p>}

      <div className="flex flex-col gap-6">
        {posts.length === 0 && <p>No posts yet. Follow users to see their posts.</p>}
        {posts.map((post) => (
          <div
            key={post.id}
            className="bg-white rounded-2xl shadow p-4 border border-gray-200"
          >
            <div className="flex items-center gap-4 mb-2">
              <img
                src={post.user_profile_picture || "/default-avatar.png"}
                alt="profile"
                className="w-10 h-10 rounded-full object-cover"
              />
              <span className="font-semibold text-[#2E2E2E]">{post.user_username}</span>
            </div>
            <p className="mb-2 text-gray-700">{post.caption}</p>
            {post.image && (
              <img
                src={post.image}
                alt="Post"
                className="w-full max-h-[400px] object-cover rounded-lg"
              />
            )}
          </div>
        ))}
      </div>
    </main>
  );
};

export default Home;
