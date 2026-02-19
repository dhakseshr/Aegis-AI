import React, { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import axios from "axios";

export default function Dashboard() {
  const [incidents, setIncidents] = useState<any[]>([]);

  useEffect(() => {
    axios.get("/api/v1/reports").then(r => setIncidents(r.data)).catch(() => {});
    const iv = setInterval(() => {
      axios.get("/api/v1/reports").then(r => setIncidents(r.data)).catch(() => {});
    }, 5000);
    return () => clearInterval(iv);
  }, []);

  return (
    <div className="space-y-6">
      <div className="grid grid-cols-3 gap-4">
        {[["Total Incidents", incidents.length], ["Active", incidents.filter(i=>i.status==="processing").length], ["Resolved", incidents.filter(i=>i.status==="done").length]].map(([label, val]) => (
          <div key={label as string} className="bg-gray-800 rounded p-4 border border-gray-700 text-center">
            <div className="text-3xl font-bold text-red-400">{val}</div>
            <div className="text-gray-400 text-sm mt-1">{label}</div>
          </div>
        ))}
      </div>
      <h2 className="text-xl font-semibold text-gray-200">Recent Incidents</h2>
      <div className="space-y-2">
        {incidents.length === 0 && <p className="text-gray-500">No incidents yet. <Link to="/submit" className="text-red-400 underline">Submit one.</Link></p>}
        {incidents.map(inc => (
          <Link key={inc.incident_id} to={`/report/${inc.incident_id}`}
            className="block bg-gray-800 rounded p-3 border border-gray-700 hover:border-red-700 transition">
            <div className="flex justify-between">
              <span className="text-sm text-gray-300">{inc.incident_id}</span>
              <span className={`text-xs font-semibold ${inc.status === "done" ? "text-green-400" : inc.status === "processing" ? "text-yellow-400" : "text-red-400"}`}>{inc.status?.toUpperCase()}</span>
            </div>
            {inc.location && <div className="text-xs text-gray-500 mt-1">{inc.location}</div>}
          </Link>
        ))}
      </div>
    </div>
  );
}
