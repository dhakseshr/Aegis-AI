import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import axios from "axios";

export default function ReportView() {
  const { id } = useParams();
  const [report, setReport] = useState<any>(null);

  useEffect(() => {
    axios.get(`/api/v1/reports/${id}`).then(r => setReport(r.data));
  }, [id]);

  if (!report) return <div className="text-gray-400">Loading report...</div>;

  return (
    <div className="max-w-4xl mx-auto space-y-6">
      <h1 className="text-2xl font-bold text-red-400">Emergency Intelligence Report</h1>
      <div className="bg-gray-800 rounded p-4 border border-red-800">
        <h2 className="text-lg font-semibold text-yellow-400 mb-2">Executive Summary</h2>
        <p className="text-gray-200 text-sm">{report.executive_summary}</p>
      </div>
      {report.immediate_actions && (
        <Section title="Immediate Actions" items={report.immediate_actions} color="text-red-400" />
      )}
      {report.evacuation_recommendations && (
        <Section title="Evacuation Recommendations" items={report.evacuation_recommendations} color="text-orange-400" />
      )}
      {report.critical_infrastructure_at_risk && (
        <Section title="Critical Infrastructure at Risk" items={report.critical_infrastructure_at_risk} color="text-yellow-400" />
      )}
      {report.resource_deployment && (
        <Section title="Resource Deployment" items={report.resource_deployment} color="text-blue-400" />
      )}
      <div className="text-xs text-gray-500">Incident ID: {report.incident_id} | Generated: {report.generated_at}</div>
    </div>
  );
}

function Section({ title, items, color }: { title: string; items: string[]; color: string }) {
  return (
    <div className="bg-gray-800 rounded p-4 border border-gray-700">
      <h2 className={`text-base font-semibold ${color} mb-2`}>{title}</h2>
      <ul className="text-sm text-gray-200 list-disc pl-5 space-y-1">
        {items.map((item, i) => <li key={i}>{item}</li>)}
      </ul>
    </div>
  );
}
