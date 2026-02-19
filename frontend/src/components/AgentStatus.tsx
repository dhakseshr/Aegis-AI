import React from "react";

interface Props {
  agents: string[];
  status: Record<string, string>;
  traces: Record<string, string[]>;
}

const LABELS: Record<string,string> = {
  intake: "1. Incident Intake", research: "2. Situation Research",
  risk: "3. Infrastructure Risk", resource: "4. Resource Discovery",
  knowledge_graph: "5. Knowledge Graph", strategy: "6. Strategy Planning",
  verification: "7. Verification", report: "8. Report Generation",
};

export default function AgentStatus({ agents, status, traces }: Props) {
  return (
    <div className="space-y-2">
      {agents.map(agent => {
        const s = status[agent] || "pending";
        const color = s === "done" ? "text-green-400" : s === "running" ? "text-yellow-400 animate-pulse" : "text-gray-500";
        return (
          <div key={agent} className="bg-gray-800 rounded p-3 border border-gray-700">
            <div className={`font-semibold ${color}`}>{LABELS[agent] || agent} — {s.toUpperCase()}</div>
            {traces[agent] && (
              <ul className="mt-1 text-xs text-gray-400 list-disc pl-5">
                {traces[agent].map((t,i) => <li key={i}>{t}</li>)}
              </ul>
            )}
          </div>
        );
      })}
    </div>
  );
}
