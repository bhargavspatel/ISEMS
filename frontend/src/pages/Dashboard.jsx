import { useEffect, useState } from "react";
import api from "../api/axios";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
} from "recharts";

function Dashboard() {
  const [data, setData] = useState(null);

  useEffect(() => {
    const token = localStorage.getItem("token");
    if (!token) {
      window.location.href = "/";
      return;
    }

    const fetchDashboard = async () => {
      try {
        const response = await api.get("/dashboard/", {
          headers: { Authorization: `Bearer ${token}` },
        });
        setData(response.data);
      } catch {
        localStorage.removeItem("token");
        window.location.href = "/";
      }
    };

    fetchDashboard();
  }, []);

  const handleLogout = () => {
    localStorage.removeItem("token");
    window.location.href = "/";
  };

  if (!data) {
    return (
      <div className="flex items-center justify-center h-screen text-lg">
        Loading...
      </div>
    );
  }

  const chartData = [];
  data.courses.forEach((course) => {
    course.skills.forEach((skill) => {
      chartData.push({
        skill: skill.skill_name,
        mastery: Math.round(skill.mastery_score * 100),
      });
    });
  });

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Top Bar */}
      <div className="bg-white shadow px-8 py-4 flex justify-between items-center">
        <h1 className="text-2xl font-semibold">
          Welcome, {data.student_name}
        </h1>
        <button
          onClick={handleLogout}
          className="bg-red-500 hover:bg-red-600 text-white px-4 py-2 rounded-lg"
        >
          Logout
        </button>
      </div>

      <div className="max-w-6xl mx-auto p-8 space-y-8">
        {/* Chart Section */}
        <div className="bg-white p-6 rounded-xl shadow">
          <h2 className="text-xl font-semibold mb-4">
            Skill Mastery Overview
          </h2>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={chartData}>
              <XAxis dataKey="skill" />
              <YAxis domain={[0, 100]} />
              <Tooltip />
              <Bar dataKey="mastery" fill="#6366f1" />
            </BarChart>
          </ResponsiveContainer>
        </div>

        {/* Course Cards */}
        {data.courses.map((course) => (
          <div
            key={course.course_id}
            className="bg-white p-6 rounded-xl shadow space-y-6"
          >
            <h2 className="text-xl font-semibold">
              {course.course_title}
            </h2>

            {course.skills.map((skill) => (
              <div
                key={skill.skill_id}
                className="border border-gray-200 rounded-lg p-4 hover:shadow-md transition"
              >
                <div className="flex justify-between mb-2">
                  <h3 className="font-medium">
                    {skill.skill_name}
                  </h3>
                  <span className="text-sm text-gray-600">
                    {(skill.mastery_score * 100).toFixed(0)}%
                  </span>
                </div>

                <div className="w-full bg-gray-200 h-2 rounded-full mb-3">
                  <div
                    className="h-2 rounded-full bg-indigo-500"
                    style={{
                      width: `${skill.mastery_score * 100}%`,
                    }}
                  />
                </div>

                {skill.recommendation && (
                  <div className="text-sm text-gray-700">
                    <p className="font-semibold mb-1">
                      AI Insight:
                    </p>
                    <p>{skill.recommendation.summary}</p>
                  </div>
                )}
              </div>
            ))}
          </div>
        ))}
      </div>
    </div>
  );
}

export default Dashboard;