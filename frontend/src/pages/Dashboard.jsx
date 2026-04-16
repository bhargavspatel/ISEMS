import { useEffect, useState } from "react";
import api from "../api/axios";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  LineChart,
  Line,
  CartesianGrid,
  Legend,
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
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });
        setData(response.data);
      } catch (error) {
        console.error("Dashboard error:", error);
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
      <div className="flex items-center justify-center h-screen text-xl">
        Loading Dashboard...
      </div>
    );
  }

  // Prepare chart data
  const chartData = [];
  let weakestSkill = null;
  let strongestSkill = null;
  let totalMastery = 0;
  let skillCount = 0;

  data.courses.forEach((course) => {
    course.skills.forEach((skill) => {
      chartData.push({
        skill: skill.skill_name,
        mastery: Math.round(skill.mastery_score * 100),
      });

      totalMastery += skill.mastery_score;
      skillCount++;

      if (!weakestSkill || skill.mastery_score < weakestSkill.mastery_score) {
        weakestSkill = skill;
      }

      if (!strongestSkill || skill.mastery_score > strongestSkill.mastery_score) {
        strongestSkill = skill;
      }
    });
  });

  const averageMastery = skillCount > 0 ? totalMastery / skillCount : 0;

  let riskLevel = "Low";
  if (averageMastery < 0.5) {
    riskLevel = "High";
  } else if (averageMastery < 0.75) {
    riskLevel = "Medium";
  }

  return (
    <div className="min-h-screen bg-gray-100 p-10">
      {/* Header */}
      <div className="flex justify-between items-center mb-8">
        <h1 className="text-4xl font-bold">
          Welcome, {data.student_name}
        </h1>
        <button
          onClick={handleLogout}
          className="bg-red-500 hover:bg-red-600 text-white px-4 py-2 rounded-lg"
        >
          Logout
        </button>
      </div>

      {/* AI Insights Panel */}
      <div className="bg-white p-6 rounded-xl shadow-md mb-6">
        <h2 className="text-xl font-semibold mb-4">AI Learning Insights</h2>
        <div className="grid grid-cols-2 gap-6">
          <div>
            <p className="font-semibold">Strongest Skill:</p>
            <p>
              {strongestSkill?.skill_name} (
              {(strongestSkill?.mastery_score * 100).toFixed(0)}%)
            </p>
          </div>
          <div>
            <p className="font-semibold">Weakest Skill:</p>
            <p>
              {weakestSkill?.skill_name} (
              {(weakestSkill?.mastery_score * 100).toFixed(0)}%)
            </p>
          </div>
          <div>
            <p className="font-semibold">Average Mastery:</p>
            <p>{(averageMastery * 100).toFixed(0)}%</p>
          </div>
          <div>
            <p className="font-semibold">Risk Level:</p>
            <p
              className={
                riskLevel === "High"
                  ? "text-red-500 font-bold"
                  : riskLevel === "Medium"
                  ? "text-yellow-500 font-bold"
                  : "text-green-500 font-bold"
              }
            >
              {riskLevel}
            </p>
          </div>
        </div>
      </div>

      {/* Mastery Bar Chart */}
      <div className="bg-white p-6 rounded-xl shadow-md mb-6">
        <h2 className="text-xl font-semibold mb-4">Skill Mastery Overview</h2>
        <ResponsiveContainer width="100%" height={300}>
          <BarChart data={chartData}>
            <XAxis dataKey="skill" />
            <YAxis domain={[0, 100]} />
            <Tooltip />
            <Legend />
            <Bar dataKey="mastery" fill="#4f46e5" />
          </BarChart>
        </ResponsiveContainer>
      </div>

      {/* Course and Skill Details */}
      {data.courses.map((course) => (
        <div
          key={course.course_id}
          className="bg-white p-6 rounded-xl shadow-md mb-8"
        >
          <h2 className="text-2xl font-semibold mb-4">
            {course.course_title}
          </h2>

          {course.skills.map((skill) => (
            <div
              key={skill.skill_id}
              className="border border-gray-200 p-4 rounded-lg mb-4"
            >
              <h3 className="text-xl font-medium mb-2">
                {skill.skill_name}
              </h3>

              <p className="mb-2">
                Mastery:{" "}
                <strong>
                  {(skill.mastery_score * 100).toFixed(0)}%
                </strong>
              </p>

              <div className="w-64 bg-gray-200 h-3 rounded-full mb-3">
                <div
                  className={`h-3 rounded-full ${
                    skill.mastery_score > 0.75
                      ? "bg-green-500"
                      : skill.mastery_score > 0.5
                      ? "bg-yellow-400"
                      : "bg-red-500"
                  }`}
                  style={{
                    width: `${skill.mastery_score * 100}%`,
                  }}
                />
              </div>

              {skill.recommendation ? (
                <div>
                  <p className="font-semibold">AI Summary:</p>
                  <p className="mb-2">
                    {skill.recommendation.summary}
                  </p>

                  <p className="font-semibold">Recommended Actions:</p>
                  <ul className="list-disc ml-6">
                    {skill.recommendation.recommended_actions.map(
                      (action, index) => (
                        <li key={index}>{action}</li>
                      )
                    )}
                  </ul>

                  <p className="mt-2 text-sm text-gray-500">
                    Confidence: {skill.recommendation.confidence_level}
                  </p>
                </div>
              ) : (
                <p className="text-gray-500">No submissions yet.</p>
              )}
            </div>
          ))}
        </div>
      ))}
    </div>
  );
}

export default Dashboard;