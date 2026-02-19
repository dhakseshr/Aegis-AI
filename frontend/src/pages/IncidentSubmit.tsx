import React, { useState, useEffect, useRef } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";
import AgentStatus from "../components/AgentStatus";

const AGENTS = ["intake","research","risk","resource","knowledge_graph","strategy","verification","report"];

export default function IncidentSubmit() {
  const [query, setQuery] = useState("");
  const [incidentId, setIncidentId] = useState<string|null>(null);
  const [agentStatus, setAgentStatus] = useState<Record<string,string>>({});
  const [traces, setTraces] = useState<Record<string,string[]>>({});
  const [done, setDone] = useState(false);
  const ws = useRef<WebSocket|null>(null);
  const nav = useNavigate();

  async function submit() {
    const res = await axios.post("/api/v1/incidents", { query });
    setIncidentId(res.data.incident_id);
  }

  useEffect(() => {
    if (!incidentId) return;
    ws.current = new WebSocket(`ws://localhost:8000/api/v1/incidents/${incidentId}/stream`);
    ws.current.onmessage = (e) => {
      const d = JSON.parse(e.data);
      if (d.current_agent) setAgentStatus(p => ({...p, [d.current_agent]: "running"}));
      if (d.reasoning_traces) setTraces(d.reasoning_traces);
      if (d.status === "done") { setDone(true); ws.current?.close(); }
    };
    return () => ws.current?.close();
  }, [incidentId]);

  return (
    <div className="max-w-3xl mx-auto space-y-6">
      <h1 className="text-2xl font-bold text-red-400">Submit Disaster Incident</h1>
      <textarea
        className="w-full bg-gray-800 rounded p-4 text-sm h-32 resize-none border border-gray-700 focus:border-red-600 outline-none"
        placeholder="Describe the disaster scenario..."
        value={query} onChange={e => setQuery(e.target.value)}
      />
      <button onClick={submit}
        className="bg-red-700 hover:bg-red-600 px-6 py-2 rounded font-semibold">
        Dispatch Agents
      </button>
      {incidentId && <AgentStatus agents={AGENTS} status={agentStatus} traces={traces} />}
      {done && (
        <button onClick={() => nav(`/report/${incidentId}`)}
          className="bg-green-700 hover:bg-green-600 px-6 py-2 rounded font-semibold">
          View Report
        </button>
      )}
    </div>
  );
}
