import React from "react";
import { BrowserRouter, Routes, Route, Link } from "react-router-dom";
import Dashboard from "./pages/Dashboard";
import IncidentSubmit from "./pages/IncidentSubmit";
import ReportView from "./pages/ReportView";

export default function App() {
  return (
    <BrowserRouter>
      <div className="min-h-screen bg-gray-950 text-white">
        <nav className="bg-gray-900 border-b border-red-800 px-6 py-4 flex items-center gap-8">
          <span className="text-red-500 font-bold text-xl tracking-widest">AEGIS AI</span>
          <Link to="/" className="text-gray-300 hover:text-white">Dashboard</Link>
          <Link to="/submit" className="text-gray-300 hover:text-white">New Incident</Link>
        </nav>
        <main className="p-6">
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/submit" element={<IncidentSubmit />} />
            <Route path="/report/:id" element={<ReportView />} />
          </Routes>
        </main>
      </div>
    </BrowserRouter>
  );
}
